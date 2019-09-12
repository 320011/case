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

function maxTime() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    if(dd<10){
            dd='0'+dd
        } 
        if(mm<10){
            mm='0'+mm
        } 
    today = yyyy+'-'+mm+'-'+dd;
    
    document.getElementById("start_time").setAttribute("max", today);
    document.getElementById("end_time").setAttribute("max", today);
}

function endMinTime() {
    var minTime = document.getElementById("start_time").value;
    document.getElementById("end_time").setAttribute('min', minTime);
}