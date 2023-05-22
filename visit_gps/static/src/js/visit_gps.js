odoo.define('visit_gps.geo', function (require) {
"use strict";
var rpc = require('web.rpc');
$(document).on('click', '#btnSubmit', function () {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
        alert("Geolocation is not supported by this browser.");
    }

    });

    function showPosition(position) {
        $("#latitud").val(position.coords.latitude).change();
        $("#longitud").val(position.coords.longitude).change();
        document.getElementById("gps").innerHTML = $("#latitud").val() + ","+ $("#longitud").val();
        savLatLon();
    }

function savLatLon(){
    // document.getElementById("latitud").value = lat;
    var eF = document.getElementById("latitud");
    eF.focus();
    const eventlat = new KeyboardEvent('keydown', {
      key: 'Enter',
      code: 'Enter',
      which: 13,
      keyCode: 13,
      charCode: 13,
      bubbles: true,
      cancelable: true,
    });
    eF.dispatchEvent(eventlat);

    var eF = document.getElementById("longitud");
    eF.focus();
    const eventlon = new KeyboardEvent('keydown', {
      key: 'Enter',
      code: 'Enter',
      which: 13,
      keyCode: 13,
      charCode: 13,
      bubbles: true,
      cancelable: true,
    });
    eF.dispatchEvent(eventlon);
}

});
