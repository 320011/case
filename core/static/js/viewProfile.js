function setGetParameter(){
    var search_word = $("#filter_tag").val();
    $.ajax({
    type: 'POST',
    url: '',
    data: search_word,
    });
}