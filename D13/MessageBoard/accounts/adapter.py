from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from.models import OneTimeCode


class MyAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        context["otp"] = OneTimeCode.objects.get(user__email=email).code
        super().send_mail(template_prefix, email, context)

