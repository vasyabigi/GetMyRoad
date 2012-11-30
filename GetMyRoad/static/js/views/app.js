define([
  'jquery',
  'underscore',
  'backbone',

  // Models
  'models/user',

  // Views:
  'views/map'
], function($, _, Backbone, User, MapView) {

  var AppView = Backbone.View.extend({

    el: 'body',

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
