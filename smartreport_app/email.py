from django.core.mail import EmailMessage
from django.conf import settings
from .models import UserType, ArchivedReport, Email, ReportTemplate

def send_emails_for_unsent_reports():
    # Get distinct user types from UserType enumeration
    user_types = [user_type[0] for user_type in UserType.choices]

    for user_type in user_types:
        try:
            # Get the unsent ArchivedReport instances for the user type
            unsent_reports = ArchivedReport.objects.filter(
                user_type=user_type, sent=False
            )

            # Get the corresponding Email instance for the user type
            email_instance = Email.objects.get(user_type=user_type)

            # Validate that emails field is a list
            if not isinstance(email_instance.emails, list):
                raise ValidationError("Emails must be a list")

            # Iterate over each unsent report and send an email for each file
            for report in unsent_reports:
                # Check if the report template matches the user's template
                if report.template.user_type == user_type:
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

# Example usage:
send_emails_for_unsent_reports()
