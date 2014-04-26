define(['controllers/controllers','services/scenes'],
  function(controllers){
    controllers.controller('MapCtrl', function ($scope, googlemaps) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];

      // $scope.map = new google.maps.Map(document.getElementById('#map_canvas'));
      // console.log('map', $scope.map, googlemaps)
    });
  }
);
