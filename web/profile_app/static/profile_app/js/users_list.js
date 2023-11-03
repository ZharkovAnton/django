$(function () {
  getUserList();
});

function getUserList() {
  const spanNavbar = document.querySelector('span.navbar-brand');
  const aTags = spanNavbar.querySelectorAll('a')
  const lastElement = aTags[aTags.length - 1];
  const userId = lastElement.getAttribute('data-userId');
  $.ajax({
    url: '/api/v1/profile/users/',
    type: "GET",
    success: function (data) {
      const filteredUsers = data.filter(user => user.id !== parseInt(userId));
      const usersHTML = filteredUsers.map(user => {
        user.date_joined = formatDate(user.date_joined)

        const urlParts = user.avatar.split('/');
        const lastElement = urlParts[urlParts.length - 1];
        if (lastElement === 'no-image-available.jpg') {
          user.avatar = 'http://localhost:8000/media/no_ava/no_ava.png';
        }
        return generateUserListHTML(user);
      }).join('')

      const divContainer = document.querySelector('.userstable');
      divContainer.insertAdjacentHTML('afterbegin', usersHTML);
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function generateUserListHTML(user){
  return `
  <tr>
      <td>
          <img src="${user.avatar}" alt="no-image" width="120" height="90">
          <a href="/profile/${user.id}" class="user-link">${user.full_name}</a>
      </td>
      <td>${user.date_joined}</td>
      <td class="text-center">
          <span class="label ${user.is_active === true ? 'label label-success' : 'label-danger'}">${user.is_active === true ? 'active' : 'inactive'}</span>
      </td>
      <td>
        ${user.email}
      </td>
      <td style="width: 20%;">
          <a href="#" class="table-link text-warning">
              <span class="fa-stack">
                  <i class="fa fa-square fa-stack-2x"></i>
                  <i class="fa fa-search-plus fa-stack-1x fa-inverse"></i>
              </span>
          </a>
          <a href="#" class="table-link text-info">
              <span class="fa-stack">
                  <i class="fa fa-square fa-stack-2x"></i>
                  <i class="fa fa-pencil fa-stack-1x fa-inverse"></i>
              </span>
          </a>
      </td>
  </tr>
  `
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
