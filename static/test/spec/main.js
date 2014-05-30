'use strict';

var tests = Object.keys(window.__karma__.files).filter(function (file) {
  // run tests - only files ending with "Spec.js"
  return /Spec\.js$/.test(file);
});

require.config({
  // Karma serves files from '/base'
  baseUrl: '/base/app/scripts',

  paths: {
    jquery: 'vendor/jquery.min',
    angular: 'vendor/angular.min',
    domReady: 'vendor/domReady',
    angularMocks: 'vendor/angular-mocks',
    ngResource: 'vendor/angular-resource.min',
    leafletmaps: '//cdn.leafletjs.com/leaflet-0.7/leaflet',
    googlemaps: '//maps.google.com/maps/api/js?sensor=true',
    unitTest: '../../test/spec'
  },

  shim: {
    angular: {
      deps: ['jquery'],
      exports: 'angular'
    },
    angularMocks: {deps: ['angular']},
    ngResource: {deps: ['angular']}
  },

  // ask Require.js to load these files (all our tests)
  deps: tests,

  // start test run, once Require.js is done
  callback: window.__karma__.start
});