function caseAdmin_fieldChanged(key, entity) {
  let $e = $(´#${key}-${rowId}´);
  let update = {
    key: key
    id: entity,
    value: $e.val(),
  };
  $.ajax({
    url: ´/api/v1/admin/${key}´,
    type: "PUT",
    dataType: "json",
    data: update,
    success: (result, status, xhr) => {
      $e.val(result.value);
      console.log("Updated value", key, "for", entity);
    },
    error: (xhr, status, error) => {
      $e.val("ERR");
      alert("Failed to update entity: " + error.message);
    }
  });
}
