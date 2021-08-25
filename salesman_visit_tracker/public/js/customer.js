// Copyright (c) 2021, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
  set_location_cf: function name(frm) {
    const zoom = 15;
    let fld = frm.get_field("client_location_cf"),
      _map = fld.map;

    let lat_long = /\/\@(.*),(.*),/.exec(frm.doc.client_location_url_cf);

    if (lat_long && lat_long.length == 3) {
      var geojsonFeature = {
        type: "Feature",
        properties: {
          name: "Customer Location",
          popupContent: "This is customer's location",
        },
        geometry: {
          type: "Point",
          coordinates: lat_long.slice(1),
        },
      };
      let layer = L.geoJSON(geojsonFeature);
      layer.addTo(_map);
      fld.editableLayers.addLayer(layer);
      fld.set_value(JSON.stringify(fld.editableLayers.toGeoJSON()));
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
