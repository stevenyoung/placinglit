require.config({
  baseUrl: '/js',
  paths: {
    'coffee-script': 'libs/coffee-script',
    'cs': 'libs/cs',
    'jquery': 'libs/jquery-1.8.2.min',
    'underscore': 'libs/underscore-min',
    'backbone': 'libs/backbone-min',
    'bootstrap': 'libs/bootstrap-min'
  },
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['libs/underscore-min', 'jquery'],
      exports: 'Backbone'
    },
    bootstrap: {
      deps: ['libs/bootstrap-min', 'jquery'],
      exports: 'bootstrap'
    }
  }
});

require(['cs!src/models/location'], function(location) {
  console.log(location);
});