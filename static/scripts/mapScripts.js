// Decorater Design Pattern
// NOTE: Typically, there would be an interface which BaseMap and Inter
class BaseMap {
  constructor(mapid, initialLat, initialLng, initialZoom) {
    // initialize map, retrieve tiles, perform basic setup
    this.map = new L.map(mapid).setView([initialLat, initialLng], initialZoom);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1IjoiY3NjNDExMGdyb3VwNSIsImEiOiJja3VjdmR4aWcxNGZjMzFvMzd2dHJhdnZmIn0.chI1y1ZmmmcdOX0nj1NtEQ'
    }).addTo(this.map);

    this.map.doubleClickZoom.disable();
  }
}

class BaseMapDecorator {
  // should be of type BaseMap, no way to enforce in JS
  constructor(baseMap) {
    console.log(baseMap);
    if (baseMap instanceof BaseMap || baseMap instanceof BaseMapDecorator) {
      this.map = baseMap.map;
    }
    else console.log(false)
  }
}

class Geocoding extends BaseMapDecorator {
  constructor(baseMap) {
    super(baseMap);
    // search map feature
    this.map.addControl(L.control.geocoder('pk.7963fb77afa804ed20fabb795cc1295d'));

    // find user location option
    this.map.addControl(L.control.locate({
      locateOptions: {
        enableHighAccuracy: true
      }
    }));
  }
}

class PinLoading extends BaseMapDecorator {
  constructor(baseMap, pins) {
    super(baseMap);
    this.loadPins(pins);
  }

  loadPins(pins) {
    var marker
    for (let pin of pins) {
      marker = new L.Marker([pin.latitude, pin.longitude]).addTo(map);
      marker.bindPopup(`<strong> ${pin.title}</strong><br>
      ${pin.city},${pin.state} <br>
      ${pin.date}<br>
      <a href=eventdetails.html>View Details</a>`)
    }
  }
}

//TODO: FIX THIS FUNCTION
class PinPlacing extends BaseMapDecorator {
  static marker;
  constructor(baseMap) {
    super(baseMap);
    // this.map.addEventListener('click', this.placePin);
  }
//   placePin(e) {
//     // on click, either remove existing pin from search or placement
//     // or place a new pin if there are no existing pins
//     console.log(e.latlng)
//     marker = new L.Marker(e.latlng, { draggable: true }).addTo(this);
//     console.log(this.tileLayer.maxZoom)
//     if (geocoder.markers.length == 1) {
//       geocoder.reset();
//       geocoder.collapse();
//     }
//     else if (marker) {
//       this.removeLayer(marker);
//       marker = false;
//     }
//     else {
      

//       // popup text
//       marker.bindPopup("test");
//     }
//   }
}



// defaultLat = 42.3591;
//   defaultLng = -83.0665;
// defaultZoom = 15;

/*----zoom levels----*/
/* 0:	 The Earth     */
/* 3:	 A continent   */
/* 4:	 Large islands */
/* 6:	 Large rivers  */
/* 10: Large roads   */
/* 15: Buildings     */
/*-------------------*/

// all controls related to the leaflet map & user location fider
// var map = L.map('mapid').setView([defaultLat, defaultLng], 15);



// function buildMap() {
//   // get map from mapbox
//   L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//     maxZoom: 18,
//     id: 'mapbox/streets-v11',
//     tileSize: 512,
//     zoomOffset: -1,
//     accessToken: 'pk.eyJ1IjoiY3NjNDExMGdyb3VwNSIsImEiOiJja3VjdmR4aWcxNGZjMzFvMzd2dHJhdnZmIn0.chI1y1ZmmmcdOX0nj1NtEQ'
//   }).addTo(map);

//   // remove double click zoom
//   map.doubleClickZoom.disable();

//   // find user location option
//   map.addControl(L.control.locate({
//     locateOptions: {
//       enableHighAccuracy: true
//     }
//   }));


// }

// function loadPins(pins) {
//   var marker
//   for (let pin of pins) {
//     marker = new L.Marker([pin.latitude, pin.longitude]).addTo(map);
//     marker.bindPopup(`<strong> ${pin.title}</strong><br>
//     ${pin.city},${pin.state} <br>
//     ${pin.date}<br>
//     <a href=eventdetails.html>View Details</a>`)
//   }

// }
// function userTools() {
//   // placeholder for user placed pin
//   var marker

//   // on click, either remove existing pin from search or placement
//   // or place a new pin if there are no existing pins
//   map.on('click', function (e) {
//     if (geocoder.markers.length == 1) {
//       geocoder.reset();
//       geocoder.collapse();
//     }
//     else if (marker) {
//       map.removeLayer(marker);
//       marker = false;
//     }
//     else {
//       marker = new L.Marker(e.latlng, { draggable: true }).addTo(map);

//       // popup text
//       marker.bindPopup("test");
//     }
//   });

// }

// buildMap();
// userTools();