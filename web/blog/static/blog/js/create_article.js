$(function () {
  $('#summernote').summernote({
    placeholder: 'Write your article ...',
    height: 120,
  });
  getCategories();
  $('#createArticleForm').submit(sendArticle);
})

function getCategories() {
  $.ajax({
    url: '/api/v1/article/create/',
    type: 'GET',
    success: function(response) {
      const generateCategoryHTML = (category) => {
        return `<option value="${category.slug}">${category.name}</option>`
      }
      const categoriesHTML = response.map(category => {
        return generateCategoryHTML(category)
      }).join('')
      const selectCategory = document.querySelector('select', 'category')
      selectCategory.insertAdjacentHTML('afterbegin', categoriesHTML)
    },
    error: function(response) {
      if (response.status === 401) {
        const errorMessage = '<span style="color:red;">You are not authorised. Please log in. </span><br/>'
        const div = document.querySelector('.col-md-offset-3')
        div.insertAdjacentHTML('afterbegin', errorMessage)
      }
    }
  })
}

function sendArticle (e) {
  e.preventDefault()
  let form = $(this)
  let formData = new FormData(form[0])
  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    contentType: false,
    processData: false,
    data: formData,
    success: function (response) {
      location.reload()
    },
    error: function (response) {
      const errors = response.responseJSON
      $.each(errors, function (key, value) {
        if (key === 'content') {
          const divPlaceholder = document.querySelector('.note-placeholder')
          divPlaceholder.classList.add('error')
          divPlaceholder.innerText = value
        } else {
          const inputCat = document.getElementsByName(`${key}`)[0];
          inputCat.classList.add('error')
          inputCat.placeholder = value;
        }
      })
    }
  })
}

