class TagsAll {
  getTags() {
    $.ajax({
      url: '/api/v1/article/tag/',
      type: 'GET',
      success: function (data) {
        generateTagsSideBar(data);
      },
      error: function (data) {
        alert('bad')
      }
    })
  }

  generateTagsSideBar(data) {
    let tagsHTML = data.map(tag => {return `<li><a href=""><span class="badge badge-info tags">${tag.name}</span></a></li>`})
    const tagsCol1HTML = tagsHTML.slice(0,4).join('')
    const tagsCol2HTML = tagsHTML.slice(4,7).join('')

    const ulList1 = document.querySelector('#list-1')
    const ulList2 = document.querySelector('#list-2')

    ulList1.insertAdjacentHTML('afterbegin', tagsCol1HTML)
    ulList2.insertAdjacentHTML('afterbegin', tagsCol2HTML)
  }
}

class ArticleList {
  getArticleList(params='?page=1') {
    let url = '/api/v1/article/' + params
    const newURL = new URL(window.location.href)
    newURL.search = `${params}`
    window.history.replaceState({ path: newURL.href }, "", newURL.href)
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
          generateTagsSideBar(tags)
          if (response.count === 0) {
            const emptyListHTML = emptyList()
            const divRow = document.querySelector('div.row')
            document.querySelectorAll('.col-lg-8, .pagination').forEach(elem => elem.remove());
            divRow.insertAdjacentHTML('beforeend', emptyListHTML);
          } else {
            const results = response.results;
            // форматируем дату
            results.forEach(function (article) {
              const date = new Date(article.updated)
              const options = { month: 'long', day: 'numeric', year: 'numeric' };
              const updatedFormatted = date.toLocaleDateString('en-US', options);
              const timeOptions = { hour: 'numeric', minute: 'numeric', hour12: true };
              const timeFormatted = date.toLocaleTimeString('en-US', timeOptions);
              const formattedDate = `${updatedFormatted} at ${timeFormatted}`;
              article.updated = formattedDate
            })

            // генерируем HTML для всех постов
            const articlesHTML = results.map(article => {
                return generatePostList(article)
            }).join('')


            // вставляем полученный код на страницу
            const divRow = document.querySelector('div.row')
            document.querySelectorAll('.col-lg-8, .pagination').forEach(elem => elem.remove());
            divRow.insertAdjacentHTML('beforeend', articlesHTML);

            // создаем кнопки переключения назад вперед
            const paginationDiv = document.createElement('div')
            paginationDiv.classList.add('pagination')

            buttonsHTML = ''
            if (response.previous) {
                buttonsHTML += `<button class="btn btn-secondary previous-page">Previous</button>`
            }
            if (response.next) {
                buttonsHTML += `<button class="btn btn-secondary next-page">Next</button>`;
            }
            paginationDiv.innerHTML = buttonsHTML;
            divRow.appendChild(paginationDiv);

            // вешаем обработчик событий и вызываем функцию getArticleList со слагом
            const previousButton = document.querySelector('.previous-page');
            const nextButton = document.querySelector('.next-page');

            if (nextButton) {
              nextButton.addEventListener('click', () => {
                url = response.next
                const params = url.substring(url.indexOf('?'));
                getArticleList(params);
              });
            }
            if (previousButton) {
              previousButton.addEventListener('click', () => {
                url = response.previous
                const params = url.substring(url.indexOf('?'));
                if (url.indexOf('?') !== -1) {
                  getArticleList(params)
                } else {
                  getArticleList()
                }
              });
            }
          }
        },
        error: function (response) {
        alert('bad')
        },
      })
    }
  }



  const generatePostList = (article) => {
    let tagLinks = 'no tags'
    if (article.tags.length!==0) {
      tagLinks = article.tags.map(tag => `<a href="#"><span class="label label-info tags">${tag}</span></a>`).join('');
    }
    return `
          <div class="col-lg-8">
            <div class="row">
              <div class="col-md-12 post">
                <div class="row">
                  <div class="col-md-12">
                      <h4>
                      <strong>
                          <a href="${ article.url }" class="post-title">${ article.title }</a>
                      </strong>
                      </h4>
                  </div>
                  </div>
                  <div class="row">
                  <div class="col-md-12 post-header-line">
                      <span class="glyphicon glyphicon-user"></span>by <a href="#">${ article.author.full_name }</a> |
                      <span class="glyphicon glyphicon-calendar"></span> ${ article.updated } |
                      <span class="glyphicon glyphicon-comment"></span><a href="#">${ article.comments_count } Comments</a> |
                      <i class="icon-share"></i><a href="#">39 Shares</a> |
                      <span class="glyphicon glyphicon-tags"></span> Tags: ${tagLinks}
                  </div>
                  </div>
                  <div class="row post-content">
                  <div class="col-md-3">
                      <a href="#">
                      <img
                          src="http://4.bp.blogspot.com/-_lqoNpVXeU4/UkxQ7N-QW8I/AAAAAAAACTw/pni-TZyp17o/s1600/cool+share+button+effects+styles.png"
                          alt="" class="img-responsive">
                      </a>
                  </div>
                  <div class="col-md-9">
                      <p>
                      ${ article.content }
                      </p>
                      <p>
                      <a class="btn btn-read-more" href="${ article.url }">Read more</a>
                      </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          `
      }

  const searchBTN = document.querySelector('#search-btn')
  searchBTN.addEventListener('click', () => {
    const queryParam = '?search=' + document.querySelector('#search').value
    getArticleList(page=queryParam)
  })

  const emptyList = () => {
    return `
    <div class="col-lg-8">
      <div class="row">
        <p>No results were found for your query.</p>
      </div>
    </div>`
  }
