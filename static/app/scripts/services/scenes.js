define(['services/services'],
  function(services){
    services.provider('SceneService', function() {
      this.$get = function($http, $q) {
        var service = {
          getAllScenes: function() {
            var d = $q.defer();
            $http({
              url: '/places/show',
            }).success(function(data) {
              d.resolve(data);
            }).error(function(data) {
              d.reject(reason);
            })
            return d.promise
          }
        };
        return service;
      }
    })
  });
