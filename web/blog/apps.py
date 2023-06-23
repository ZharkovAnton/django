from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        # Импортируйте сигналы для их регистрации.
        import api.v1.blog.signals
