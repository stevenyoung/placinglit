define(['controllers/controllers',
        'googlemaps'],
  function(controllers, googlemaps){
    controllers.controller('GoogleMapCtrl', function ($scope, googlemaps) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
      // angular.extend($scope, {
      //   center : {
      //     lat: 31.653381399664,
      //     lng: -39.375,
      //     zoom: 2
      //   }
      // });

      $scope.center = {
        lat: 31.653381399664,
        lng: -39.375,
        // lat: 0,
        // lng: 0,
        zoom: 2
      }
      // $scope.map = new google.maps.Map(document.getElementById('#mapcontainer'));
      // console.log('map', $scope.map, googlemaps)
    });
  }
);
