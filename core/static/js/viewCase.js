$("#feedback").toggle();
$(document).ready(function () {
  if (window.innerWidth < 1026) {
    $('#row-container').removeClass('row');
    $('.comment-container').removeClass('col-8').addClass('col');
    $('.comment-content').removeClass('d-flex');
    $('.comment-break').removeClass('d-none');
    $('#details').removeClass('col-3');
  }
});

$(window).resize(function () {
  if (window.innerWidth < 1026) {
    $('#row-container').removeClass('row');
    $('.comment-container').removeClass('col-8').addClass('col');
    $('.comment-content').removeClass('d-flex');
    $('.comment-break').removeClass('d-none');
    $('#details').removeClass('col-3');
  } else {
    $('#row-container').addClass('row');
    $('.comment-container').removeClass('col').addClass('col-8');
    $('.comment-content').addClass('d-flex');
    $('.comment-break').addClass('d-none');
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
      url: '/cases/api/v1/validate_answer/' + id,
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

$('#discussion').toggle();
$('#show_discussion').click(function () {
  $('#discussion').slideToggle();
  $('#show_discussion').slideToggle();
})

$('#submit_comment').click(function () {
  let comment_body = document.getElementById('comment-box').value;
  let comment_is_anon = false; 
  if (document.getElementById('is_anonymous_checkbox') && document.getElementById('is_anonymous_checkbox').checked) comment_is_anon = true; 
  let id = document.getElementById('case_id').innerText;
  if (comment_body) {
    $.ajax({
      url: '/cases/api/v1/submit_comment/' + id,
      dataType: 'json',
      data: {
        'body': comment_body,
        'is_anon': comment_is_anon
      },
      success: function (data) {
        $('#comment-box').val('');
        let container = window.innerWidth < 1026 ? "col comment-container" : "col-8 comment-container";
        let content = window.innerWidth < 1026 ? "w-100 justify-content-between comment-content" : "d-flex w-100 justify-content-between comment-content";
        let br = window.innerWidth < 1026 ? "comment-break" : "comment-break d-none";
        let name = data.user.name;
        let date = moment(data.comment.date).format("MMM D YYYY, hh:mm a.");
        let delete_img = "/static/img/report_delete.png"
        let comment_id = data.comment.id
        if ( data.user.is_tutor ) {
          name = '<a data-toggle="tooltip" title="Tutor"><i class="fa fa-fw fa-graduation-cap" data-toggle="tooltip"></i></a>' + data.user.name;
        } else {
          name = data.comment.is_anon ? data.user.name + " (Anonymous)" :  data.user.name;
        }
        // 

        htmlstring =
          `<div class="row justify-content-end">\
                  <div class="${container}">\
                    <div class="alert alert-primary" role="alert">\
                      <div class="${content}">\
                        <small class="text-muted">\
                        ${name}\
                        </small>\
                        <br class="${br}">\
                        <small class="text-muted">${date}</small>\
                      </div>\
                    <small class="float-right delete id="${comment_id}"><img src="${delete_img}" width="20" height="20" data-toggle="tooltip title="Delete" data-placement="bottom"></small>\
                      <p class="mb-1">${data.comment.body}</p>\
                    </div>\
                  </div>\
                </div>`;
        $("#comment-container").prepend($(htmlstring).hide().delay(500).show('slow'));

    $(".delete").click(function(){
    if(confirm('Are you sure you would like to delete this comment.\n\nIt will no longer appear to users but it will still be available in the admin until it is hard deleted.')){
        $.ajax({
            type: 'POST',
            url: '/cases/api/v1/delete_comment/' + comment_id  + '/' ,
            dataType: 'json',
            data:{
                'comment_id': comment_id 
            },
            success: function(){
                alert("The comment has been deleted.");
                location.reload();
            }
        });
    }
});
      }
    });
  }
});


