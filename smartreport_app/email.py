from django.core.mail import EmailMessage
from django.conf import settings
from django.forms import ValidationError
from .models import UserType, ArchivedReport, Email, Alarm
from .sync_db_kb import get_kpi_value

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
                    for email_instance in email_instances:
                        # Create an EmailMessage object
                        subject = 'Subject of your email'
                        message = 'Body of your email'
                        email = EmailMessage(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            email_instance.emails,
                            reply_to=[settings.DEFAULT_FROM_EMAIL],
                        )

                        # Get the file content from the ArchivedReport
                        file_content = report.file.read()

                        # Attach the file to the email
                        email.attach(report.file.name, file_content, 'application/octet-stream')

                        # Send the email
                        email.send()

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
            current_kpi_value = get_kpi_value(current_kpi_uid)
    

        if current_kpi_value <= alarm.min_value or current_kpi_value >= alarm.max_value:
            # Create an EmailMessage object
            subject = 'SmartReports Alarm'
            message = f'The value of {alarm.kpi.kb_name} is {current_kpi_value}.'
            email = EmailMessage(
                subject = subject,
                body = message,
                from_email = settings.DEFAULT_FROM_EMAIL,
                to = Email.objects.get(user_type=alarm.user_type).emails,
                reply_to = [settings.DEFAULT_FROM_EMAIL],
            )
            print(subject, message, settings.DEFAULT_FROM_EMAIL, Email.objects.get(user_type=alarm.user_type).emails, [settings.DEFAULT_FROM_EMAIL], sep='\n' )

            print(f'sending mail for {current_kpi_uid} to {Email.objects.get(user_type=alarm.user_type).emails}')

            # Send the email
            print(f'Success: {email.send()== 1}')

