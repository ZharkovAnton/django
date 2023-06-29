$(function () {
  const articleDetail = new ArticleDetail()
  articleDetail.getArticleDetail()

  const commentList = new CommentList()
  commentList.getCommentList()

});

class ArticleDetail {

  generateArticleDetailHTML(article) {
    return `

      <!-- the actual blog post: title/author/date/content -->
      <h1><a href="">${ article.title }</a></h1>
      <p class="lead"><i class="fa fa-user"></i> by <a href="">${article.author.full_name}</a>
      </p>
      <hr>
      <p><i class="fa fa-calendar"></i>${article.updated}</p>
      <p><i class="fa fa-tags"></i> Tags: <a href=""><span class="badge badge-info">Bootstrap</span></a> <a
        href=""><span class="badge badge-info">Web</span></a> <a href=""><span class="badge badge-info">CSS</span></a>
        <a href=""><span class="badge badge-info">HTML</span></a></p>

      <hr>
      <img src="${article.image}" class="img-responsive">
      <hr>
      ${article.content}
      <br/>
      <p><h4>I like the post? Like this!</h4></p>


      <div class="g-plusone" data-annotation="inline" data-width="300" data-href=""></div>

      <br/>
      <hr>
      <div class="well">
        <h4><i class="fa fa-paper-plane-o"></i> Leave a Comment:</h4>
        <form role="form">
          <div class="form-group">
            <textarea id="summernote" name="content" class="form-control input-lg"></textarea>
          </div>
          <button type="submit" class="btn btn-primary"><i class="fa fa-reply"></i> Submit</button>
        </form>
      </div>
      <hr>
    </div>
    `
  };

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
      $('#summernote').summernote({
        placeholder: 'Write your article ...',
        height: 120,
      });
      },
      error: function (data) {
      alert('bad')
      }
  })
  }
}

class CommentList{
  generateCommentListHTML(comment) {
    return `
    <h3><i class="fa fa-comment"></i> ${comment.author} says:
    <small> ${comment.updated}</small>
    </h3>
    <p>${comment.content}</p>
    `
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
      error: function (response) {
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
