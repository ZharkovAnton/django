$(function () {
  getDetailProfile();
});

function getDetailProfile() {
  const url = new URL(window.location.href);
  const pathnameArray = url.pathname.split('/');
  const userId = pathnameArray[pathnameArray.length - 1];
  $.ajax({
    url: `/api/v1/profile/${userId}/`,
    type: "GET",
    success: function (data) {
      $('.bootstrap').empty();
      const profileHTML = generateProfileHTML(data);
      const divContainer = document.querySelector('.bootstrap');
      divContainer.insertAdjacentHTML('afterbegin', profileHTML);
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function generateProfileHTML(bioData) {
  return `
  <div class="row">
  <div class="col-sm-10"><h1>${bioData.full_name}</h1></div>
  <div class="col-sm-2"><a href="/users" class="pull-right"><img title="profile image" class="img-circle img-responsive" src="http://www.gravatar.com/avatar/28fd20ccec6865e2d5f0e1f4446eb7bf?s=100"></a></div>
</div>
<div class="row">
  <div class="col-sm-3"><!--left col-->


  <div class="text-center">
    <img src="${bioData.avatar}" class="avatar img-circle img-thumbnail" alt="avatar">
  </div></hr><br>


        <ul class="list-group">
          <li class="list-group-item text-muted">Activity <i class="fa fa-dashboard fa-1x"></i></li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Shares</strong></span> 125</li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Likes</strong></span> 13</li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Articles</strong></span> ${bioData.count_articles}</li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Comments</strong></span> ${bioData.count_comments}</li>
        </ul>

        <div class="panel panel-default">
          <div class="panel-heading">Social Media</div>
          <div class="panel-body">
            <i class="fa fa-facebook fa-2x"></i> <i class="fa fa-github fa-2x"></i> <i class="fa fa-twitter fa-2x"></i> <i class="fa fa-pinterest fa-2x"></i> <i class="fa fa-google-plus fa-2x"></i>
          </div>
        </div>

      </div><!--/col-3-->
    <div class="col-sm-9">
          <ul class="nav nav-tabs">
              <li class="active"><a data-toggle="tab" href="#bio">BIO</a></li>
            </ul>


        <div class="tab-content">
          <div class="tab-pane active" id="bio">
            <form class="form" action="##" method="post" id="bioForm">
              <div class="form-group">

                  <div class="col-xs-6">
                    <h4>First name</h4>
                    <p><span>${bioData.first_name}</span></p>
                  </div>
              </div>
              <div class="form-group">

                  <div class="col-xs-6">
                    <h4>Last name</h4>
                    <p><span>${bioData.last_name}</span></p>
                  </div>
              </div>

              <div class="form-group">

                  <div class="col-xs-6">
                    <h4>Birthday</h4>
                    <p><span>${bioData.birthday || 'no date'}</span></p>
                  </div>
              </div>

              <div class="form-group">
                  <div class="col-xs-6">
                    <h4>Gender</h4>
                    <p><span>${bioData.gender === 0 ? 'Unknown' : bioData.gender === 1 ? 'Male' : 'Female'}</span></p>
                  </div>
              </div>
              <div class="form-group">

                  <div class="col-xs-6">
                    <h4>Email</h4>
                    <p><span>${bioData.email}</span></p>
                  </div>
              </div>
        </form>

            <hr>
      </div><!--/col-9--
  `
}
