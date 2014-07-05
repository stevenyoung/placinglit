define(['angularMocks',
  'controllers/leafletmap'],
  function(){
    'use strict';
    beforeEach(module('controllers'));

    describe('Controller: LeafletMapCtrl', function () {
      var ctrl,
        scope,
        leafletEvents;

      describe('#loading map', function() {
        beforeEach(inject(function($controller, $rootScope){
          scope = $rootScope.$new();
          ctrl = $controller('LeafletMapCtrl', {
            $scope: scope,
            leafletEvents: leafletEvents
          });
        }));
        it('should load a map with a center and zoom', function(){
          expect(scope.center.lat).toBeDefined();
          expect(scope.center.lng).toBeDefined();
          expect(scope.center.zoom).toBeDefined();
        });
        it('should listen for load', function(){
          expect(scope.events.map.enable).toContain('load');
        });
        it('should listen for click', function(){
          expect(scope.events.map.enable).toContain('click');
        });
      });
    });
  });