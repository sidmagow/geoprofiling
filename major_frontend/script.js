function initMap() {
 var directionsService = new google.maps.DirectionsService;
 var directionsDisplay = new google.maps.DirectionsRenderer;
 var map = new google.maps.Map(document.getElementById('map'), {
   zoom: 7,
   center: {lat: 41.85, lng: -87.65}
 });
 directionsDisplay.setMap(map);

 var onClickHandler = function() {
   calculateAndDisplayRoute(directionsService, directionsDisplay);
 };
 document.getElementById('find').addEventListener('click', onClickHandler);

}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
  console.log(document.getElementById('start').value);
  console.log(document.getElementById('end').value);
 directionsService.route({
   origin: document.getElementById('start').value,
   destination: document.getElementById('end').value,
   travelMode: 'DRIVING'
 }, function(response, status) {
   if (status === 'OK') {
     directionsDisplay.setDirections(response);
   } else {
     window.alert('Directions request failed due to ' + status);
   }
 });
}
