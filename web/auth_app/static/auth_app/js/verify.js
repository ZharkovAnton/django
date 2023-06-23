$(function () {
  verifyEmail()
});

function verifyEmail() {
  const url = new URL(window.location.href);
  const key = url.searchParams.get('key');
  $.ajax({
    url: '/api/v1/auth/sign-up/verify/',
    type: 'POST',
    dataType: 'json',
    data: {key: key},
    success: function(data) {
      document.querySelector('.verification').innerText = data.detail;
      setTimeout(function () {
        window.location.assign('/');
      }, 3000);
    },
    error: function(data) {
      document.querySelector('.verification').innerText = data.responseJSON.detail;
    }
    });
}
