define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone) {

  var AppView = Backbone.View.extend({

    Models: {},
    Collections: {},
    Views: {},

    initialize: function() {
      console.log('working');
    }

  });

  return AppView;
});
