var url = new URL(window.location.href);
var key = url.searchParams.get('key');

$.ajax({
  url: {% url 'api:v1:auth_app:sign-up-verify' %},
  type: 'POST',
  data: {key: key},
  success: function(response) {
  },
  error: function(xhr, status, err) {
  }
  });

