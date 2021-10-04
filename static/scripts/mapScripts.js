// default to WSU coordinates
var defaultLat = 42.3591
var defaultLong = -83.0665

var map = L.map('mapid').setView([defaultLat, defaultLong], 15);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoiY3NjNDExMGdyb3VwNSIsImEiOiJja3VjdmR4aWcxNGZjMzFvMzd2dHJhdnZmIn0.chI1y1ZmmmcdOX0nj1NtEQ'
}).addTo(map);

// geolocation - HIGHLY inaccurate on PC, likely better on mobile.
map.addControl(L.control.locate({
  locateOptions: {
          enableHighAccuracy: true
}}));