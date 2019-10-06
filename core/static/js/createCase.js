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

// Add other 
$('#add_other').click(function () {
  $('#submission_type').val("other");
  $('form').submit();
});

// Save 
$('#save').click(function () {
  $('#submission_type').val("save");
  $('#id_is_submitted').prop('value', false);
  $('form').submit();
});

// Submit 
$('#submit_button').click(function () {
  $('#submission_type').val("submit");
  $('#id_is_submitted').prop('value', true);
  $('form').submit();
});


// Dynamically Generating Description Base
window.onload = function () {
  // Get relevant elements
  let age_type = document.getElementById('id_age_type');
  let age = document.getElementById('id_age');
  let sex = document.getElementById('id_sex');
  let height = document.getElementById('id_height');
  let weight = document.getElementById('id_weight');
  let scr = document.getElementById('id_scr');

  // Add event listeners for change
  age_type.addEventListener("change", handleChange);
  age.addEventListener("change", handleChange);
  sex.addEventListener("change", handleChange);
  height.addEventListener("change", handleChange);
  weight.addEventListener("change", handleChange);
  scr.addEventListener("change", handleChange);
  scr.addEventListener("load", handleChange);

  // Conditionally creates optionals string in the format [(*optional* height/weight/SCr)]
  function createOptionals(height, weight, scr) {
    let optional_string;
    let height_value = height.value;
    height_value ? height_value += 'cm' : height_value = '';
    let weight_value = weight.value;
    weight_value ? weight_value += 'kg' : weight_value = '';
    let scr_value = scr.value;
    scr_value ? scr_value += 'μmol/L SCr' : scr_value = '';
    let optional_array = [height_value, weight_value, scr_value];
    if (!height_value && !weight_value && !scr_value) {
      optional_string = '';
    } else {
      let output = '[';
      optional_array.forEach(function (value) {
        if (value) {
          output += value + '/';
        }
      });
      if (output.charAt(output.length - 1) === '/') {
        output = output.slice(0, -1);
      }
      output += ']';
      optional_string = output;
    }
    return optional_string;
  }

  // Get the corresponding values on page load
  let age_type_value = age_type.value;
  age_type_value === 'M' ? age_type_value = 'mo' : age_type_value = 'yo';
  let age_value = age.value || '46';
  let sex_value = sex.value || 'Male';
  let optionals = createOptionals(height, weight, scr);
  sex_value === 'F' ? sex_value = 'female' : sex_value = 'male';
  document.getElementById('description_preview').innerText = 'A ' + age_value + '-' + age_type_value + ' ' + sex_value + ' ' + optionals + ' presents to your pharmacy...';

  // Deal with change for dynamic description rendering
  function handleChange() {
    document.getElementById('id_age_type').value === 'M' ? age_type_value = 'mo' : age_type_value = 'yo';
    age_value = document.getElementById('id_age').value || '46';
    document.getElementById('id_sex').value === 'F' ? sex_value = 'female' : sex_value = 'male';
    optionals = createOptionals(document.getElementById('id_height'), document.getElementById('id_weight'), document.getElementById('id_scr'))
    document.getElementById('description_preview').innerText = 'A ' + age_value + '-' + age_type_value + ' ' + sex_value + ' ' + optionals + ' presents to your pharmacy...';
  }
};