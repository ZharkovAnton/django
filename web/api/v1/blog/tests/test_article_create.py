from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from blog.models import Article

from api.v1.blog.tests.conftest import locmem_email_backend

import re

import pytest

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@locmem_email_backend
@pytest.mark.parametrize(
    ['language', 'text'],
    [
        ('ru',
            '''
            <p>
                На сайте создана новая статья Title1. Пожалуйста, проверьте ее и либо активируйте либо удалите.
                Нажмите на кнопку для модерации, если вы не видите ее, пожалуйста, нажмите на
                <a href="http://localhost:8000/admin/blog/article/1/change"> ссылку.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/1/change">Редактировать</a>
                </button>
            </p>
            '''
        ),
        ('en',
            '''
            <p>
                A new article  Title1 has been created on the website. Please moderate it and activate or delete it.
                Click on the button to moderate, if you do not see it please click on the
                <a href="http://localhost:8000/admin/blog/article/2/change"> link.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/2/change">Moderate</a>
                </button>
            </p>
            '''
        ),
        ('es',
            '''
            <p>
                Se ha creado un nuevo artículo Title1 en el sitio web. Por favor, modérelo y actívelo o elimínelo.
                Haga clic en el botón para moderar, si no lo ve por favor haga clic en el botón
                <a href="http://localhost:8000/admin/blog/article/3/change"> enlace.</a>
                <button class="btn btn-lg btn-primary btn-block signup-btn" type="button">
                    <a href="http://localhost:8000/admin/blog/article/3/change">Moderado</a>
                </button>
            </p>
            '''
        )
    ]
    )
def test_article_create(api_client, category, language, text):

    url = reverse('api:v1:blog:article-create')
    # with open('/web/media/articles/hqdefault_live.png', 'rb') as image_file:
    #     file = {'image': image_file} не получается передать картинку
    data = {
        'title': 'Title1',
        'category': category.slug,
        'content': 'Content'
    }

    headers = {
        'Accept-Language': language,
    }

    response = api_client.post(url, data=data, format='multipart/form-data', headers=headers)
    assert response.status_code == 200

    article = Article.objects.get(title='Title1')
    assert article.status == False
    assert len(mail.outbox) == 2

    email_message = str(mail.outbox[0].message())
    link_moderate_article = re.search(r'href=[\"]?([^\">]+)', email_message)[1]
    assert link_moderate_article == f'http://localhost:8000/admin/blog/article/{article.id}/change'

    body_message = re.findall(r'<body>(.*?)<\/body>', email_message, re.DOTALL)[0]
    assert body_message
    assert ''.join(body_message.split()) == ''.join(text.split())


