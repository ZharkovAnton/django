from django.db.models.signals import pre_save
from django.dispatch import receiver
from blog.models import Article
from api.v1.blog.services import EmailStatusArticleHandler

@receiver(pre_save, sender=Article)
def send_email_article_status(sender, instance, **kwargs):
    if instance.pk:
        original = sender.objects.get(pk=instance.pk)
        if original.status != instance.status:
            service = EmailStatusArticleHandler(instance)
            service.send_email()
