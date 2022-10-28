from django.forms import ModelForm
from .models import Post, Subscribers, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post_text', 'author', 'post_category']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class SubscribeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.get('prefix')
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(subscriber=user.id)

    class Meta:
        model = Subscribers
        fields = [
            'category',
        ]
