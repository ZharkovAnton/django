from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from actions.services import EventService
from blog.models import Article

User = get_user_model()


@receiver(post_save, sender=User)
def update_avatar(sender, instance, update_fields, **kwargs):
    # TODO: посмотреть в чем проблема если убрать if update_fields
    if update_fields and 'avatar' in update_fields:
        service = EventService()
        service.update_avatar(instance)


@receiver(post_save, sender=Article)
def create_article(sender, instance, **kwargs):
    if kwargs['created']:
        service = EventService()
        service.create_article(instance.author)
