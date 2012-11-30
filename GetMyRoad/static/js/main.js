require.config({
  // Specify the paths of vendor libraries
  paths: {
    jquery: 'vendor/jquery',
    underscore: 'vendor/underscore',
    backbone: 'vendor/backbone',
    handlebars: 'vendor/handlebars',
    text: 'vendor/require-text',
    leaflet: 'vendor/leaflet',
    csrf: 'vendor/csrf',
    leafletPlugins: 'vendor/leafletPlugins',
    jquery_ui: 'vendor/jquery-ui-1.9.2.custom.min',
    timepicker: 'vendor/timepicker'
  },
  // Underscore and Backbone are not AMD-capable per default,
  // so we need to use the AMD wrapping of RequireJS
  shim: {
    underscore: {
      exports: '_'
    },

    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },

    handlebars: {
      exports: 'Handlebars'
    },

    leaflet: {
      exports: 'L'
    },

    leafletPlugins: ['leaflet'],

    'csrf': {
        deps: ['jquery']
    },

    timepicker: ['jquery_ui']
  }
});

require(['views/app'], function (App) {
  'use strict';

  var app = new App();

});
