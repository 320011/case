// Add tag
$('#add_tag').click(function () {
  $('#submission_type').val("tag");
  $('form').submit();
});

// Add medical history
$('#add_medical_history').click(function () {
  $('#submission_type').val("medical_history");
  $('form').submit();
});

// Add medication
$('#add_medication').click(function () {
  $('#submission_type').val("medication");
  $('form').submit();
});

$('#save').click(function () {
  $('#submission_type').val("save");
  $('#id_is_submitted').prop('value', false);
  $('form').submit();
});

$('#submit_button').click(function () {
  $('#submission_type').val("submit");
  $('#id_is_submitted').prop('value', true);
  $('form').submit();
});
