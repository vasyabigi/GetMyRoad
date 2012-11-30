define([
    'underscore',
    'backbone'
], function(_, Backbone) {

  var User = Backbone.Model.extend({

    defaults: {

        coordinates: {
            lat: null,
            lng: null
        },

        isFigured: false,

        currentPos: {
            lat: null,
            lng: null
        }

    },

    getLatLng: function() {
        return {
            lat: this.get('coordinates').lat,
            lng: this.get('coordinates').lng
        };
    }

  });

  return new User();

});
