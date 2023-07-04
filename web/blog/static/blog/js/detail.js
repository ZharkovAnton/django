$(function () {
  const articleDetail = new ArticleDetail()
  articleDetail.getArticleDetail()

  const commentList = new CommentList()
  commentList.getCommentList()
});

class ArticleDetail {

  generateTagsHTML(tag) {
    return `
      <a href=""><span class="badge badge-info">${tag}</span></a>
    `
  }

  generateArticleDetailHTML(article) {
    const tagsHTML = article.tags.length ? article.tags.map(tag => this.generateTagsHTML(tag)).join('') : 'no tags';
    return `
      <!-- the actual blog post: title/author/date/content -->
      <h1><a href="">${article.title}</a></h1>
      <p class="lead"><i class="fa fa-user"></i> by <a href="">${article.author.full_name}</a></p>
      <hr>
      <p><i class="fa fa-calendar"></i> ${article.updated}</p>
      <p><i class="fa fa-tags"></i> Tags: ${tagsHTML}</p>
      <hr>
      <img src="${article.image}" class="img-responsive">
      <hr>
      ${article.content}
      <br/>
      <p><h4>I like the post? Like this!</h4></p>
      <div class="g-plusone" data-annotation="inline" data-width="300" data-href=""></div>
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
    return `
      <h4><i class="fa fa-comment"></i> ${child.user} says:
      <small> ${child.updated}</small>
      </h4>
      <p>${child.content}</p>
      <hr>
      `
  }

  generateCommentListHTML(comment) {
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
        <p class="reply"><a href="#" onclick="toggleReplyForm(event, this)">Reply</a></p>
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

  getCommentList() {
    const self = this
    const slug = getSlug()
    $.ajax({
      url: `/api/v1/article/comments/${slug}`,
      type: 'GET',
      success: function (data) {
      const commentHTML = data.map(comment => {
        comment.updated = formatDate(comment.updated)
        return self.generateCommentListHTML(comment)
      }).join('');

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
