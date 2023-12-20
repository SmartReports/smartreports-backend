from django.core.mail import EmailMessage
from django.conf import settings
from django.forms import ValidationError
from .models import UserType, ArchivedReport, Email, Alarm
from .sync_db_kb import get_kpi_value
from base64 import b64decode
from django.template.loader import render_to_string
from django.core.mail import send_mail

def send_emails_for_unsent_reports():
    # Get distinct user types from UserType enumeration
    user_types = [user_type[0] for user_type in UserType.choices]

    for user_type in user_types:
        try:
            # Get the unsent ArchivedReport instances for the user type
            unsent_reports = ArchivedReport.objects.filter(
                user_type=user_type, sent=False
            )

            # Get all corresponding Email instances for the user type
            email_instances = Email.objects.filter(user_type=user_type)

            # Validate that emails field is a list
            for email_instance in email_instances:
                if not isinstance(email_instance.emails, list):
                    raise ValidationError("Emails must be a list")

            # Iterate over each unsent report and send an email for each file
            for report in unsent_reports:
                # Check if the report template matches the user's template
                if report.template.user_type == user_type:
                    # Iterate over each Email instance
                    for email_address in email_instance.emails:
                        # Create an EmailMessage object
                        subject = 'Your SmartReport'
                        message = f'Dear {report.template.user_type},\nThis is your {report.template.frequency} report.'

                        email = EmailMessage(
                            subject = subject,
                            body = message,
                            from_email = settings.DEFAULT_FROM_EMAIL,
                            to = [email_address],
                            reply_to = [settings.DEFAULT_FROM_EMAIL],
                        )

                        # Get the file content from the ArchivedReport
                        file_content = report.file
                        file_content = b64decode(file_content, validate=True)

                        if not report.file_name.endswith('.pdf'):
                            report.file_name = report.file_name + '.pdf'

                        # Attach the file to the email
                        email.attach(report.file_name, file_content, 'application/octet-stream')
                        
                        print(f'sending mail for {report.file_name} to {email_address}')
                        # Send the email
                        print(f'Success: {email.send()== 1}')

                    # Update the sent status of the ArchivedReport
                    report.sent = True
                    report.save()
        except Email.DoesNotExist:
            print(f"Email with user_type {user_type} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")


def send_emails_for_alarms():
    
    alarms = Alarm.objects.all().order_by('kpi', 'user_type')

    current_kpi_uid = None
    current_kpi_value = None

    for alarm in alarms:
        
        if alarm.kpi.kb_uid != current_kpi_uid: # update for the new kpi 
            current_kpi_uid = alarm.kpi.kb_uid
            current_kpi_value = get_kpi_value(current_kpi_uid)['value'][-1]
    

        if current_kpi_value <= alarm.min_value or current_kpi_value >= alarm.max_value:
            # Create an EmailMessage object
            subject = 'SmartReports Alarm Notification'
            message = f'Dear {alarm.user_type},\nThe value of {alarm.kpi.kb_name} is {current_kpi_value}.\n'

            with open(f'smartreport_app/email_body.html', 'r') as f:
                message += f.read()

            
            for email_address in Email.objects.get(user_type=alarm.user_type).emails:
                email = EmailMessage(
                    subject = subject,
                    body = message,
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    to = [email_address],
                    reply_to = [settings.DEFAULT_FROM_EMAIL],
                )
                email.content_subtype = 'html'
                
                print(f'sending mail for {current_kpi_uid} to {email_address}')
                # Send the email
                print(f'Success: {email.send()== 1}')


def mail_final_presentation():
    from email.mime.image import MIMEImage
    from django.core.mail import EmailMultiAlternatives


    subject = 'Reporting on wearable device'
    body_html = '''
            <html>
                <body>
                    <p>Dear Sandra,</p>
                    <p>We regret to inform you that there seems to be an issue with the wearable device n°1234. </p>
                    <p>We encourage you to contact the doctor and to check the functioning of the device through your dashboard or the virtual assistant. </p>
                    <p>Kind regards,<br>The Smartreports team</p>
                    <img src="cid:yellow.png" width="300" />
                </body>
            </html>
            '''

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(
        subject,
        body_html,
        from_email=from_email,
        to=['matteotolloso@gmail.com', 'f.biondi12@studenti.unipi.it'],
        # to=['f.biondi12@studenti.unipi.it'],
        # to=['p.magos@studenti.unipi.it']

    )

    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, "text/html")
    image = 'yellow.png'
    with open('/home/matteo/smartreports-backend/smartreport_app/yellow.png', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    msg.attach(img)
    print(msg.send(fail_silently=False))