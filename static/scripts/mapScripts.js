/*----zoom levels----*/
/* 0:	 The Earth     */
/* 3:	 A continent   */
/* 4:	 Large islands */
/* 6:	 Large rivers  */
/* 10: Large roads   */
/* 15: Buildings     */
/*-------------------*/


// Decorater Design Pattern
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
  // constructor should take a parameter of type BaseMap 
  // but there is no way to enforce interfaces in JS
  constructor(baseMap) {
    if (baseMap instanceof BaseMap || baseMap instanceof BaseMapDecorator) {
      this.map = baseMap.map;
    }
    else return false;
  }
}

class Geocoding extends BaseMapDecorator {
  // adds geocoding functionality to the map
  // including searching for locations
  // and finding user location
  constructor(baseMap) {
    super(baseMap);
    // search for address
    const geocoder = L.control.geocoder('pk.7963fb77afa804ed20fabb795cc1295d').addTo(this.map);

    // find user location
    this.map.addControl(L.control.locate({
      locateOptions: {
        enableHighAccuracy: true
      }
    }));

    // collapse search bar on click
    this.map.addEventListener('click', function () {
      geocoder.reset();
      geocoder.collapse();
    });
  }
}

class PinLoading extends BaseMapDecorator {
  // adds the ability to load pins from the database
  // parsed from JSON in HTML and sent to this function
  constructor(baseMap, pins) {
    super(baseMap);
    this.loadPins(pins);
  }

  loadPins(pins) {
    let marker = null;
    for (let pin of pins) {
      let form =
      `<form id="view-details" method="POST">` +
      `<a href="/event-details/${pin.id}" name="id" value="${pin.id}">View Details</a>` +
      `<input type="hidden" name="eventid" value=${pin.id}>` +
      `</form>`

      let bookmarkBtn = 
      `<div class="buttoncontainer">` +
      `<form id="addBookmark" action="/addBookmark/${pin.id}" method="POST">` + 
      `<input type="hidden" name="eventid" value="${pin.id}">` +
      `</form>` +
      `<button type='submit' id="bmbutton" form="addBookmark"><i class="far fa-bookmark"></i></button>` +
      `</div>`
      
      marker = new L.Marker([pin.latitude, pin.longitude]).addTo(this.map);
      marker.bindPopup(
        `<strong>${pin.title}</strong>` + 
        bookmarkBtn + `<br>` +
        `${pin.city}, ${pin.state}<br>` + 
        `${pin.date}<br>` +
        `${form}`)
    }
  }
}

class PinPlacing extends BaseMapDecorator {
  // adds the ability for the user to place pins on the map
  constructor(baseMap, retriveLatLng) {
    super(baseMap);
    this.placePin(retriveLatLng)
  }

  placePin(retriveLatLng) {
    // on click, either remove placed pin from search or placement
    // or place a new pin if there are no placed pins
    // can retrieve the latitude and longitude of the placed pin if desired
    this.map.addEventListener('click', function (e) {
      let marker = null;

      this.eachLayer(function (layer) {
        if (layer instanceof L.Marker) {
          marker = layer;
        }
      });

      if (marker) {
        this.removeLayer(marker);
      }
      else {
        marker = new L.Marker(e.latlng, { draggable: true }).addTo(this);
        marker.bindPopup('Your event will take place here!');

        if (retriveLatLng) {
          let lat = document.getElementById('latitude');
          let lng = document.getElementById('longitude');

          lat.value = e.latlng['lat']
          lng.value = e.latlng['lng'];

          // move the label out of the input on map click
          lat.previousElementSibling.classList.add('move-label');
          lng.previousElementSibling.classList.add('move-label');
        }
      }
    });
  }
}