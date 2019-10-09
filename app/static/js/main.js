window.onload = function() {
  return  // disabled

  _attach_on_form_submit_event_listener("#gathering_form", gathering_callback)
  _attach_on_form_submit_event_listener("#identifying_form", identifying_callback)

  var data = JSON.parse(sessionStorage.getItem("data"))

  if (data) {
    if ("gathering" in data) {
      var gathering_data = data.gathering

      document.getElementById("gathering_roll").value = gathering_data.roll
      document.getElementById("travel_method").value = gathering_data.travel_method
      document.getElementById("terrain_type").value = gathering_data.terrain_type
    }

    if ("identifying" in data) {
      var identifying_data = data.identifying

      document.getElementById("identify_roll").value = identifying_data.roll
      document.getElementById("identify_ingredient").value = identifying_data.ingredient
    }
  }
}

function gathering_callback() {
  var roll = document.getElementById("gathering_roll").value
  var travel_method = document.getElementById("travel_method").value
  var terrain_type = document.getElementById("terrain_type").value

  var data = {
    "gathering": {
      "roll": roll,
      "travel_method": travel_method,
      "terrain_type": terrain_type
    }
  }

  sessionStorage.setItem("data", JSON.stringify(data))
}

function identifying_callback() {
  var roll = document.getElementById("identify_roll").value
  var ingredient = document.getElementById("identify_ingredient").value

  var data = {
    "identifying": {
      "roll": roll,
      "ingredient": ingredient
    }
  }

  sessionStorage.setItem("data", JSON.stringify(data))
}

function _attach_on_form_submit_event_listener(element_query, callback) {
  var ele = document.querySelector(element_query)
  if (ele.addEventListener) {
    ele.addEventListener("submit", callback, false);  //Modern browsers
  } else if (ele.attachEvent) {
    ele.attachEvent('onsubmit', callback);            //Old IE
  }
}
