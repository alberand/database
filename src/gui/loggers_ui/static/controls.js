/*
 * Check button which turn on/off aerospaces on the map
 */
document.getElementById('aerospace_on_btn').onclick = function() {
  if(document.getElementById('aerospace_on_btn').checked) {
    // map.addLayer(aerospace_layer);
    aerospace_layer.setVisible(true);
  } else {
    aerospace_layer.setVisible(false);
  }
}
