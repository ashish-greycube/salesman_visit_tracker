// Copyright (c) 2021, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Visit", {
  before_submit: function (frm) {
    if (!["Completed", "Cancelled"].includes(frm.doc.status)) {
      frappe.throw(
        __(
          "Invalid status <strong>{0}</strong>. Can submit Visit only when status is Completed or Cancelled.",
          [frm.doc.status]
        )
      );
    }
  },

  validate: function (frm) {
    return new Promise((resolve, reject) => {
      let client_location =
          frm.doc.__onload && frm.doc.__onload.client_location_cf,
        max_distance_from_client_location =
          (frm.doc.__onload &&
            frm.doc.__onload.max_distance_from_client_location) ||
          0;

      if (!client_location || frm.doc.status == "Cancelled") {
        resolve(true);
      } else {
        frappe.get_user_location().then((user_loc) => {
          let client_loc = client_location.map((r) => parseFloat(r));
          // console.log("user location", user_loc);
          // console.log("client loc", client_loc);

          let distance = frappe.haversineDistance(client_loc, user_loc) * 1000;
          if (distance > max_distance_from_client_location) {
            frappe.throw(
              `User location error. User is ${distance.toFixed()}m away from client's location.`
            );
            reject();
          } else {
            resolve();
          }
        });
      }
    });
  },
});
