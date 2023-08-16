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
  const aTags = document.querySelector('span.navbar-brand').querySelectorAll('a');
  const lastElement = aTags[aTags.length - 1];
  const authUser = parseInt(lastElement.getAttribute('data-userId'))
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
          ${user.id === authUser ? '' : (user.followers.includes(authUser) ? `<button type="button" id="follower-update-list" data-userid="${user.id}" class="btn btn-danger btn-sm waves-effect waves-light" onclick="getUpdateFollowersForOtherUser(event, this, buttonId='list_button')"><span class="type-following">Unsubscribe</span></button>`:`<button type="button" data-userid="${user.id}" class="btn btn-success btn-sm waves-effect waves-light" onclick="getUpdateFollowersForOtherUser(event, this, buttonId='list_button')"><span class="type-following">Subscribe</span></button>`)}
        </div>
        <div><a class="name" href="/profile/${user.id === authUser ? '':`${user.id}`}"> ${user.full_name}</a></div>
        <small>${user.email}</small>
      </div>
    </div>
  </li>
  `
}

function getUpdateFollowersForOtherUser(event, element, buttonId) {
  event.preventDefault();
  const userId = parseInt(element.getAttribute('data-userid'))
  $.ajax({
    url: `/api/v1/actions/followers/update/`,
    type: "POST",
    dataType: "json",
    data: {id: userId},
    success: function (data) {
      if (buttonId === 'list_button') {
        if(element.classList.contains('btn-success')) {
          element.classList.remove('btn-success')
          element.classList.add('btn-danger')
          element.querySelector('span.type-following').innerText = 'Unsubscribe'
        } else {
          element.classList.remove('btn-danger')
          element.classList.add('btn-success')
          element.querySelector('span.type-following').innerText = 'Subscribe'
      }

      } else if (buttonId === 'profile_button') {
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

      }

    },
    error: function (data) {
      console.log('error', data)
    }
  })
}
