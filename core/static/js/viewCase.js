$("#feedback").toggle();
$(document).ready(function () {
  if (window.innerWidth < 1026) {
    $('#row-container').removeClass('row');
    $('#details').removeClass('col-3');
  }
});

$(window).resize(function () {
  if (window.innerWidth < 1026) {
    $('#row-container').removeClass('row');
    $('#details').removeClass('col-3');
  } else {
    $('#row-container').addClass('row');
    $('#details').addClass('col-3');
  }
});

function handleClick(e) {
  let a = document.getElementById('A');
  let b = document.getElementById('B');
  let c = document.getElementById('C');
  let d = document.getElementById('D');
  if (a.classList.contains('list-group-item-warning')) {
    a.classList.remove('list-group-item-warning');
    a.classList.remove('clicked');
  }
  if (b.classList.contains('list-group-item-warning')) {
    b.classList.remove('list-group-item-warning');
    b.classList.remove('clicked');
  }
  if (c.classList.contains('list-group-item-warning')) {
    c.classList.remove('list-group-item-warning');
    c.classList.remove('clicked');
  }
  if (d.classList.contains('list-group-item-warning')) {
    d.classList.remove('list-group-item-warning');
    d.classList.remove('clicked');
  }
  e.classList.add('list-group-item-warning');
  e.classList.add('clicked');

}

$("#submit_response").click(function () {
  let element = document.getElementsByClassName('clicked')[0];
  let id = document.getElementById('case_id').innerText;

  if (element) {
    $.ajax({
      url: '/cases/ajax/validate_answer/' + id,
      dataType: 'json',
      data: {
        'choice': element.id
      },
      success: function (data) {
        $('#discussion_container').removeClass('d-none');
        $('#show_discussion').trigger('click');
        $('#questions').slideUp('slow');
        $('#feedback').slideDown('slow');
        if (data.success) {
          $('#feedback_alert').removeClass('alert-danger').addClass('alert-success').html(data.answer_message)
        } else {
          $('#feedback_alert').removeClass('alert-success').addClass('alert-danger').html(data.answer_message)
        }
        $('#feedback_text').html(data.feedback);
        $('#total_average').html(data.attempts.total_average);
        $('#user_average').html(data.attempts.user_average);
        $('#total_attempts').html(data.attempts.total_attempts);
        $('#user_attempts').html(data.attempts.user_attempts);
      }
    });
  }

});

$('#attempt_again').click(function () {
  $('#questions').slideDown('slow');
  $('#feedback').slideUp('slow')
});