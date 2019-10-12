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

function admin_updateEntity(endpoint, entity, silent=false) {
  // construct a user model with the updated data
  let inps = document.getElementById(`admin-table-${entity}`).getElementsByTagName("input");
  let updates = {};
  for (let i = 0; i < inps.length; i++) {
    let inp = inps[i];
    if (inp.type === "checkbox") {
      updates[inp.name] = inp.checked;
    } else if (inp.type === "datetime-local") {
      updates[inp.name] = inp.value.toString();
    } else {
      updates[inp.name] = inp.value;
    }
  }
  // get the <select> tags too
  let sels = document.getElementById(`admin-table-${entity}`).getElementsByTagName("select");
  for (let i = 0; i < sels.length; i++) {
    let sel = sels[i];
    if (sel.multiple) {
      updates[sel.name] = [];
      for (let j = 0; j < sel.selectedOptions.length; j++) {
        updates[sel.name].push(sel.selectedOptions[j].value);
      }
      console.log(updates[sel.name])
    } else {
      updates[sel.name] = sel.value;
    }
  }
  // get <textarea> tags
  let txtareas = document.getElementById(`admin-table-${entity}`).getElementsByTagName("textarea");
  for (let i = 0; i < txtareas.length; i++) {
    let ta = txtareas[i];
    updates[ta.name] = ta.value;
  }

  // ajax the updated data to the server
  fetch(endpoint + entity, {
    method: "PATCH",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify(updates),
  }).then(r => r.json()).then(resp => {
    if (resp && resp.success) {
      if (!silent) {
        alert("Updated an entity");
      }
      console.log("Updated an entity. \nNew values:", updates);
      location.reload();
    } else {
      alert("Failed to update an entity. \nError: " + resp.message);
      console.log("Failed to update an entity. \nError:", resp.message);
    }
  }).catch(err => {
    alert("Failed to update an entity. \nFatal Error: " + err);
    console.log("Failed to update an entity. \nFatal Error:", err);
  });
}

function admin_deleteEntity(endpoint, entity, hard, silent=false) {
  let conf = () => { return confirm("Are you sure you want to SOFT DELETE this entity?\n\nThis will HIDE the entity from all areas of the site besides the admin."); };
  if (hard) {
    conf = () => { return confirm("Are you sure you want to HARD DELETE this entity?\n\nThis will PERMANENTLY DELETE the entity from the entire system."); };
  }
  if (conf()) {
    // ajax the deleted entity id to the server
    fetch(endpoint + entity, {
      method: "DELETE",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "same-origin",
      body: JSON.stringify({
        "hard": hard
      }),
    }).then(r => r.json()).then(resp => {
      if (resp && resp.success) {
        if (!silent) {
          alert("Deleted an entity");
        }
        console.log("Deleted an entity.");
        location.reload();
      } else {
        alert("Failed to delete an entity. \nError: " + resp.message);
        console.log("Failed to delete an entity. \nError:", resp.message);
      }
    }).catch(err => {
      alert("Failed to delete an entity. \nFatal Error: " + err);
      console.log("Failed to delete an entity. \nFatal Error:", err);
    });
  }
}

function admin_entityAction(endpoint, entity, action, silent=false, conf_msg=null, reload=false) {
  if (confirm(conf_msg || "Are you sure you want to perform this action?")) {
    // ajax the action to the server
    fetch(endpoint + entity, {
      method: "PUT", // use PUT for actions
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "same-origin",
      body: JSON.stringify({
        action: action,
      }),
    }).then(r => r.json()).then(resp => {
      if (resp && resp.success) {
        if (!silent) {
          alert("Success: " + resp.message);
        }
        console.log("Success:", resp.message);
        if (reload) {
          location.reload();
        }
      } else {
        alert("Failed to perform an action. \nError: " + resp.message);
        console.log("Failed to perform an action. \nError:", resp.message);
      }
    }).catch(err => {
      alert("Failed to perform an action. \nFatal Error: " + err);
      console.log("Failed to perform an action. \nFatal Error:", err);
    });
  }
}

function admin_newEntity(endpoint, silent=false) {
  // construct a user model with the updated data
  let inps = document.getElementById("entity-edit-modal-new").getElementsByTagName("input");
  let updates = {};
  for (let i = 0; i < inps.length; i++) {
    let inp = inps[i];
    if (inp.type === "checkbox") {
      updates[inp.name] = inp.checked;
    } else {
      updates[inp.name] = inp.value;
    }
  }

  // ajax the action to the server
  fetch(endpoint, {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify(updates),
  }).then(r => r.json()).then(resp => {
    if (resp && resp.success) {
      if (!silent) {
        alert("Success: " + resp.message);
      }
      console.log("Success:", resp.message);
      location.reload();
    } else {
      alert("Failed to create a new entity. \nError: " + resp.message);
      console.log("Failed to create a new entity. \nError:", resp.message);
    }
  }).catch(err => {
    alert("Failed to create a new entity. \nFatal Error: " + err);
    console.log("Failed to create a new entity. \nFatal Error:", err);
  });
}

function admin_approveEntity(endpoint, entity) {
  admin_updateEntity(endpoint, entity, true);
  admin_entityAction(endpoint, entity, "APPROVE", false, "Are you sure you want to approve this entity?\n\nThis will allow all users of the site to view it.", true);
}

function admin_denyEntity(endpoint, entity) {
  admin_entityAction(endpoint, entity, "DENY", false, "Are you sure you want to deny this entity?\n\nThis will PERMANENTLY DELETE the entity from the entire system.", true);
}

function admin_silenceReporter(endpoint, entity) {
  admin_entityAction(endpoint, entity, "SILENCE_REPORT_AUTHOR", false, "Are you sure you want to silence this user?\n\nThis will prevent reports from this user appearing in the report admin. To undo this, change the 'Report Silence' field in the user admin.", true);
}

function admin_banCommentAuthor(endpoint, entity) {
  admin_entityAction(endpoint, entity, "BAN_COMMENT_AUTHOR", false, "Are you sure you want to ban this user?\n\nThis will prevent the user from logging in and using the site. To undo this, change the 'Banned' field in the user admin. This does not fully delete the user's account from the system. This does not fully delete the comment from the system, but it will be hidden from users. To fully delete the comment please hard delete it in the comment admin.", true);
}

function admin_deleteComment(endpoint, entity) {
  admin_entityAction(endpoint, entity, "DELETE_COMMENT", false, "Are you sure you want to delete this comment?\n\nThis will simply delete the comment and take no action against the offending user.", true);
}

function admin_dismissCommentReport(endpoint, entity) {
  admin_entityAction(endpoint, entity, "DISMISS_REPORT", false, "Are you sure you want to dismiss this report?\n\nThis will dismiss the report with no further action taken.", true);
}
