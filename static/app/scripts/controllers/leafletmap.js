define(['controllers/controllers',
        'leafletmaps',
        'services/scenes',
        'services/geolocation'],
  function(controllers, leafletEvents) {
    controllers.controller('LeafletMapCtrl',
      function ($scope, leafletEvents, $location, SceneService,
                GeolocationService) {
      $scope.eventDetected = 'Nothing'
      angular.extend($scope, {
       defaults: {
          tileLayer: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          minZoom: 2,
          path: {
            weight: 10,
            color: '#800000',
            opacity: 1
          },
        }
      });
      angular.extend($scope, {
        center: {
          lat: 31.653381399664,
          lng: -39.375,
          // lat: 0,
          // lng: 0,
          zoom: 2
        }
      });
      angular.extend($scope, {
        layers: {
          baselayers: {
            osm: {
              name: 'OpenStreetMap',
              type: 'xyz',
              url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              layerOptions: {
                subdomains: ['a', 'b', 'c'],
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
              }
            },
          },
        }
      });
      angular.extend($scope, {
        events: {
          map: {
            enable: ['click', 'load'],
            logic: 'emit'
          },
          markers: {
            enable: ['click'],
            logic: 'emit'
          }
        }
      });

      $scope.userMarkerLatitude = $scope.center.lat;
      $scope.userMarkerLongitude = $scope.center.lng;

      function openFormOnMarkerClick(event, args) {
        console.log(event, args)
        var markerLocation = args.leafletEvent.latlng,
          lat = markerLocation.lat,
          lng = markerLocation.lng;
        console.log('dropped at ' + lat + ',' + lng);
        console.log($scope.markers[0]);
        var edit_iframe = '<iframe src="#/edit" height="400px" width="600px" border="0"></iframe>'
        $scope.markers[0].message= edit_iframe;
      }

      function dropMarkerOnMapClick(event, args) {
        var leafEvent = args.leafletEvent;
        $scope.eventDetected = event.name;
        $scope.markers.pop();
        $scope.markers.push({
          lat: leafEvent.latlng.lat,
          lng: leafEvent.latlng.lng,
          message: '<a ng-href="#/edit" href="#/edit">Add a new place</a>',
          draggable: true
        });

        $scope.userMarkerLatitude = $scope.markers[0].lat;
        $scope.userMarkerLongitude = $scope.markers[0].lng;

        $scope.$on('leafletDirectiveMarker.click', openFormOnMarkerClick)
        $scope.$on('leafletDirectiveMarker.popupopen', function(e, args) {
          console.log('leaflet popup open')
        });
        $scope.$on('leafletDirectiveMarker.dragend', function(e, args) {
          console.log('leaflet drag end');
          $scope.userMarkerLatitude = $scope.markers[0].lat;
          $scope.userMarkerLongitude = $scope.markers[0].lng;
        });

      }

      function showEventsViaBinding(event, args) {
        $scope.eventDetected = 'load';
        var mapEvents = leafletEvents.getAvailableMapEvents();
        for (var e in mapEvents) {
          var eventName = 'leafletDirectiveMap.' + mapEvents[e];
          $scope.$on(eventName, function(event, args){
            $scope.eventDetected = event.name;
          });
        }
        var markerEvents = leafletEvents.getAvailableMarkerEvents();
        for (e in markerEvents) {
          var eventName = 'leafletDirectiveMarker.' + markerEvents[e];
          $scope.$on(eventName, function(event, args){
            $scope.eventDetected = event.name;
          });
        }
      }


      function getUserLocation() {
        GeolocationService.getLocation().then(function(data){
          $scope.coords = {lat:data.coords.latitude, long:data.coords.longitude};
        });
      }

      function showAllScenes() {
        SceneService.getAllScenes().then(function(scenes) {
          $scope.scenes = scenes;
          angular.forEach(scenes, function(scene) {
            $scope.markers.push({
              group: 'cluster',
              lat: scene.latitude,
              lng: scene.longitude,
              message: scene.title + ' by ' + scene.author,
              draggable: false
            });
          });
          $scope.$on('leafletDirectiveMarker.click', function(e, args) {
            console.log('scene marker click', e, args);
          })
        });
      }

      $scope.markers=[];
      $scope.$on('leafletDirectiveMap.click', dropMarkerOnMapClick);
      $scope.$on('leafletDirectiveMap.load', showEventsViaBinding);
      $scope.$on('leafletDirectiveMap.load', showAllScenes);
      $scope.$on('leafletDirectiveMap.load', getUserLocation);
    });
  }
);