import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.utils.html import strip_tags

from blog.choices import ArticleStatus
from blog.models import Article
from conftest import locmem_email_backend

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@locmem_email_backend
@pytest.mark.parametrize(
    ['language', 'text_admin', 'text_user'],
    [
        (
            'ru',
            '''
            <p>
                На сайте создана новая статья Title1. Пожалуйста, проверьте ее и либо активируйте либо удалите.
                Нажмите на кнопку для модерации, если вы не видите ее, пожалуйста, нажмите на
                <a href="http://localhost:8000/admin/blog/article/1/change"> ссылку.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/1/change" style="color:white">Редактировать</a>
                </button>
            </p>
            ''',
            '''
            <p>
                Ваша статья находится на модерации. После она будет доступна
            </p>
            ''',
        ),
        (
            'en',
            '''
            <p>
                A new article  Title1 has been created on the website. Please moderate it and activate or delete it.
                Click on the button to moderate, if you do not see it please click on the
                <a href="http://localhost:8000/admin/blog/article/2/change"> link.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/2/change" style="color:white">Moderate</a>
                </button>
            </p>
            ''',
            '''
            <p>
                Your article has been submitted for moderation. Then it will be available
            </p>
            ''',
        ),
        (
            'es',
            '''
            <p>
                Se ha creado un nuevo artículo Title1 en el sitio web. Por favor, modérelo y actívelo o elimínelo.
                Haga clic en el botón para moderar, si no lo ve por favor haga clic en el botón
                <a href="http://localhost:8000/admin/blog/article/3/change"> enlace.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/3/change" style="color:white">Moderado</a>
                </button>
            </p>
            ''',
            '''
            <p>
                Su artículo ha sido sometido a moderación. Entonces estará disponible
            </p>
            ''',
        ),
    ],
)
def test_article_create(api_client, category, language, text_admin, text_user, image_content_file):
    url = reverse('api:v1:blog:article-create')

    data = {'title': 'Title1', 'category': category.slug, 'content': 'Content', 'image': image_content_file}

    headers = {
        'Accept-Language': language,
    }

    response = api_client.post(url, data=data, format='multipart/form-data', headers=headers)
    assert response.status_code == 200

    article = Article.objects.get(title='Title1')
    assert article.image
    assert article.status == ArticleStatus.INACTIVE
    assert len(mail.outbox) == 2

    email_admin_message = str(mail.outbox[0].message())
    link_moderate_article = re.search(r'<p>.*?<a\s+href="(.*?)">', email_admin_message, re.DOTALL)[1]
    assert link_moderate_article == f'http://localhost:8000/admin/blog/article/{article.id}/change'

    body_admin_message = re.findall(r'<body>(.*?)<\/body>', email_admin_message, re.DOTALL)[0]
    assert body_admin_message
    assert ''.join(body_admin_message.split()) == ''.join(text_admin.split())

    email_user_message = str(mail.outbox[1].message())
    body_user_message = re.findall(r'<body>(.*?)<\/body>', email_user_message, re.DOTALL)[0]
    assert body_user_message
    assert ''.join(body_user_message.split()) == ''.join(text_user.split())
