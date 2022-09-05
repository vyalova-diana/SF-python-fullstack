from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import OneTimeCode
import random


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='Common')
        basic_group.user_set.add(user)

        OneTimeCode.objects.create(code=''.join(random.sample('1234567890', 4)), user=user)
        return user
