/*
 * Load file from address and then call 'callback' function on received
 * response.
 * Args:
 *  file: string with filename or address.
 *  callback: pointer to function to call after receiving response.
 */
function load_file(file, callback) {   
  // Create request
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', file, true);
  // Add callback function.
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
        callback(xobj.responseText);
    }
  };
  xobj.send(null);  
}

/*
 * Function which receive json data of the route and returns OpenLayers feature.
 * Args:
 *  json_data: GeoJSON object.
 * Retunrs:
 *  Array of ol.Feature's
 */
function create_route(json_data, color=[100, 200, 50]){
  var route = new ol.format.GeoJSON().readFeatures(json_data, {
      featureProjection: 'EPSG:3857'
  });

  // Get element from the array and set type
	route = route[0];

  // Get coordinates for further points generation
	routeCoords = route.getGeometry().getCoordinates();

  // Create line
  var line = new ol.geom.LineString(routeCoords);
  var lineFeature = new ol.Feature(line);
	lineFeature.set('type', 'route');
	lineFeature.setStyle(
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        width: 5,
        color: 'rgba(' + color[0] + ', ' + color[1] + ', ' + color[2] + ', 0.5)'
      }),
    })
  );


  // Array of points. Used for keyboard orientation on the map.
  var features = Array();
  features.push(lineFeature);

  // Create points
  for(i = 0; i < routeCoords.length; i++){
    var point = new ol.Feature({
      geometry: new ol.geom.Point(routeCoords[i]),
      type: 'point',
    });
    point.id = i
		point.setStyle(
      new ol.style.Style({
        image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({
            color: 'rgba(' + color[0] + ', ' + color[1] + ', ' + color[2] + 
                       ', 1)'
          }),
          stroke: new ol.style.Stroke({
            color: '#555', 
            width: 1
          })
        })
      })
    )
    features.push(point);
  }

  return features;
}

/*
 * Adds feature to the map.
 * Args:
 *  feat_data: GeoJSON reponse.
 */
function add_route(feat_data, color=[100, 200, 50]){
  var features = create_route(feat_data, color);
  
  vec_layer.getSource().addFeatures(features);
}

/*
 * Create popup message.
 * Args:
 *  feature: ol.Feature object. 
 *  element: html element which is used as content container (div).
 */
function create_popup(feature, element){
  if (feature && feature.get('type') == 'point') {
    var coordinates = feature.getGeometry().getCoordinates();
		console.log(coordinates);
    get_address(coordinates);
    popup.setPosition(coordinates);
    var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinates, 'EPSG:3857', 'EPSG:4326'));
    content = '<p>Information:</p><code>' + hdms +
        '</code>';
    content = content + '<p id="hidden_id">' + feature.id + '</p>'
    // Add coordinates to Point information table
	  var point_table = document.getElementById('point_coords');
    if(point_table){
      point_table.innerHTML = '<code>' + hdms + '</code>';
    }
    $(element).popover({
      'placement': 'top',
      'html': true,
      'content': function (){
        return content;
      }
    });
    $(element).popover('show');
  } else {
    $(element).popover('destroy');
  }
}

/*
 * Listener used for moving popup box from point to point by keyboard.
 * Args:
 *  e: keyboard event.
 */
function key_listener(e) {
  // If popup already exists
  if ($(popup_element).data()['bs.popover'].tip().hasClass('in')){
    // Get id from hidden HTML code
    var id = parseInt(document.getElementById('hidden_id').innerText);

    // Decide which key pressed
    if (e.keyCode == 37){
      console.log("Left " + id);
      create_popup(points[id - 1], $(popup_element))
    } else if (e.keyCode == 39){
      console.log("Right " + id);
      create_popup(points[id + 1], $(popup_element))
    } else {
      console.log("Not implemented.");
    }
  }
}

/*
 * Returns a random integer between min (inclusive) and max (inclusive)
 * Using Math.round() will give you a non-uniform distribution!
 * Args:
 * 	min: integer number
 * 	max: integer number
 * Retunrs:
 * 	Integer number between two values.
 */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/*
 * Function for map initialization. This function create global variable 'map'
 * which can be user for further interaction with map.
 * Args:
 *  center: array with to point which will be map center
 */
function init_map(center){
  // Create styles
  styles = {
      'point': new ol.style.Style({
        image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({
            color: 'rgba(60, 160, 10, 0.9)'
          }),
          stroke: new ol.style.Stroke({
            color: '#555', 
            width: 1
          })
        })
      }),

      'route': new ol.style.Style({
        stroke: new ol.style.Stroke({
          width: 5,
          color: 'rgba(100, 200, 50, 0.9)'
        }),
      })
  };

  // Create vector layear
  vec_layer = new ol.layer.Vector({
    source: new ol.source.Vector(),
    rendererOptions: { zIndexing: true }
  });
  vec_layer.setStyle(styles);

  // Create Map
  map = new ol.Map({
    target: 'map',
    view: new ol.View({
      center: ol.proj.fromLonLat(center),
      zoom: 15,
      minZoom: 2,
      maxZoom: 19
    }),

    // Add layers
    layers: [
      new ol.layer.Tile({
        source: new ol.source.XYZ({
          url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/' + 
            '256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic25hc2hlIiwiYSI6ImRF' + 
            'WFVLLWcifQ.IcYEbFzFZGuPmMDAGfx4ew'
        })
      }),
      vec_layer
    ],
  });

  // Create popup and add overlay layer to the map
	popup_element = document.getElementById('popup');

  popup = new ol.Overlay({
    element: popup_element,
    positioning: 'bottom-center',
    stopEvent: false,
    offset: [-2, -8]
  });
  map.addOverlay(popup);

  // Add listener to the map to react on the mouse click.
  map.on('click', function(evt) {
    var feature = map.forEachFeatureAtPixel(evt.pixel,
        function(feature) {
          return feature;
        }
    )
    create_popup(feature, popup_element)
  });

  // Add keyboard listener. To allow user to manipulate with popup box with key
  // arrows.
  window.addEventListener("keydown", key_listener, false);
};

/*
 * Gets address for the coordinates.
 * Args:
 *  coords: array with to float numbers, latitude and longitude.
 */
function get_address(coords){
  // Get response from API
  coords = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
  lon = coords[0];
  lat = coords[1];
  load_file(
      'http://open.mapquestapi.com/nominatim/v1/reverse.php?key=xKWXF' + 
      'zDoNFf4q9DbKXh6zPpfOkqAwb5A&format=json&lat=' + lat + '&lon=' + 
      lon, 
      function(data){
        data = JSON.parse(data);
        console.log(data['display_name'])
	      var element = document.getElementById('point_address');
        if(element){
          element.textContent = data['display_name'];
        }
      }
  );

}

/*
 * Loads route from address. As a response should be received GeoJSON object.
 * Args:
 *  address: string representing address which should be requested for a data.
 */
function load_route(address){
  load_file(address, add_route);
}
    

// Call response function when loading is finished
function draw_map(response, center){
  // Some initial information 
  var zoom = 15;
  // var center = [14.398977756500244, 50.07859060687297];
  var center = JSON.parse(center);

  // Load data
  var geojsonObject = JSON.parse(response);
  console.log(response);
  // var lineFeature = add_route(geojsonObject);

	routeCoords = lineFeature.getGeometry().getCoordinates();
	routeLength = routeCoords.length;

  // Define styles for features
  // Styles for points
  var styles = {
      'start_marker': new ol.style.Style({
        // graphicZIndex: 100,
        // zIndex: 100,
        image: new ol.style.Circle({
          radius: 7,
          snapToPixel: false,
          fill: new ol.style.Fill({color: '#13E821'}),
          stroke: new ol.style.Stroke({
            color: '#888', width: 2
          })
        })
      }),

      'end_marker': new ol.style.Style({
        // graphicZIndex: 100,
        // zIndex: 100,
        image: new ol.style.Circle({
          radius: 7,
          snapToPixel: false,
          fill: new ol.style.Fill({color: 'yellow'}),
          stroke: new ol.style.Stroke({
            color: '#888', width: 2
          })
        })
      }), 
      
      'point': new ol.style.Style({
        // graphicZIndex: 99,
        // zIndex: 99,
        image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({
            //color: '#800',
            color: 'rgba(60, 160, 10, 0.9)'
          }),
          stroke: new ol.style.Stroke({
            color: '#555', 
            width: 1
          })
        })
      }),

      'line': new ol.style.Style({
        stroke: new ol.style.Stroke({
          width: 5,
          color: 'rgba(100, 200, 50, 0.9)'
        }),
      })
  };

  // Create start and end marker
  var startMarker = new ol.Feature({
    type: 'start_marker',
    geometry: new ol.geom.Point(routeCoords[0])
  });

  var endMarker = new ol.Feature({
    type: 'end_marker',
    geometry: new ol.geom.Point(routeCoords[routeLength - 1])
  });


	// Set styles
  startMarker.setStyle(styles['start_marker']);
  endMarker.setStyle(styles['end_marker']);
  lineFeature.setStyle(styles['line']);

  // Create vector layear
  var vector_layer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: [lineFeature, startMarker, endMarker]
    }),
    rendererOptions: { zIndexing: true }
  });

  // Array of points. Used for keyboard orientation on the map.
  var points = Array();
  // Create features
  for(i = 0; i < routeCoords.length; i++){
    var point = new ol.Feature({
      geometry: new ol.geom.Point(routeCoords[i]),
      type: 'point',
    });
    point.id = i
    point.setStyle(styles['point']);
    vector_layer.getSource().addFeature(point);
    points.push(point);
  }

  // Create map
  var map = new ol.Map({
    target: 'map',
    view: new ol.View({
      center: ol.proj.fromLonLat(center),
      zoom: zoom,
      minZoom: 2,
      maxZoom: 19
    }),

    // Add layers
    layers: [
      new ol.layer.Tile({
        source: new ol.source.XYZ({
          url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic25hc2hlIiwiYSI6ImRFWFVLLWcifQ.IcYEbFzFZGuPmMDAGfx4ew'
        })
      }),
      vector_layer
    ],
  });

  // Load airspaces
  load_file('../static/polygon.gml', function (response){
    var airspaces_layer = new ol.layer.Vector({
      source: new ol.source.Vector(),
			style: new ol.style.Style({
        strokeColor: '#bada55'
      })
    });
    // console.log(response);
    response = (new DOMParser()).parseFromString(response, 'text/xml');
    var airspaces = new ol.format.WMSGetFeatureInfo().readFeatures(response);
    console.log('Airspaces:');
    console.log(airspaces);
    console.log('Create airspaces layer.');
    airspaces_layer.getSource().addFeatures(airspaces);
    console.log('Adding airspaces layer to the map.');
    map.addLayer(airspaces_layer);
  });

	var element = document.getElementById('popup');

  var popup = new ol.Overlay({
    element: element,
    positioning: 'bottom-center',
    stopEvent: false,
    offset: [-2, -8]
  });
  map.addOverlay(popup);

  function create_popup(feature, element){
    if (feature && feature.get('type') == 'point') {
      var coordinates = feature.getGeometry().getCoordinates();
			console.log(coordinates);
      get_address(coordinates);
      popup.setPosition(coordinates);
      var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
                          coordinates, 'EPSG:3857', 'EPSG:4326'));
      content = '<p>Information:</p><code>' + hdms +
                              '</code>';
      content = content + '<p id="hidden_id">' + feature.id + '</p>'
      // Add coordinates to Point information table
	    var point_table = document.getElementById('point_coords');
      point_table.innerHTML = '<code>' + hdms + '</code>';
      $(element).popover({
        'placement': 'top',
        'html': true,
        'content': function (){
          return content;
        }
      });
      $(element).popover('show');
    } else {
      $(element).popover('destroy');
    }
  }

  window.addEventListener("keydown", checkKeyPressed, false);
   
  function checkKeyPressed(e) {
    // If popup already exists
    if ($(element).data()['bs.popover'].tip().hasClass('in')){
      // Get id from hidden HTML code
      var id = parseInt(document.getElementById('hidden_id').innerText);

      // Decide which key pressed
      if (e.keyCode == 37){
        console.log("Left " + id);
        create_popup(points[id - 1], $(element))
      } else if (e.keyCode == 39){
        console.log("Right " + id);
        create_popup(points[id + 1], $(element))
      } else {
        console.log("Upside-down");
      }
    }
  }

  // map.on('keydown', function(e){
    //console.log(e.keyCode);
  //});

	// display popup on click
  map.on('click', function(evt) {
    // console.log(evt);
    // var pos = evt.coordinate;        
    // var point =  new ol.geom.Point(pos.lon, pos.lat);
    // var closest = Math.min(vector_layer.getSource().getFeatures().map(
          // function(feature) {
            // console.log(feature.getGeometry().getClosestPoint(pos));
            // return feature.getGeometry().getClosestPoint(point);
    // }));
    // var closest = lineFeature.getGeometry().getClosestPoint(pos);
    // console.log(pos);
    // console.log(closest);
    var feature = map.forEachFeatureAtPixel(evt.pixel,
        function(feature) {
          return feature;
        })
    create_popup(feature, element)
  });

};

