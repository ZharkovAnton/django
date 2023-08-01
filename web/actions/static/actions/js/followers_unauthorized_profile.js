$(function () {
});

function getFollowersForOtherUser() {
  const url = new URL(window.location.href);
  const pathnameArray = url.pathname.split('/');
  const userId = pathnameArray[pathnameArray.length - 1];
  $.ajax({
    url: `/api/v1/actions/followers/${userId}/`,
    type: "GET",
    success: function (data) {
      console.log(data.results)
      $('.bootstrap').find('.list-group-dividered').empty();
      const followersHTML = data.results.map(user => {
        return generateFollowersHTML(user)
      }).join('');
      const ulListGroup = document.querySelector('.bootstrap').querySelector('.list-group-dividered')
      ulListGroup.insertAdjacentHTML('afterbegin', followersHTML)

    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function generateFollowersHTML(user) {
  return `
  <li class="list-group-item">
    <div class="media">
      <div class="media-left">
        <a class="avatar">
          <img src="${user.avatar}" alt="no-image">
          <i></i>
        </a>
      </div>
      <div class="media-body">
        <div class="pull-right">
          <button type="button" class="btn btn-info btn-sm waves-effect waves-light">Follow</button>
        </div>
        <div><a class="name" href="#">${user.full_name}</a></div>
        <small>${user.email}</small>
      </div>
    </div>
  </li>
  `
}

function getUpdateFollowersForOtherUser(event) {
  event.preventDefault();
  const url = new URL(window.location.href);
  const pathnameArray = url.pathname.split('/');
  const userId = pathnameArray[pathnameArray.length - 1];
  $.ajax({
    url: `/api/v1/actions/followers/update/`,
    type: "POST",
    dataType: "json",
    data: {id: userId},
    success: function (data) {
      const buttonSubscribers = document.querySelector('.bootstrap').querySelector('#follower-update')
      const countSubscribers = document.querySelector('.bootstrap').querySelector('#follow-value')
      countSubscribers.innerText = data.count_followers

      if(buttonSubscribers.classList.contains('btn-success')) {
        buttonSubscribers.classList.remove('btn-success')
        buttonSubscribers.classList.add('btn-danger')
        buttonSubscribers.querySelector('span.type-following').innerText = 'Unsubscribe'
      } else {
        buttonSubscribers.classList.remove('btn-danger')
        buttonSubscribers.classList.add('btn-success')
        buttonSubscribers.querySelector('span.type-following').innerText = 'Subscribe'
      }

    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

