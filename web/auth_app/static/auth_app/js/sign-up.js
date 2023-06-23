$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      let errors = data.responseJSON;
      $.each(errors, function(key, value) {
      let input = $('#'+key);
      input.after('<span class="error">'+value+'</span>');
    });
    }
  })
}
