frappe.get_user_location = async function () {
  return new Promise((resolve, reject) => {
    // check geolocation api is available
    if (!navigator.geolocation) {
      frappe.throw(__("Geolocation is not enabled."));
      reject();
    }

    // if((window.location.href.match(/:[0-9]+/g)||[]).length) {
    //   // return client location for local test. comment in production
    //   resolve(
    //     [ '12.880834','80.215677',]
    //   );
    //   return
    // }   
        navigator.geolocation.getCurrentPosition(
        (loc) => {
          // console.log([loc.coords.latitude, loc.coords.longitude]);
          resolve([loc.coords.latitude, loc.coords.longitude]);
        },
        (err) => {
          frappe.throw(err.message);
          reject([]);
        }
      );
  });
};


frappe.haversineDistance = ([lat1, lon1], [lat2, lon2], isMiles = false) => {
  const toRadian = (angle) => (Math.PI / 180) * angle;
  const distance = (a, b) => (Math.PI / 180) * (a - b);
  const RADIUS_OF_EARTH_IN_KM = 6371;

  const dLat = distance(lat2, lat1);
  const dLon = distance(lon2, lon1);

  lat1 = toRadian(lat1);
  lat2 = toRadian(lat2);

  // Haversine Formula
  const a =
    Math.pow(Math.sin(dLat / 2), 2) +
    Math.pow(Math.sin(dLon / 2), 2) * Math.cos(lat1) * Math.cos(lat2);
  const c = 2 * Math.asin(Math.sqrt(a));

  let finalDistance = RADIUS_OF_EARTH_IN_KM * c;

  if (isMiles) {
    finalDistance /= 1.60934;
  }

  console.log("Distance to client location in km - ", finalDistance);
  return finalDistance;
};
