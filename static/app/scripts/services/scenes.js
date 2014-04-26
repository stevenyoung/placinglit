define(['services/services'],
  function(services){
    services.provider('Scene', function() {
      this.$get = function($http, $q) {
        var service = {
          getScene: function() {
            var d = $q.defer();
          }
        };
        return service
      }
    })
  });