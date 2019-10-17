function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(".report").click(function(){
	var reasons = window.prompt('What is the report reason?');
	var success_message = "Thanks for your report!";
	var failure_message = "You can't submit a report without reasons";

	if(reasons != null && reasons != '') 
    {
      var id = $(this).attr('id'); //get the id of the comment

  	$.ajax({
  		type: 'POST',
  		url: '/cases/api/v1/submit_report/' + id + '/' ,
      dataType: 'json',
      data:{
            'comment_id': id,
            'report_reason': reasons
          },

    success: function(){
      alert(success_message);

      }

  	});


    }

    if(reasons == null)
    {
    	return;
    }

    if(reasons == ''){
    	alert(failure_message);
    }

});



$(".delete").click(function(){
  confirmation = window.confirm('Is it okay to delete this comment?');
  success_message = "You have deleted a comment(softly).";

  if(confirmation){
      var id = $(this).attr('id'); //get the id of the comment\

    $.ajax({
      type: 'POST',
      url: '/cases/api/v1/delete_comment/' + id + '/' ,
      dataType: 'json',
      data:{
            'comment_id': id
          },

    success: function(){
      alert(success_message);
      }
  });

  if(!confirmation)
  {
    return;
  }

};
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

