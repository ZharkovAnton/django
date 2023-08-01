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
    success: function (data) {;
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
  const spanNavbar = document.querySelector('span.navbar-brand');
  const aTags = spanNavbar.querySelectorAll('a')
  const lastElement = aTags[aTags.length - 1];
  const authUser = parseInt(lastElement.getAttribute('data-userId'))
  return `
  <div class="row">
  <div class="col-sm-10"><h1>${bioData.full_name}</h1></div>
  <div class="col-sm-2"><a href="/users" class="pull-right"><img title="profile image" class="img-circle img-responsive" src="http://www.gravatar.com/avatar/28fd20ccec6865e2d5f0e1f4446eb7bf?s=100"></a></div>
</div>
<div class="row">
  <div class="col-sm-3"><!--left col-->


  <div class="text-center">
    <img src="${bioData.avatar}" class="avatars img-circle img-thumbnail" alt="avatar">
  </div></hr><br>
  <div class="action-buttons">
      <div class="row">
          <div class="col-xs-6">
              <a href="#" id="follower-update" onclick="getUpdateFollowersForOtherUser(event, this)" class="${bioData.followers.includes(authUser) ? 'btn-danger' :'btn-success'} btn btn-block"> <span class="type-following">${bioData.followers.includes(authUser) ? 'Unsubscribe':'Subscribe'}</span> <span id="follow-value" class="badge bg-secondary">${bioData.count_followers}</span></a>
          </div>
          <div class="col-xs-6">
              <a href="#" onclick="getFollowersForOtherUser(event, this)" class="btn btn-primary btn-block" data-target="#modal-example" data-toggle="modal"><i class="fa fa-android-mail"></i> Followers</a>
          </div>


          <!-- line modal -->
          <div class="modal fade" id="modal-example" tabindex="-1" role="dialog" aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>
                  <h3 class="modal-title" id="lineModalLabel">Followers</h3>
                </div>
              <div class="modal-body">
                    <!-- content goes here -->
                    <div class="container-fluid">
                      <div class="row bootstrap snippets bootdey">
                        <div class="col-md-12 col-xs-12">
                          <div class="panel" id="followers">
                            <h4><i class="fa fa-search"></i> Followers Search...</h4>
                            <div class="input-group">
                              <input id="search" type="text" class="form-control">
                              <span class="input-group-btn">
                                <button id="search-btn" class="btn btn-default" type="button">
                                    <i class="fa fa-search"></i>
                                </button>
                              </span>
                            </div>

                            <div class="panel-heading">
                              <h3 class="panel-title">
                                <i class="icon md-check" aria-hidden="true"></i> Followers
                              </h3>
                            </div>
                            <div class="panel-body">
                              <ul class="list-group list-group-dividered list-group-full">

                              </ul>
                            </div>
                          </div>
                        </div>
                    </div>
                  </div>
                    <!-- content ends here -->
              </div>
              <div class="modal-footer">
                <div class="btn-group btn-group-justified" role="group" aria-label="group button">
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default" data-dismiss="modal"  role="button">Close</button>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>
      </div>


  </div>
  <br>

        <ul class="list-group">
          <li class="list-group-item text-muted">Activity <i class="fa fa-dashboard fa-1x"></i></li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Shares</strong></span> 125</li>
          <li class="list-group-item text-right"><span class="pull-left"><strong>Likes</strong></span> ${bioData.total_likes}</li>
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
