function add_routes(routes){
  var geojson = JSON.parse(routes);
  var center = JSON.parse(center);

  console.log(geojson);
  for(i = 0; i < geojson.features.length; i++){
    add_route(geojson.features[i]);
  }
}
