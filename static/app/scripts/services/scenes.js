define(['services/services'],
  function(services){
    services.provider('SceneService', function() {
      this.$get = function($http, $q) {
        var service = {
          getAllScenes: function() {
            var d = $q.defer();
            $http({
              url: '/places/show',
              cache: true
            }).success(function(data) {
              d.resolve(data);
            }).error(function(data) {
              d.reject(reason);
            });
            return d.promise;
          },
          getScene: function(scene_key) {
            var d = $q.defer();
            $http({
              method: GET,
              url: '/places/info/' + scene_key,
              cache: true
            }).success(function(data) {
              d.resolve(data);
            }).error(function(data) {
              d.reject(reason);
            });
            return d.promise;
          },
          addScene: function() {
            var d = $q.defer();
            $http({
              method: POST,
              url: 'places/add'
            }).sucess(function(data) {
              d.resolve(data);
            }).error(function(data) {
              d.reject(reason);
            });
            return d.promise;
          }
        };
        return service;
      }
    })
  });
