function setGetParameter(){
    var search_word = $("#filter_tag").val();
    var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
    $.ajax({
    type: 'POST',
    url: '',
    data: search_word,
    beforeSend : function(jqXHR, settings) {
        jqXHR.setRequestHeader("x-csrftoken", get_the_csrf_token_from_cookie());
    },
    });
}