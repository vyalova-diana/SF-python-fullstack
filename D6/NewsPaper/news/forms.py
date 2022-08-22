from django.forms import ModelForm
from .models import Post, Category

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core import mail


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['type', 'category', 'title', 'content']

    def send_email(self):
        form_data = self.cleaned_data   #form validated data

        categories = form_data['category']
        recipients_list = []    #list of subscribers from all post's categories
        for cat in categories:
            recipients_list.extend(cat.subscribers.values('username', 'email'))

        messages = []   #list of all personalized EmailMultiAlternatives objects
        for recipient in recipients_list:
            html_content = render_to_string(
                'email_category_update.html',
                {
                    'news_post': form_data,
                    'username': recipient['username']
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{form_data["title"]}',
                body=f'Здравствуй, %{recipient["username"]}. Новая статья в твоём любимом разделе!',
                from_email='test.serv3r@yandex.ru',
                to=[recipient['email']]
            )
            msg.attach_alternative(html_content, "text/html")
            messages.append(msg)

        connection = mail.get_connection()
        connection.send_messages(messages)  #auto handled single instance connection



