require.config({
  paths: {
    jquery: 'vendor/jquery.min',
    angular: 'vendor/angular.min',
    // 'angular-resource': 'vendor/angular-resource.min',
    // ngCookies: 'vendor/angular-cookies.min',
    ngRoute: 'vendor/angular-route.min',
    ngTouch: 'vendor/angular-touch.min',
    domReady: 'vendor/domReady',
    // bootstrapAffix: '../bower_components/bootstrap-sass/js/bootstrap-affix',
    // bootstrapAlert: '../bower_components/bootstrap-sass/js/bootstrap-alert',
    // bootstrapDropdown: '../bower_components/bootstrap-sass/js/bootstrap-dropdown',
    // bootstrapTooltip: '../bower_components/bootstrap-sass/js/bootstrap-affix',
    // bootstrapModal: '../bower_components/bootstrap-sass/js/bootstrap-affix',
    // bootstrapTransition: '../bower_components/bootstrap-sass/js/bootstrap-transition',
    // bootstrapButton: '../bower_components/bootstrap-sass/js/bootstrap-button',
    // bootstrapPopover: '../bower_components/bootstrap-sass/js/bootstrap-popover',
    // bootstrapTypeahead: '../bower_components/bootstrap-sass/js/bootstrap-typeahead',
    // bootstrapCarousel: '../bower_components/bootstrap-sass/js/bootstrap-carousel',
    // bootstrapScrollspy: '../bower_components/bootstrap-sass/js/bootstrap-scrollspy',
    // bootstrapCollapse: '../bower_components/bootstrap-sass/js/bootstrap-collapse',
    // bootstrapCollapse: '../bower_components/sass-bootstrap/js/collapse',
    // bootstrapTab: '../bower_components/bootstrap-sass/js/bootstrap-tab',
    async: '../bower_components/requirejs-plugins/src/async',
    // googlemaps: '//maps.google.com/maps/api/js?sensor=true',
    leafletmaps: '//cdn.leafletjs.com/leaflet-0.7/leaflet',
    'leaflet-directive': 'vendor/angular-leaflet-directive.min',
    'leaflet.markercluster': 'vendor/leaflet.markercluster',
    // 'ui-router': 'vendor/angular-ui-router'
  },
  shim: {
    angular: {
      deps: ['jquery'],
      exports: 'angular'
    },
    // 'angular-resource': {
    //   deps: ['angular'],
    // },
    ngRoute: {
      deps: ['angular'],
      exports: 'ngRoute'
    },
    ngTouch: {
      deps: ['angular'],
      exports: 'ngTouch'
    },
    // bootstrap: {
    //   deps: ['jquery', 'bootstrapCollapse'],
    //   exports: 'bootstrap'
    // },
    'leaflet-directive': {
      deps: ['angular']
    },
    'leaflet.markercluster': {
      deps: ['leafletmaps']
    },
    // 'ui-router': {
    //   deps: ['angular']
    // }
  },
  // TO DO do not use cache-busting url args on  live
  urlArgs: "cb=" +  (new Date()).getTime()
});

require([
  'angular',
  'app',
  'domReady',
  'leaflet-directive',
  'leaflet.markercluster',
  // 'googlemaps',
  // 'ui-router',
  // 'angular-resource',
  'ngRoute',

  'jquery',

  'controllers/main',
  'controllers/leafletmap',
  'controllers/scenes',

  'services/pagination',
  'services/scenes',
  'services/geolocation'
  ],
  function (angular, app, domReady) {
    'use strict';
    var mapView = {
        templateUrl: 'views/map.html',
        controller: 'MapCtrl'
      },
      homeView = {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl'
      },
      editView = {
        templateUrl: 'views/placeform.html',
        controller: 'EditCtrl'
      },
      leafletMapView = {
        templateUrl: 'views/leaflet-map.html',
        controller: 'LeafletMapCtrl'
      },
      googleMapView = {
        templateUrl: 'views/google-map.html',
        controller: 'GoogleMapCtrl'
      };
    app.config(['$routeProvider',
      function($routeProvider) {
        $routeProvider
          .when('/map', leafletMapView)
          .when('/edit', editView)
          .when('/home', homeView)
          .when('/', leafletMapView)
          .when('/lmap', leafletMapView)
          .when('/gmap', googleMapView)
          // .when('/', {
          //   templateUrl: 'views/main.html',
          //   controller: 'MainCtrl'
          // });
      }
    ]);
    domReady(function() {
      angular.bootstrap(document, ['pl2clientApp']);
    });
  }
);
