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
      var coordinates = User.get('coordinates');
      $.ajax({
          type: "POST",
          url: 'find-places/',
          async: false,
          dataType: 'json',
          data: {
            "lat": coordinates.lat,
            "lng": coordinates.lng
          }
        }).then(function(contents) {
            data = contents;
        });
      console.log(data);
    }

  });

  return AppView;
});
