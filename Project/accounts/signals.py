from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=PostCategory)
def notify_subscriber(sender, instance, **kwargs):
    for cat in instance.post_category.all():
        subscribers = Subscribers.objects.filter(category=cat)
        for person in subscribers:
            html_content = render_to_string(
                'subscription_letter.html',
                {
                    'post': instance,
                    'person': person,
                    'cat': cat,
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.post_text,
                from_email='levinkirill@yandex.ru',
                to=[person.subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()

# @receiver(m2m_changed, sender=PostCategory)
# def notify_subscriber(sender, instance, **kwargs):
#     for cat in instance.post_category.all():
#         subscribers = Subscribers.objects.filter(category=cat)
#         for person in subscribers:
#             send_mail(
#                 f'Новая статья в категории {cat}: {instance.title}',
#                 f'{instance.post_text}',
#                 'levinkirill@yandex.ru',
#                 [person.subscriber.email],
#                 )
