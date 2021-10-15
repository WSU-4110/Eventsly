defaultLat = 42.3591;
defaultLng = -83.0665;
defaultZoom = 15;
myLat = 0;
myLong = 0;

/*----zoom levels----*/
/* 0:	 The Earth     */
/* 3:	 A continent   */
/* 4:	 Large islands */
/* 6:	 Large rivers  */
/* 10: Large roads   */
/* 15: Buildings     */
/*-------------------*/

// all controls related to the leaflet map & user location fider
var map = L.map('mapid').setView([defaultLat, defaultLng], 15);

// all controls related only to the search map feature
var geocoder = L.control.geocoder('pk.7963fb77afa804ed20fabb795cc1295d').addTo(map);

function buildMap() {
  // get map from mapbox
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiY3NjNDExMGdyb3VwNSIsImEiOiJja3VjdmR4aWcxNGZjMzFvMzd2dHJhdnZmIn0.chI1y1ZmmmcdOX0nj1NtEQ'
  }).addTo(map);

  // remove double click zoom
  map.doubleClickZoom.disable();

  // find user location option
  map.addControl(L.control.locate({
    locateOptions: {
      enableHighAccuracy: true
    }
  }));
}

function userTools() {
  // placeholder for user placed pin
  var marker
  var marker2 // static pin marking WSU

  marker2 = new L.Marker([42.358768, -83.071228]).addTo(map);


  // on click, either remove existing pin from search or placement
  // or place a new pin if there are no existing pins
  map.on('click', function (e) {
    if (geocoder.markers.length == 1) {
      geocoder.reset();
      geocoder.collapse();
    }
    else if (marker) {
      map.removeLayer(marker);
      marker = false;
    }
    else {
      marker = new L.Marker(e.latlng, { draggable: true }).addTo(map);
      myLat = e.latlng;

      // popup text
      marker.bindPopup(myLat);
    }
  });

}

buildMap();
userTools();