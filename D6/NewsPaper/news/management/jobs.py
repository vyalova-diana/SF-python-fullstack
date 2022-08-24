from datetime import date, timedelta
from news.models import Post, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core import mail


def weekly_category_email():
    today_date = date.today()
    week = timedelta(weeks=1)
    week_start_date = today_date - week

    categories = Category.objects.all()
    messages = []  # list of all personalized EmailMultiAlternatives objects
    for cat in categories:
        recipients_list = cat.subscribers.values('username', 'email')
        news_list = cat.post_set.filter(date__date__gte=week_start_date, type='NW').values('id', 'title')
        if len(news_list) != 0:
            for recipient in recipients_list:
                html_content = render_to_string(
                    'news/email_category-weekly_digest.html',
                    {
                        'news_list': news_list,
                        'username': recipient['username'],
                        'category': cat.name
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'{cat.name} weekly digest',
                    body=f'Здравствуй, {recipient["username"]}. Вот список статей за неделю в категории #{cat.name} !',
                    from_email='test.serv3r@yandex.ru',
                    to=[recipient['email']]
                )
                msg.attach_alternative(html_content, "text/html")
                messages.append(msg)

    connection = mail.get_connection()
    connection.send_messages(messages)  # auto handled single instance connection
    print("Job DONE!!!!")
