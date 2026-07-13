import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_html_email(
    subject,
    template_name,
    context,
    recipient_list,
    reply_to=None,
):

    try:

        html_message = render_to_string(
            template_name,
            context,
        )

        try:

            text_message = render_to_string(
                template_name.replace(".html", ".txt"),
                context,
            )

        except TemplateDoesNotExist:

            text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(

            subject=subject,

            body=text_message,

            from_email=settings.DEFAULT_FROM_EMAIL,

            to=recipient_list,

            reply_to=reply_to or [],

        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send(fail_silently=False)

        return True

    except Exception:

        logger.exception("Email Sending Failed")

        return False