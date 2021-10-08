defaultLat = 42.3591;
defaultLng = -83.0665;
defaultZoom = 15;

/*----zoom levels----*/
/* 0:	 The Earth     */
/* 3:	 A continent   */
/* 4:	 Large islands */
/* 6:	 Large rivers  */
/* 10: Large roads   */
/* 15: Buildings     */
/*-------------------*/

var map = L.map('mapid').setView([defaultLat, defaultLng], 15);

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

  // user location - HIGHLY inaccurate on PC, likely better on mobile.
  map.addControl(L.control.locate({
    locateOptions: {
      enableHighAccuracy: true
    }
  }));

  
}

function userTools() {
  var marker
  // add a marker with a popup
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
      marker.bindPopup("test");
    }
  });

}

buildMap();
userTools();