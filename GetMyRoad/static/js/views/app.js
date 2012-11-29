define([
  'jquery',
  'underscore',
  'backbone',

  // Views:
  'views/map'
], function($, _, Backbone, MapView) {

  var AppView = Backbone.View.extend({

    Models: {},
    Collections: {},
    Views: {
      'map': new MapView()
    },

    initialize: function() {
      console.log('working');
    }

  });

  return AppView;
});
