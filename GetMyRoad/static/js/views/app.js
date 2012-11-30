define([
  'jquery',
  'underscore',
  'backbone',

  // Views:
  'views/map'
], function($, _, Backbone, MapView) {

  var AppView = Backbone.View.extend({

    el: 'body',

    events: {
      'click #find_places': 'fetchPlaces'
    },

    Models: {},
    Collections: {},
    Views: {
      'map': new MapView()
    },

    initialize: function() {
      console.log('working');
    },

    fetchPlaces: function() {
      $.ajax({ url: 'find-places/', async: false }).then(function(contents) {
          data = contents;
      });
      console.log(data);
    }

  });

  return AppView;
});
