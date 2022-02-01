from django.shortcuts import redirect
from django.contrib import messages

# Sendgrid
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(request, email, subject, html_content):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e)
        messages.error(request, 'Could not send confirmation email!')
        return redirect(f'{request.path_info}/')