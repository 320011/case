function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

function refreshPlaylist(id) {
  let confirmation = confirm("You are about to refresh this playlist. This will re-randomise all cases in the playlist, and you will lose your current progress.\n\nAre you sure you want to proceed?\nThis action cannot be undone.");
  if (confirmation) {
    $.ajax({
      type: "POST",
      url: "/cases/api/v1/refresh_playlist/",
      dataType: "json",
      data: {
        "playlist_id": id
      },
      success: function (resp) {
        if (resp.success) {
          alert(resp.message);
          window.location.reload(false);
        }else{
          alert(resp.message)
        }
      }
    });
  }
}

function deletePlaylist(id) {
  let confirmation = confirm("You are about to delete this playlist.\n\nAre you sure you want to proceed?\nThis action cannot be undone.");
  if (confirmation) {
    $.ajax({
      type: "POST",
      url: "/cases/api/v1/delete_playlist/",
      dataType: "json",
      data: {
        "playlist_id": id
      },
      success: function (resp) {
        if (resp.success) {
          alert("Playlist deleted!");
          window.location.reload(false);
        } else {
          alert("An error has occurred. Please try again.")
        }
      }
    });
  }
}


$('#create_playlist').click(function () {
  $.ajax({
    type: "POST",
    url: "/cases/api/v1/new_playlist/",
    data: {
      "tag_id": $("#id_field").val()
    },
    success: function (resp) {
      if (resp.success) {
        alert(resp.message);
        window.location.reload(false);
      } else {
        alert(resp.message);
      }
    }
  });
})