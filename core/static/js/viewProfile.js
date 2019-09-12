function setGetParameter() {
    var search_word = $(".filter_tag").prop("value");
    console.log(search_word);
    $.ajax({
        type: 'POST',
        url: '',
        data: search_word,
        beforeSend : function(jqXHR, settings) {
            jqXHR.setRequestHeader("x-csrftoken", get_the_csrf_token_from_cookie());
        },
    });
}