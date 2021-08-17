// Copyright (c) 2021, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
  set_location_cf: function name(frm) {
    const zoom = 15;
    let fld = frm.get_field("client_location_cf"),
      _map = fld.map;

    let lat_long = /\/\@(.*),(.*),/.exec(frm.doc.client_location_url_cf);

    if (lat_long && lat_long.length == 3) {
      let point = L.marker(lat_long.slice(1)).toGeoJSON();
      L.geoJSON(point).addTo(_map);
      _map.setView(lat_long.slice(1), zoom);

      //
      frm.set_value("client_location_cf", JSON.stringify(point));
    } else {
      frappe.throw(
        __(
          `The url does not contain valid longitide, latitude. (e.g. /@24.645284,46.7002566,17z/) 
          Please paste a google map link url in the Client Location Url in order to set marker.`
        )
      );
    }
  },
});
