var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
});

// Initialize all of the LayerGroups we'll be using
var layers = {
  brewery: new L.LayerGroup(),
  // starbucks: new L.LayerGroup(),
  // zipcodes: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5,
  layers: [
    layers.brewery,
    // layers.starbucks,
    // layers.zipcodes
  ]
});

// Add our 'lightmap' tile layer to the map
lightmap.addTo(map);

// Create an overlays object to add to the layer control
var overlays = {
  "Brewery": layers.brewery,
  // "Starbucks": layers.starbucks,
  // "Zip Codes": layers.zipcodes
};

L.control.layers(null, overlays).addTo(map);

// Initialize an object containing icons for each layer group
var icons = {
  brewery: L.ExtraMarkers.icon({
    icon: "ion-beer",
    iconColor: "white",
    markerColor: "blue",
    shape: "cirlce"
  }),
  // starbucks: L.ExtraMarkers.icon({
  //   icon: "ion-cafe",
  //   iconColor: "white",
  //   markerColor: "green",
  //   shape: "circle"
  // }),
  // zipcodes: L.ExtraMarkers.icon({
  //   icon: "ion-home",
  //   iconColor: "white",
  //   markerColor: "red",
  //   shape: "circle"
  // })
};

// Perform an API call to the Citi Bike Station Information endpoint
d3.json("http://127.0.0.1:5000/api/v1.0/breweries", function(data) {
    console.log(data);
    var breweryData = data.features;

    // Loop through the stations (they're the same size and have partially matching data)
    for (var i = 0; i < breweryData.length; i++) {

      var location = breweryData[i].geometry
      var name = breweryData[i].properties
      // Create a new marker with the appropriate icon and coordinates
      var newMarker = L.marker([location.coordinates[1], location.coordinates[0]], {
        icon: icons["brewery"]
      });

      // Add the new marker to the appropriate layer
      newMarker.addTo(layers[brewery]);

      // Bind a popup to the marker that will  display on click. This will be rendered as HTML
      newMarker.bindPopup(`<h2>${name.name}`);
    }

    // Call the updateLegend function, which will... update the legend!
  });



