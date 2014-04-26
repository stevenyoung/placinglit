define(['controllers/controllers','async!//maps.google.com/maps/api/js?sensor=true'],
  function(controllers, googlemaps){
    controllers.controller('MapCtrl', function ($scope, googlemaps) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];

      $scope.map = new google.maps.Map(document.getElementById('#map_canvas'));
      console.log('map', $scope.map, googlemaps)
    });
  }
);
