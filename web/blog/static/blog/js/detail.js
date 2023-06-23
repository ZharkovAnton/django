$(function () {
  const articleDetail = new ArticleDetail()
  articleDetail.getArticleDetail()
});

class ArticleDetail {

  getSlug() {
    const href = window.location.href
    const arr = href.split("/");
    const slug = arr[arr.length - 2];
    return slug
  }

  generateArticleDetailHTML(article) {
    return `
    <div class="col-lg-8">
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
    </div>
    `
  };

  getArticleDetail() {
    const self = this;
    const slug = this.getSlug()
    $.ajax({
      url: `/api/v1/article/${slug}`,
      type: 'GET',
      success: function (response) {
      response = self.formatDate(response)
      const articleHTML = self.generateArticleDetailHTML(response)
      const divRow = document.querySelector('div.row')
      divRow.insertAdjacentHTML('beforeend', articleHTML);
      },
      error: function (response) {
      alert('bad')
      }
  })
  }

  formatDate(response) {
    const date = new Date(response.updated)
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    const updatedFormatted = date.toLocaleDateString('en-US', options);
    const timeOptions = { hour: 'numeric', minute: 'numeric', hour12: true };
    const timeFormatted = date.toLocaleTimeString('en-US', timeOptions);
    const formattedDate = `${updatedFormatted} at ${timeFormatted}`;
    response.updated = formattedDate
    return response;
  }
}
