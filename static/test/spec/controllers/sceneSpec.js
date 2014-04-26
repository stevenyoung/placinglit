define(['angularMocks',
  'controllers/edit'],
  function(){
    'use strict';
    beforeEach(module('controllers'));

    describe('Controller: EditCtrl', function () {
      var ctrl,
        scope,
        mockBackend;

      // Initialize the controller and a mock scope
      beforeEach(inject(function ($controller, $rootScope, $httpBackend) {
        scope = $rootScope.$new();
        ctrl = $controller('EditCtrl', {
          $scope: scope
        });
      }));

      describe('#new place form', function() {
        it('should prevent submission if missing fields', function() {
        });
        it('should save data with new fields', function() {});
      });
    });
  });