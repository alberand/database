// Load json file with data
function loadJSON(file, callback) {   
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  console.log("Start loading ");
  xobj.open('GET', file, true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
        callback(xobj.responseText);
    }
  };
  xobj.send(null);  
}
    

// Call response function when loading is finished
function draw_map(response, center){
  // Some initial information 
  var zoom = 15;
  // var center = [14.398977756500244, 50.07859060687297];
  var center = JSON.parse(center);

  // Load data
  geojsonObject = JSON.parse(response);
  var route = new ol.format.GeoJSON().readFeatures(geojsonObject, {
      featureProjection: 'EPSG:3857'
  });

  // Get element from the array and set type
	route = route[0];
	route.set('type', 'route');

  // Get coordinates for further points generation
	routeCoords = route.getGeometry().getCoordinates();
	routeLength = routeCoords.length;

  // Create line
  var line = new ol.geom.LineString(routeCoords);
  var lineFeature = new ol.Feature(line);

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
			console.log(coordinates)
      popup.setPosition(coordinates);
      var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
                          coordinates, 'EPSG:3857', 'EPSG:4326'));
      content = '<p>Information:</p><code>' + hdms +
                              '</code>';
      content = content + '<p id="hidden_id">' + feature.id + '</p>'
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

