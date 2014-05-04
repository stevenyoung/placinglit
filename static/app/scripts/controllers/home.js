define(['controllers/controllers'],
  function(controllers){
    controllers.controller('HomeCtrl', function ($scope) {
      $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    });
  }
);
