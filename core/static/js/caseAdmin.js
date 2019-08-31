function getCookie(name) {
  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
  return null;
}

function admin_updateEntity(endpoint, entity) {
  // construct a user model with the updated data
  let inps = document.getElementById(`admin-table-${entity}`).getElementsByTagName("input");
  let updates = {};
  for (let i = 0; i < inps.length; i++) {
    let inp = inps[i];
    if (inp.type === "checkbox") {
      updates[inp.name] = inp.value === "on"; // checkbox sends string "on"/"off" and api expects a bool
    } else {
      updates[inp.name] = inp.value;
    }
  }

  // ajax the updated data to the server
  fetch(endpoint + entity, {
    method: "PUT",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify(updates),
  }).then(r => r.json()).then(resp => {
    if (resp && resp.success) {
      alert("Updated an entity");
      console.log("Updated an entity. \nNew values:", updates);
    } else {
      alert("Failed to update an entity. \nError: " + resp.message);
      console.log("Failed to update an entity. \nError:", resp.message);
    }
  }).catch(err => {
    alert("Failed to update an entity. \nFatal Error: " + err);
    console.log("Failed to update an entity. \nFatal Error:", err);
  });
}