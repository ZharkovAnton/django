from actions.models import EventAction


class EventService:
    def update_avatar(self, user):
        EventAction.objects.create(user=user, name='update_avatar')

    def create_article(self, user):
        EventAction.objects.create(user=user, name='create_article')
