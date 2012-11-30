define([
  'jquery',
  'underscore',
  'backbone',

  // Models
  'models/user',

  // Views:
  'views/map',

  'jquery_ui',
  'timepicker'
], function($, _, Backbone, User, MapView) {

  var AppView = Backbone.View.extend({

    el: 'body',

    Models: {},
    Collections: {},
    Views: {
      'map': new MapView()
    },

    initialize: function() {
        this.$('.timepicker').datetimepicker();
    }

  });

  return AppView;
});
