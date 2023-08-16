$(function () {
  getNewsline();
});

function getNewsline() {
  $.ajax({
    url: `/api/v1/actions/walls/`,
    type: "GET",
    success: function (data) {
      $('.bootstrap').empty();
      const newslineHTML = data.map(event => {
        return generateNewslineHTML(event)
      }).join('');
      const divBootstrap = document.querySelector('.bootstrap')
      divBootstrap.insertAdjacentHTML('afterbegin', newslineHTML)
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function generateNewslineHTML(event) {
  event.created = formatDate(event.created)
  return `
  <div class="row">
    <div class="alert alert-${event.name.toLowerCase()=== 'updated avatar' ? 'success':'info'}" role="alert">${event.user.full_name} ${event.name.toLowerCase()} at ${event.created}</div>
	</div>
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
