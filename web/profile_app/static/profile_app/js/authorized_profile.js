$(function () {
  getDetailProfile();
  $('.bootstrap').on('submit', '#bioForm', updateBIOProfile);
  $('.bootstrap').on('submit', '#passwordForm', updatePasswordProfile);
  $('.bootstrap').on('change', 'input[type="file"]', updateAvatarProfile);
});

function getDetailProfile() {
  const spanNavbar = document.querySelector('span.navbar-brand');
  const aTags = spanNavbar.querySelectorAll('a')
  const lastElement = aTags[aTags.length - 1];
  const userId = lastElement.getAttribute('data-userId');
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

function updateBIOProfile(e) {
  e.preventDefault();
  const form = $(this)
  $.ajax({
    url: '/api/v1/profile/update/bio/',
    type: "PUT",
    dataType: "json",
    data: form.serialize(),
    success: function (data) {
      getDetailProfile();

    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function updatePasswordProfile(e) {
  e.preventDefault();
  const form = $(this)
  console.log(userId);
  $.ajax({
    url: '/api/v1/profile/update/password/',
    type: "POST",
    dataType: "json",
    data: form.serialize(),
    success: function (data) {
      getDetailProfile();

    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function updateAvatarProfile(e) {
  e.preventDefault();
  const formData = new FormData()
  let avatarFile = $('.bootstrap .file-upload')[0].files[0];
  if (avatarFile) {
    formData.append('avatar', avatarFile)
    $.ajax({
      url: '/api/v1/profile/update/avatar/',
      type: "POST",
      contentType: false,
      processData: false,
      data: formData,
      success: function (data) {
        getDetailProfile();

      },
      error: function (data) {
        console.log('error', data)
      }
    })
  }
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
    <h6>Upload a different photo...</h6>
    <input type="file" class="text-center center-block file-upload">
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
              <li><a data-toggle="tab" href="#change-password">Change Password</a></li>
              <li><a data-toggle="tab" href="#settings">Menu 2</a></li>
            </ul>


        <div class="tab-content">
          <div class="tab-pane active" id="bio">
            <form class="form" action="##" method="post" id="bioForm">
              <div class="form-group">

                  <div class="col-xs-6">
                      <label for="first_name"><h4>First name</h4></label>
                      <input type="text" class="form-control" name="first_name" id="first_name" placeholder="first name" value="${bioData.first_name}" title="enter your first name if any.">
                  </div>
              </div>
              <div class="form-group">

                  <div class="col-xs-6">
                    <label for="last_name"><h4>Last name</h4></label>
                      <input type="text" class="form-control" name="last_name" id="last_name" placeholder="last name" value="${bioData.last_name}" title="enter your last name if any.">
                  </div>
              </div>

              <div class="form-group">

                  <div class="col-xs-6">
                      <label for="phone"><h4>Birthday</h4></label>
                      <input type="date" class="form-control" name="birthday" id="birthday" placeholder="Select date of birth" onfocus="(this.type='date')" value="${bioData.birthday || ''}" title="Select date of birth">
                  </div>
              </div>

              <div class="form-group">
                  <div class="col-xs-6">
                      <label for="gender"><h4>Gender</h4></label>
                      <select name="gender" id="gender" class="form-control">
                      <option value="0" ${bioData.gender === 0 ? 'selected' : ''}>Unknown</option>
                      <option value="1" ${bioData.gender === 1 ? 'selected' : ''}>Man</option>
                      <option value="2" ${bioData.gender === 2 ? 'selected' : ''}>Female</option>
                      </select>
                  </div>
              </div>
              <div class="form-group">

                  <div class="col-xs-6">
                      <label for="email"><h4>Email</h4></label>
                      <input type="email" class="form-control" name="email" id="email" placeholder="you@email.com" value="${bioData.email}" title="enter your email." readonly>
                  </div>
              </div>
              <div class="form-group">
                    <div class="col-xs-12">
                        <br>
                        <button class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Save</button>
                    </div>
              </div>
        </form>

            <hr>

           </div><!--/tab-pane-->
           <div class="tab-pane" id="change-password">
                <form class="form" action="##" method="post" id="passwordForm">
                    <div class="form-group">

                        <div class="col-xs-6">
                            <label for="password_1"><h4>Password</h4></label>
                            <input type="password" class="form-control" name="password_1" id="password_1" placeholder="new password" title="enter your password.">
                        </div>
                    </div>
                    <div class="form-group">

                        <div class="col-xs-6">
                          <label for="password_2"><h4>Verify</h4></label>
                            <input type="password" class="form-control" name="password_2" id="password_2" placeholder="repeat new password" title="enter your password2.">
                        </div>
                    </div>
                    <div class="form-group">

                      <div class="col-xs-6">
                        <label for="old_password"><h4>Old Password</h4></label>
                          <input type="password" class="form-control" name="old_password" id="old_password" placeholder="old password" title="enter your old_password.">
                      </div>
                  </div>
                    <div class="form-group">
                         <div class="col-xs-12">
                              <br>
                              <button class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Save</button>
                          </div>
                    </div>
              </form>

           </div><!--/tab-pane-->
           <div class="tab-pane" id="settings">

            </div>

            </div><!--/tab-pane-->
        </div><!--/tab-content-->

      </div><!--/col-9--
  `
}
