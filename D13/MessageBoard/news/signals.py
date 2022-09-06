from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core import mail
from django.contrib.auth.models import User
from django.conf import settings


@receiver(post_save, sender=News)
def news_update_notify_users(sender, instance, created, **kwargs,):
    if created:

        recipients_list = User.objects.filter(is_active=True).values('username', 'email')

        messages = []  # list of all personalized EmailMultiAlternatives objects
        for recipient in recipients_list:
            html_content = render_to_string(
                'news/email/email_news_update.html',
                {
                    'news_post': instance,
                    'username': recipient['username']
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=f'Здравствуй, %{recipient["username"]}. Новая статья в разделе "Новости"!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient['email']]
            )
            msg.attach_alternative(html_content, "text/html")
            messages.append(msg)

        connection = mail.get_connection()
        connection.send_messages(messages)  # auto handled single instance connection


