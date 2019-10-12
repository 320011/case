$(".report").click(function(){
	var reasons = window.prompt('What is the report reason?');
	var success_message = "Thanks for your report!";
	var failure_message = "You can't submit a report without reasons";

	if(reasons != null && reasons != '') 
    {
      alert(success_message);
      console.log(reasons);

      let comment_body = document.getElementById('comment_body').innerText;;
   	  let case_id = document.getElementById('case_id').innerText;
      let comment_date = document.getElementById('comment_date').innerText;
      console.log(comment_body);
      console.log(comment_date);


  	// $.ajax({
  	// 	type: 'POST',
  	// 	url: 'api/v1/submit_report/' + case_id + '/' + report_id
    //  data:{
    // comment 
    // comment_author 
    // report_author 
    // comment_body x
    // comment_date x
    // report_date 
    // reason x
    // report_reviewed

    //},


    //success: function(){

      //}

  	// });


    }

    if(reasons == null)
    {
    	return;
    }

    if(reasons == ''){
    	alert(failure_message);
    }

});










