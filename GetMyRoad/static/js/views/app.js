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
        var date = new Date();
        this.$('#fromTime').val(
            date.getMonth() + '/' + date.getDay() + '/' + date.getFullYear() +
            ' ' + date.getHours() + ':' + date.getMinutes()
        );
        date.setHours(date.getHours() + 8);
        this.$('#toTime').val(
            date.getMonth() + '/' + date.getDay() + '/' + date.getFullYear() +
            ' ' + date.getHours() + ':' + date.getMinutes()
        );
    }

  });

  return AppView;
});
