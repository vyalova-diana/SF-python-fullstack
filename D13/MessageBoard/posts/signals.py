from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Post, Comment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings

@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers_category_update(sender, instance, **kwargs):

    categories = instance.category.all()

    recipients_list = []  # list of subscribers from all post's categories
    for cat in categories:
        recipients_list.extend(cat.subscribers.values('username', 'email'))

    messages = []  # list of all personalized EmailMultiAlternatives objects
    for recipient in recipients_list:
        html_content = render_to_string(
            'posts/email/email_category_update.html',
            {
                'news_post': instance,
                'username': recipient['username']
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{instance.title}',
            body=f'Здравствуй, %{recipient["username"]}. Новая статья в твоём любимом разделе!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient['email']]
        )
        msg.attach_alternative(html_content, "text/html")
        messages.append(msg)

    connection = mail.get_connection()
    connection.send_messages(messages)  # auto handled single instance connection


@receiver(post_save, sender=Comment)
def comment_added_notify_author(sender, instance, created, **kwargs,):
    if created:

        recipient = instance.post.author.user
        html_content = render_to_string(
            'posts/email/new_comment_alert.html',
            {
                'comment': instance,
                'username': recipient.username
            }
        )

        msg = EmailMultiAlternatives(
            subject='Новый комментарий',
            body=f'Здравствуй, %{recipient.username}. Вы получили новый комментарий!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient.email]
        )
        msg.attach_alternative(html_content, "text/html")

        connection = mail.get_connection()
        connection.send_messages([msg])  # auto handled single instance connection

    else:

        recipient = instance.user
        html_content = render_to_string(
            'posts/email/comment_approved_alert.html',
            {
                'comment': instance,
                'username': recipient.username
            }
        )

        msg = EmailMultiAlternatives(
            subject='Комментарий одобрен',
            body=f'Здравствуй, %{recipient.username}. Ваш комментарий одобрен!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient.email]
        )
        msg.attach_alternative(html_content, "text/html")

        connection = mail.get_connection()
        connection.send_messages([msg])  # auto handled single instance connection
