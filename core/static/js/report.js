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
    let reasons = prompt('Report reason');
    if(reasons != null && reasons.trim() != "")
    {
        let id = $(this).attr('id'); //get the id of the comment
        $.ajax({
            type: 'POST',
            url: '/cases/api/v1/submit_report/' + id,
            dataType: 'json',
            data:{
                'comment_id': id,
                'report_reason': reasons
            },
            success: function(resp){
                alert("Your report has been submitted and will be reviewed by staff");
            }
        });
    } else {
        alert("Please try again and enter a reason");
    }
});

    
$(".delete").click(function(){
    if(confirm('Are you sure you would like to delete this comment.\n\nIt will no longer appear to users but it will still be available in the admin until it is hard deleted.')){
        let id = $(this).attr('id'); //get the id of the comment\
        $.ajax({
            type: 'POST',
            url: '/cases/api/v1/delete_comment/' + id + '/' ,
            dataType: 'json',
            data:{
                'comment_id': id
            },
            success: function(){
                alert("The comment has been deleted.");
                location.reload();
            }
        });
    }
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

