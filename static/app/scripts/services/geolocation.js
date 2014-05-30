define(['services/services'],
  function (services) {
    services.factory('GeolocationService',//'$q','$rootScope','$window'],
      function ($q, $window, $rootScope) {
        return {
          getLocation: function () {
            var deferred = $q.defer();
            if ($window.navigator && $window.navigator.geolocation) {
              $window.navigator.geolocation.getCurrentPosition(
                function(position){
                  $rootScope.$apply(function(){deferred.resolve(position);});
                },
              function(error) {
                switch (error.code) {
                  case 1:
                    $rootScope.$broadcast('error', 'permission denied');
                    $rootScope.$apply(function() {
                      deferred.reject('permission denied');
                    });
                    break;
                  case 2:
                    $rootScope.$broadcast('error', 'position unavailable');
                    $rootScope.$apply(function() {
                      deferred.reject('position unavailable');
                    });
                    break;
                  case 3:
                    $rootScope.$broadcast('error', 'timeout');
                    $rootScope.$apply(function() {
                      deferred.reject('timeout');
                    });
                    break;
                }
              }
            )
          }
          else {
            $rootScope.$broadcast('error','unsupported browser');
            $rootScope.$apply(function(){
              deferred.reject('unsupported browser');
            });
          }
          return deferred.promise;;
        }
      };
    }
  );
});