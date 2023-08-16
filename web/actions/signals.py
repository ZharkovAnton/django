from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from actions.services import EventService
from blog.models import Article

User = get_user_model()


@receiver(post_save, sender=User)
def update_avatar(sender, instance, **kwargs):
    if 'avatar' in kwargs['update_fields']:
        service = EventService()
        service.update_avatar(instance)

@receiver(post_save, sender=Article)
def create_article(sender, instance, **kwargs):
    if kwargs['created']:
        service = EventService()
        service.create_article(instance.author)
