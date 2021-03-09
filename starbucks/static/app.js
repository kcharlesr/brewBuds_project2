// kcharlesr



d3.csv("../plot_us_stores.csv").then(function(data) {
        // data.Name = +data.Name;
        // data.Street1 = +data.Street1;
        // data.CountrySubdivisionCode = +data.CountrySubdivisionCode;
        // data.CountryCode = +data.CountryCode;
        // data.PostalCode = +data.PostalCode;
        // data.Longitude = +data.Longitude;
        // data.Latitude - +data.Latitude;
        console.log(data);
        // console.log(data.Latitude)

         
         var coordinates = data.forEach(function(data) {
          console.log(`${data.Longitude}: ${data.Latitude}`);
        });
        console.log(coordinates);

        var myMap = L.map("map", {
          center: [37.0902, -95.7129],
          zoom: 4
        });
        
        // Add a tile layer (the background map image) to our map
        // We use the addTo method to add objects to our map
        L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
          attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
          tileSize: 512,
          maxZoom: 18,
          zoomOffset: -1,
          id: "mapbox/streets-v11",
          accessToken: API_KEY
        }).addTo(myMap);
        
        // Create a new marker
        // Pass in some initial options, and then add it to the map using the addTo method
        var marker = L.marker([], {
          draggable: true,
          title: "My First Marker"
        }).addTo(myMap);
        
        // Binding a pop-up to our marker
        marker.bindPopup("Hello There!");

});







