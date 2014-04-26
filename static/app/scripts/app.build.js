({
  // appDir: "../",
  // baseUrl: "../scripts",
  // dir: "../../appdirectory-build",
  mainConfigFile : 'main.js',
  name: 'main',
  out: '../../appdirectory-build/main.js',
  removeCombined: true,
  findNestedDependencies: true
})
// ({

//   appDir: "../",
//   baseUrl: "scripts",
//   dir: "../../appdirectory-build",
//   modules: [
//       {
//           name: "main"
//       }
//   ],
//   paths: {
//     jquery: 'vendor/jquery.min',
//     angular: 'vendor/angular.min',
//     // ngResource: 'vendor/angular-resource.min',
//     // ngCookies: 'vendor/angular-cookies.min',
//     // ngRoute: 'vendor/angular-route.min',
//     domReady: 'vendor/domReady',
//     // bootstrapAffix: '../bower_components/bootstrap-sass/js/bootstrap-affix',
//     // bootstrapAlert: '../bower_components/bootstrap-sass/js/bootstrap-alert',
//     // bootstrapDropdown: '../bower_components/bootstrap-sass/js/bootstrap-dropdown',
//     // bootstrapTooltip: '../bower_components/bootstrap-sass/js/bootstrap-affix',
//     // bootstrapModal: '../bower_components/bootstrap-sass/js/bootstrap-affix',
//     // bootstrapTransition: '../bower_components/bootstrap-sass/js/bootstrap-transition',
//     // bootstrapButton: '../bower_components/bootstrap-sass/js/bootstrap-button',
//     // bootstrapPopover: '../bower_components/bootstrap-sass/js/bootstrap-popover',
//     // bootstrapTypeahead: '../bower_components/bootstrap-sass/js/bootstrap-typeahead',
//     // bootstrapCarousel: '../bower_components/bootstrap-sass/js/bootstrap-carousel',
//     // bootstrapScrollspy: '../bower_components/bootstrap-sass/js/bootstrap-scrollspy',
//     // bootstrapCollapse: '../bower_components/bootstrap-sass/js/bootstrap-collapse',
//     bootstrapCollapse: '../bower_components/sass-bootstrap/js/collapse',
//     // bootstrapTab: '../bower_components/bootstrap-sass/js/bootstrap-tab',
//     async: '../bower_components/requirejs-plugins/src/async',
//     googlemaps: '//maps.google.com/maps/api/js?sensor=true',
//     leafletmaps: '//cdn.leafletjs.com/leaflet-0.7/leaflet',
//     'leaflet-directive': 'vendor/angular-leaflet-directive',
//     'ui-router': 'vendor/angular-ui-router'
//   },
//   shim: {
//     angular: {
//       // disabling jquery as an experiment
//       // deps: ['jquery'],
//       exports: 'angular'
//     },
//     // ngResource: {
//     //   deps: ['angular'],
//     //   exports: 'ngResource'
//     // },
//     // ngCookies: {
//     //   deps: ['angular'],
//     //   exports: 'ngCookies'
//     // },
//     bootstrap: {
//       deps: ['jquery', 'bootstrapCollapse'],
//       exports: 'bootstrap'
//     },
//     'leaflet-directive': {
//       deps: ['angular']
//     },
//     'ui-router': {
//       deps: ['angular']
//     }
//   }
// })
