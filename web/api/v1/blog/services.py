from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.db.models import Count, F
from django.utils.translation import gettext_lazy as _

from api.email_services import BaseEmailHandler
from blog.choices import ArticleStatus
from blog.models import Article, Category, Comment

from main.models import UserType


class BlogService:
    @staticmethod
    def category_queryset():
        return Category.objects.all()

    @staticmethod
    def get_active_articles():
        return (
            Article.objects.filter(status=ArticleStatus.ACTIVE)
            .annotate(comments_count=Count('comment_set'))
            .order_by(F('created').asc())
        )


class CreateArticleService:
    def get_category(self, category_name: str):
        return Category.objects.get(
            name=category_name
        )  # в valid_data находится объект Category, почему срабатывает поиск name= Category object

    def create_article(self, data: dict, user: UserType):
        category = self.get_category(data['category'])  # я так понимаю это уже можно удалить

        image = data.get('image', '')

        article = Article.objects.create(
            title=data['title'], category=data['category'], content=data['content'], image=image, author=user
        )

        return article


class CreateCommentService:
    def create_comment(self, data: dict, user: UserType):
        return Comment.objects.create(
            author=user.email, user=user, content=data['content'], article=data['article'], parent=data['parent']
        )


class EmailCreateArticleAdminHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    TEMPLATE_NAME = 'email/blog/created-article-admin-email.html'

    def __init__(self, data, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article = data
        self.request = request  # не нужен скорее всего надо проверить
        self.FRONTEND_PATH = f'admin/blog/article/{self.article.id}/change'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        return f'{url}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('New article %(article_title)s.') % {'article_title': self.article.title},
            'to_email': settings.SUPERUSER_EMAIL,
            'context': {
                'article_title': self.article.title,
                'activate_url': self._get_activate_url(),
            },
        }


class EmailCreateArticleUserHandler(BaseEmailHandler):
    TEMPLATE_NAME = 'email/blog/created-article-user-email.html'

    def email_kwargs(self, **kwargs) -> dict:
        return {'subject': _('New article moderation'), 'to_email': self.user, 'context': {}}


class EmailStatusArticleHandler(BaseEmailHandler):
    TEMPLATE_NAME = 'email/blog/status-article-email.html'

    def __init__(self, obj: Article, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article = obj

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Article status'),
            'to_email': self.article.author.email,
            'context': {
                'status': self.article.status,
                'title': self.article.title,
            },
        }
