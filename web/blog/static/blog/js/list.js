$(function () {
  const url = new URL(window.location.href)
  params = url.search
  if (params) {
    getArticleList(params)
  } else {
    getArticleList()
  }

});

// TODO: переписать код и убрать лайки

function getArticleList(params='?page=1') {
  let url = '/api/v1/article/' + params
  const newURL = new URL(window.location.href)
  newURL.search = `${params}`
  window.history.replaceState({ path: newURL.href }, "", newURL.href)
  $.ajax({
    url: '/api/v1/article/tag/',
    type: 'GET',
    success: function (tags) {
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
    error: function (response) {
      alert('bad')
      }
            })
          }
        })

}

const generateTagsSideBar = (tags) => {
  let tagsHTML = tags.map(tag => {return `<li><a href=""><span class="badge badge-info tags">${tag.name}</span></a></li>`})
  const tagsCol1HTML = tagsHTML.slice(0,4).join('')
  const tagsCol2HTML = tagsHTML.slice(4,7).join('')

  const ulList1 = document.querySelector('#list-1')
  const ulList2 = document.querySelector('#list-2')

  ulList1.insertAdjacentHTML('afterbegin', tagsCol1HTML)
  ulList2.insertAdjacentHTML('afterbegin', tagsCol2HTML)
}

const generatePostList = (article) => {
  let tagLinks = 'no tags'
  if (article.tags.length!==0) {
    tagLinks = article.tags.map(tag => `<a href="#"><span class="label label-info tags">${tag}</span></a>`).join('');
  }
  const spanNavbar = document.querySelector('span.navbar-brand');
  const aTags = spanNavbar.querySelectorAll('a')
  const lastElement = aTags[aTags.length - 1];
  const userId = parseInt(lastElement.getAttribute('data-userId'));
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
                      <a href="#" id="like" data-model="Article" data-objectid="${article.id}" data-type=1 onclick="likeDislike(event, this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${article.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'green' : 'black'}" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16">
                          <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
                        </svg>
                      </a> <span>${article.count_like_dislike > 0 ? article.count_like_dislike : 0}</span>
                      <a href="#" id="dislike" data-model="Article" data-objectid="${article.id}" data-type=-1 onclick="likeDislike(event, this)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${article.votes.find(vote => vote.user === userId && vote.vote === -1) ? 'red' : 'black'}" class="bi bi-hand-thumbs-down-fill" viewBox="0 0 16 16">
                          <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.378 1.378 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51.136.02.285.037.443.051.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.896 1.896 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2.094 2.094 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.162 3.162 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.823 4.823 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591z"/>
                        </svg>
                      </a>
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

function likeDislike (event, element) {
  event.preventDefault()
  const model = element.dataset.model
  const objectId = parseInt(element.dataset.objectid)
  const type = parseInt(element.dataset.type)
  const svgElement = element.querySelector('svg');
  const divRow = document.querySelector('div.row');
  let searchId = ''
  if (type === 1) {
    searchId = 'dislike'
  } else {
    searchId = 'like'
  }
  const svgA = divRow.querySelector(`#${searchId}`).querySelector('svg')
  console.log(svgA)

  if (svgElement.getAttribute('fill') === 'black' && type === 1) {
    svgElement.setAttribute('fill', 'green');
    svgA.setAttribute('fill', 'black');
  } else if (svgElement.getAttribute('fill') === 'black' && type === -1) {
    svgElement.setAttribute('fill', 'red');
    svgA.setAttribute('fill', 'black');
  } else {
    svgElement.setAttribute('fill', 'black');
  }
  const data = {
    model: model,
    object_id: objectId,
    vote_type: type
  }
  const jsonData = JSON.stringify(data)
  $.ajax({
    url: `/api/v1/actions/`,
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: jsonData,
    success: function (data) {
      console.log(data)
    },
    error: function (data) {
    alert('bad')
    }
  })
}
