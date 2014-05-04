define(['angular',
  // 'ngCookies',
  // 'angular-resource',
  // 'ngSanitize',
  'ngRoute',
  'ngTouch',
  'controllers/controllers',
  'services/services',
  'filters/filters',
  'directives/directives',
  // 'googlemaps'
  ],
  function(angular) {
    return angular.module('pl2clientApp',
      [
        // 'angular-resource',
        // 'ui.router',
        // 'ngCookies',
        'ngRoute',
        'ngTouch',
        'leaflet-directive',
        // 'leaflet.markercluster',
        'controllers',
        'services',
        'directives',
        'filters'
      ]);
  });
