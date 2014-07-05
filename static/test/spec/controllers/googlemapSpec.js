define(['angularMocks',
  'controllers/googlemap'],
  function(){
    'use strict';
    beforeEach(module('controllers'));

    describe('Controller: GoogleMapCtrl', function () {
      var ctrl,
        scope;
        // leafletEvents;

      describe('#loading map', function() {
        beforeEach(inject(function($controller, $rootScope){
          scope = $rootScope.$new();
          ctrl = $controller('GoogleMapCtrl', {
            $scope: scope,
            // leafletEvents: leafletEvents
          });
        }));
        it('should have a map property', function(){
          expect(scope.map).toBeDefined();
        });
        it('should load a map with a center and zoom', function(){
          expect(scope.map.center.lat).toBeDefined();
          expect(scope.map.center.lng).toBeDefined();
          expect(scope.center.zoom).toBeDefined();
        });
        it('should listen for load', function(){
          expect(scope.events.map.enable).toContain('load');
        });
        it('should listen for click', function(){
          expect(scope.events.map.enable).toContain('click');
        });
      });

      // these need to be integration tests
      describe('#using map', function() {
        // beforeEach(inject(function($compile, $controller, $rootScope){
        //   scope = $rootScope.$new();
        //   ctrl = $controller('MapCtrl', {
        //     $scope: scope,
        //     leafletEvents: leafletEvents
        //   });
        //   var element = angular.element('<leaflet defaults="defaults" center="center" event-broadcast="events" markers="markers"></leaflet>');
        //   $compile(element)(scope);
        //   scope.$digest();
        // }));

        // this shold be an e2e test
        it('should add a marker on click', function() {
          // var element;
          // inject(function($compile, $controller, $rootScope){
          //   scope = $rootScope.$new();
          //   element = angular.element('<leaflet defaults="defaults" center="center" event-broadcast="events" markers="markers" height="400px" width="400px"></leaflet>');
          //   $compile(element)(scope);
          //   scope.$digest();
          //   ctrl = $controller('MapCtrl', {
          //     $scope: scope,
          //     leafletEvents: leafletEvents
          //   });
          // });
          // scope.markers = [];
          // element.click();
          // console.log('element', element);
          // console.log('scope', scope.center);
          // expect(scope.markers.length).toEqual(1);
        });
        // this shold be an e2e test
        it('should update binding on click', function(){
          // var element;
          // inject(function($rootScope, $controller){
          //   scope = $rootScope;
          //   element = angular.element(
          //     '<ul><li><strong ng-bind="eventDetected"></strong> caught in listener.</li></ul>'
          //   );
          //   ctrl = $controller('MapCtrl', {
          //     $scope: scope,
          //     leafletEvents: leafletEvents
          //   })
          // });
          // console.log(element);
          // element.click();
          // console.log(scope);
          // expect(scope.eventDetected).toEqual('click');
        });
      });
      describe('#using scene markers', function() {
        it('should listen for a marker click', function() {
          // expect(scope.events.marker.enable).toContain('click');
        });
      });
      describe('#using scene popup window', function() {

      })
    });
  });