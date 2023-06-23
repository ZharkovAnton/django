$(document).ready(function() {
  $('#subRes').submit(onClick);
});

function onClick(e) {
  e.preventDefault();
  grecaptcha.ready(function() {
    grecaptcha.execute('6LcUJYsmAAAAAC_rjShi2_WWfcdtQXxS_iKJwlsp', {action: 'login'}).then(function(token) {
        $.ajax({
          url: '/api/v1/auth/captcha/',
          type: "POST",
          dataType: 'json',
          data: {token: token},
          success: function (data) {
            if (data.detail === 'success') {
              resetPassword(e)
            }
          },
          error: function (data) {
            alert('bad');
            }
          })
        })
    });
  };


function resetPassword(e) {
  let form = $('#subRes');
  const url = new URL(window.location.href);
  const uid = url.searchParams.get('uid');
  const token = url.searchParams.get('token');
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: `${form.serialize()}&token=${token}&uid=${uid}`,
    success: function (data) {
      alert('ok')
    },
    error: function (data) {
      console.log('error', data);
    }
  })
}
