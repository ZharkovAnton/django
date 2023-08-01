$(function () {
  const articleDetail = new ArticleDetail()
  articleDetail.getArticleDetail()

  const commentList = new CommentList()
  commentList.getCommentList()
});

let pageNumber = 0

class ArticleDetail {

  generateTagsHTML(tag) {
    return `
      <a href=""><span class="badge badge-info">${tag}</span></a>
    `
  }

  generateArticleDetailHTML(article) {
    const tagsHTML = article.tags.length ? article.tags.map(tag => this.generateTagsHTML(tag)).join('') : 'no tags';
    const spanNavbar = document.querySelector('span.navbar-brand');
    const aTags = spanNavbar.querySelectorAll('a')
    const lastElement = aTags[aTags.length - 1];
    const userId = parseInt(lastElement.getAttribute('data-userId'));
    return `
      <!-- the actual blog post: title/author/date/content -->
      <h1><a href="">${article.title}</a></h1>
      <p class="lead"><i class="fa fa-user"></i> by <a href="">${article.author.full_name}</a></p>
      <hr>
      <p><i class="fa fa-calendar"></i> ${article.updated}</p>
      <p><i class="fa fa-tags"></i> Tags: ${tagsHTML}</p>
      <hr>
      <img src="${article.image}" class="img-responsive" width="140" height="110">
      <hr>
      ${article.content}
      <br/>
      <p>
      <a class="btn btn-read-more" href="${ article.url }">Read more</a>
      <a href="#" id="like" data-model="Article" data-objectid="${article.id}" data-type=1 onclick="likeDislike(event, this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${article.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'green' : 'black'}" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16">
          <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
        </svg>
      </a> <span id="article_${article.id}">${article.count_like_dislike > 0 ? article.count_like_dislike : 0}</span>
      <a href="#" id="dislike" data-model="Article" data-objectid="${article.id}" data-type=-1 onclick="likeDislike(event, this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${article.votes.find(vote => vote.user === userId && vote.vote === -1) ? 'red' : 'black'}" class="bi bi-hand-thumbs-down-fill" viewBox="0 0 16 16">
          <path d="M6.956 14.534c.065.936.952 1.659 1.908 1.42l.261-.065a1.378 1.378 0 0 0 1.012-.965c.22-.816.533-2.512.062-4.51.136.02.285.037.443.051.713.065 1.669.071 2.516-.211.518-.173.994-.68 1.2-1.272a1.896 1.896 0 0 0-.234-1.734c.058-.118.103-.242.138-.362.077-.27.113-.568.113-.856 0-.29-.036-.586-.113-.857a2.094 2.094 0 0 0-.16-.403c.169-.387.107-.82-.003-1.149a3.162 3.162 0 0 0-.488-.9c.054-.153.076-.313.076-.465a1.86 1.86 0 0 0-.253-.912C13.1.757 12.437.28 11.5.28H8c-.605 0-1.07.08-1.466.217a4.823 4.823 0 0 0-.97.485l-.048.029c-.504.308-.999.61-2.068.723C2.682 1.815 2 2.434 2 3.279v4c0 .851.685 1.433 1.357 1.616.849.232 1.574.787 2.132 1.41.56.626.914 1.28 1.039 1.638.199.575.356 1.54.428 2.591z"/>
        </svg>
      </a>
    </p>
      <br/>
      <hr>
      <div class="well comment">
        <h4><i class="fa fa-paper-plane-o"></i><a href="#" onclick="toggleReplyForm(event, this)"> Comments on the article</a></h4>
        <div class="replyForm" style="display: none;">
          <form class="replyForm" onsubmit="submitReply(event, this)" action="">
            <textarea class="summernote"></textarea>
            <button type="submit" class="btn btn-primary"><i class="fa fa-reply"></i> Submit</button>
          </form>
        </div>
      </div>
      <hr>
    </div>`;
  }

  getArticleDetail() {
    const self = this;
    const slug = getSlug()
    $.ajax({
      url: `/api/v1/article/${slug}`,
      type: 'GET',
      success: function (data) {
      data.updated = formatDate(data.updated)
      const articleHTML = self.generateArticleDetailHTML(data)
      const divCollg8 = document.querySelector('div.col-lg-8')
      divCollg8.insertAdjacentHTML('afterbegin', articleHTML);
      },
      error: function (data) {
      alert('bad')
      }
  })
  }
}

class CommentList{
  generateСhildHTML(child) {
    const userId = get_userId()
    return `
      <h4><i class="fa fa-comment"></i> ${child.user} says:
      <small> ${child.updated}</small>
      </h4>
      <p>${child.content}</p>
      <p class="reply"><a href="#" onclick="toggleReplyForm(event, this)">Reply</a>
      <a href="#" id="like" data-model="Comment" data-objectid="${child.id}" data-type=1 onclick="likeDislike(event, this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${child.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'red':'black'}" class="${child.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'bi bi-suit-heart-fill' : 'bi bi-suit-heart'} viewBox="0 0 16 16">
          <path d="${child.votes.find(vote => vote.user === userId && vote.vote === 1) ? `M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0
          3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z`:`m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2
          2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446
          6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784
          0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281
          2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z`}"/>
        </svg>
      </a> <span id="comment_${child.id}">${child.count_like}</span>
      </p>
      <hr>
      `
  }

  generateCommentListHTML(comment) {
    const userId = get_userId()
    if (comment.children!=false) {
      const childHTML = comment.children.map(child => {
        child.updated = formatDate(child.updated)
        return this.generateСhildHTML(child)
      }).join('')
      return `
      <div class="comment">
        <h3><i class="fa fa-comment"></i> ${comment.user} says:
        <small> ${comment.updated}</small>
        </h3>
        <p>${comment.content}</p>
        <p class="reply"><a href="#" onclick="toggleReplyForm(event, this)">Reply</a>
        <a href="#" id="like" data-model="Comment" data-objectid="${comment.id}" data-type=1 onclick="likeDislike(event, this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'red':'black'}" class="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'bi bi-suit-heart-fill' : 'bi bi-suit-heart'} viewBox="0 0 16 16">
            <path d="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? `M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0
            3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z`:`m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2
            2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446
            6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784
            0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281
            2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z`}"/>
          </svg>
        </a> <span id="comment_${comment.id}">${comment.count_like}</span>
        </p>
        <div class="replyForm" style="display: none;">
          <form class="replyForm" onsubmit="submitReply(event, this)" action="">
            <textarea class="summernote"></textarea>
            <button type="submit" class="btn btn-primary" value="${comment.id}><i class="fa fa-reply"></i> Submit</button>
          </form>
        </div>
        <hr>
        <div style="margin-left: 40px;">
        ${childHTML}
        </div>
      </div>
      `
    } else {
      return `
      <div class="comment">
        <h3><i class="fa fa-comment"></i> ${comment.user} says:
        <small> ${comment.updated}</small>
        </h3>
        <p>${comment.content}</p>
        <p class="reply"><a href="#" onclick="toggleReplyForm(event, this)">Reply</a></p>
        <a href="#" id="comment_like" data-model="Comment" data-objectid="${comment.id}" data-type=1 onclick="likeDislike(event, this)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'red':'black'}" class="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? 'bi bi-suit-heart-fill' : 'bi bi-suit-heart'} viewBox="0 0 16 16">
            <path d="${comment.votes.find(vote => vote.user === userId && vote.vote === 1) ? `M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0
            3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z`:`m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2
            2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446
            6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784
            0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281
            2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z`}"/>
          </svg>
        </a> <span id="comment_${comment.id}">${comment.count_like}</span>
        <div class="replyForm" style="display: none;">
          <form class="replyForm" onsubmit="submitReply(event, this)" action="">
            <textarea class="summernote"></textarea>
            <button type="submit" class="btn btn-primary" value="${comment.id}"><i class="fa fa-reply"></i> Submit</button>
          </form>
        </div>
      </div>
      <hr>
      `
    }
  }

  getCommentList(page=null) {
    const self = this
    const slug = getSlug()
    let url = `/api/v1/article/comments/${slug}/`
    if (page) {
      url += `?page=${page}`
    }
    $.ajax({
      url: url,
      type: 'GET',
      success: function (data) {
        const commentHTML = data.results.map(comment => {
          comment.updated = formatDate(comment.updated)
          return self.generateCommentListHTML(comment)
        }).join('');

        if (data.next != null) {
          pageNumber = data.next[data.next.indexOf('page=')+5]
        } else {
          pageNumber = null
        }

        const divCollg8 = document.querySelector('div.col-lg-8')
        divCollg8.insertAdjacentHTML('beforeend', commentHTML);

      },
      error: function (data) {
      alert('bad')
      }
    })
  }
}

function formatDate(data_date) {
  const date = new Date(data_date);

  const options = {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  };

  return date.toLocaleString('en-US', options);
}

function getSlug() {
  const {href} = window.location;
  const arr = href.split("/");
  return arr[arr.length - 2];
}

function toggleReplyForm(event, replyLink) {
  const $comment = $(replyLink).closest('.comment');
  const $replyForm = $comment.find('.replyForm');

  if ($replyForm.is(':visible')) {
    hideReplyForm($replyForm);
  } else {
    showReplyForm($replyForm);
  }

  event.preventDefault();
}

function showReplyForm($replyForm) {
  $replyForm.show();
  $replyForm.find('.summernote').summernote({placeholder: 'Write your comment ...', height: 120});
}

function hideReplyForm($replyForm) {
  $replyForm.hide();
  $replyForm.find('.summernote').summernote('destroy');
}

function submitReply(event, replyForm) {
  event.preventDefault();
  const form = $(replyForm);
  const content = form[0][0].value
  const article = getSlug()
  const parent = parseInt(form[0][207].value) || ''
  $.ajax({
    url: '/api/v1/article/comment/create/',
    type: 'POST',
    dataType: 'json',
    data: {
      'content': content,
      'parent': parent,
      'article': article
    },
    success: function (data) {
      location.reload()
    },
    error: function (data) {
      console.log(data);
    },
  })
}

window.addEventListener('scroll', () => {
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight && pageNumber) {
    const comm = new CommentList()
    comm.getCommentList(pageNumber)
  }
});

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
      if (model === 'Article') {
        const svgA = divRow.querySelector(`#${searchId}`).querySelector('svg')
        const spanNumLike = divRow.querySelector(`#article_${objectId}`)
        spanNumLike.textContent = data.sum_likes > 0 ? data.sum_likes : 0

        if (svgElement.getAttribute('fill') === 'black' && type === 1) {
          svgElement.setAttribute('fill', 'green');
          svgA.setAttribute('fill', 'black');
        } else if (svgElement.getAttribute('fill') === 'black' && type === -1) {
          svgElement.setAttribute('fill', 'red');
          svgA.setAttribute('fill', 'black');
        } else {
          svgElement.setAttribute('fill', 'black');
        }
      } else if (model === 'Comment') {
        const spanNumLike = divRow.querySelector(`#comment_${objectId}`)
        spanNumLike.textContent = data.sum_likes
        if (svgElement.getAttribute('fill') === 'red'){
          svgElement.setAttribute('fill', 'black')
          svgElement.setAttribute('class', 'bi bi-suit-heart')
          svgElement.innerHTML = '<path d="m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2 2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446 6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z"/>'
        } else {
          svgElement.setAttribute('fill', 'red')
          svgElement.setAttribute('class', 'bi bi-suit-heart-fill')
          svgElement.innerHTML = '<path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>'
        }
      }

    },
    error: function (data) {
    alert('bad')
    }
  })
}

function get_userId() {
  const spanNavbar = document.querySelector('span.navbar-brand');
    const aTags = spanNavbar.querySelectorAll('a')
    const lastElement = aTags[aTags.length - 1];
    return parseInt(lastElement.getAttribute('data-userId'));
}

