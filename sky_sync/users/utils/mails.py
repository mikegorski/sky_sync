from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def get_email_message(
    recipient_email: str,
    subject: str,
    html_template_name: str,
    user: User,
    domain: str,
) -> EmailMessage:
    message = render_to_string(
        html_template_name,
        {
            'user': user,
            'domain': domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        },
    )

    return EmailMessage(subject, message, to=[recipient_email])
