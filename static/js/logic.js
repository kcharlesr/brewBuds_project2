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
  starbucks: new L.LayerGroup(),
  zipcodes: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5,
  layers: [
    layers.brewery,
    layers.starbucks,
    layers.zipcodes
  ]
});

// Add our 'lightmap' tile layer to the map
lightmap.addTo(map);

// Create an overlays object to add to the layer control
var overlays = {
  "Brewery": layers.brewery,
  "Starbucks": layers.starbucks,
  "Ideal ZIP Code": layers.zipcodes
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
  starbucks: L.ExtraMarkers.icon({
    icon: "ion-coffee",
    iconColor: "white",
    markerColor: "green",
    shape: "circle"
  }),
  zipcodes: L.ExtraMarkers.icon({
    icon: "ion-home",
    iconColor: "white",
    markerColor: "red",
    shape: "circle"
  })
};

// Perform an API call to the Citi Bike Station Information endpoint
d3.json("http://127.0.0.1:5000/api/v1.0/breweries", function(data) {
    console.log(data);
    var breweryData = data.features;

    // Loop through the stations (they're the same size and have partially matching data)
    for (var i = 0; i < breweryData.length; i++) {

      var location = breweryData[i].geometry
      var name = breweryData[i].properties
      var brewery = "brewery"
      // Create a new marker with the appropriate icon and coordinates
      var newMarker = L.marker([location.coordinates[1], location.coordinates[0]], {
        icon: icons[brewery]
      });

      // Add the new marker to the appropriate layer
      newMarker.addTo(layers[brewery]);

      // Bind a popup to the marker that will  display on click. This will be rendered as HTML
      newMarker.bindPopup(`<h5>${name.name}</h5>`);
    }

    // Call the updateLegend function, which will... update the legend!
  });

  d3.json("http://127.0.0.1:5000/api/v1.0/starbucks", function(data) {
    console.log(data);
    var starbucksData = data.features;

    // Loop through the stations (they're the same size and have partially matching data)
    for (var i = 0; i < starbucksData.length; i++) {

      var location = starbucksData[i].geometry
      var name = starbucksData[i].properties
      var starbucks= "starbucks"
      // Create a new marker with the appropriate icon and coordinates
      var newMarker = L.marker([location.coordinates[1], location.coordinates[0]], {
        icon: icons[starbucks]
      });

      // Add the new marker to the appropriate layer
      newMarker.addTo(layers[starbucks]);
    }
  });

  d3.json("/static/zips.json", function(zipdata){
      console.log(zipdata)
      for (var i = 0; i < zipdata.length; i++) {
        var location = zipdata[i]
        var zipcodes= "zipcodes"
        // Create a new marker with the appropriate icon and coordinates
        var newMarker = L.marker([location.coordinates[0], location.coordinates[1]], {
          icon: icons[zipcodes]
       });

      // Add the new marker to the appropriate layer
        newMarker.addTo(layers[zipcodes])
        newMarker.bindPopup(`<h5>${location.zip}</h5>`);
      }
   });


  // function getColor(income) {
  //   return d > 200000 ? '#0000ff' :
  //          d > 170000 ? '#1a0fe6' :
  //          d > 150000  ? '#331fcc' :
  //          d > 140000  ? '#4c2eb2' :
  //          d > 130000  ? '#5936a6' :
  //          d > 120000  ? '#8c5473' :
  //          d > 110000 ? '#995c66' :
  //          d > 100000  ? '#b26b4d' :
  //          d > 90000  ? '#bf7340' :
  //          d > 80000  ? '#d98226' :
  //          d > 70000  ? '#f2910d' :
  //                     '#ff9900';
  // };
  

// d3.json("http://127.0.0.1:5000/api/v1.0/demo", function(demoData) {
  
  d3.json("/static/merge.json", function(data) {
    // Creating a geoJSON layer with the retrieved data
    // var demo = demoData.features
    L.geoJson(data, {
      // Style each feature (in this case a neighborhood)
      style: function(feature) {
        return {
          color: "white",
          // Call the chooseColor function to decide which color to color our neighborhood (color based on borough)
          // fillColor: chooseColor(feature.properties.borough),
          fillColor: "red",
          fillOpacity: 0.5,
          weight: 1.5
        };
      },
      // Called on each feature
      onEachFeature: function(feature, layer) {
        // Set mouse events to change map styling
        layer.on({
          // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
          mouseover: function(event) {
            layer = event.target;
            layer.setStyle({
              fillOpacity: 0.9
            });
          },
          // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
          mouseout: function(event) {
            layer = event.target;
            layer.setStyle({
              fillOpacity: 0.5
            });
          },
          // When a feature (neighborhood) is clicked, it is enlarged to fit the screen
          click: function(event) {
            map.fitBounds(event.target.getBounds());
          }
        });
        // Giving each feature a pop-up with information pertinent to it
        layer.bindPopup("<h1>" + feature.properties.zipcode+ "</h1> <hr> <h2>" + feature.properties.borough + "</h2>");
  
      }
    }).addTo(map);
  }); 