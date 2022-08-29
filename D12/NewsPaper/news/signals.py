from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core import mail


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers_category_update(sender, instance, **kwargs):
    if instance.type == 'NW':
        categories = instance.category.all()

        recipients_list = []  # list of subscribers from all post's categories
        for cat in categories:
            recipients_list.extend(cat.subscribers.values('username', 'email'))

        messages = []  # list of all personalized EmailMultiAlternatives objects
        for recipient in recipients_list:
            html_content = render_to_string(
                'news/email_category_update.html',
                {
                    'news_post': instance,
                    'username': recipient['username']
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=f'Здравствуй, %{recipient["username"]}. Новая статья в твоём любимом разделе!',
                from_email='test.serv3r@yandex.ru',
                to=[recipient['email']]
            )
            msg.attach_alternative(html_content, "text/html")
            messages.append(msg)

        connection = mail.get_connection()
        connection.send_messages(messages)  # auto handled single instance connection


