define([
    'underscore',
    'backbone'
], function(_, Backbone) {

  var Place = Backbone.Model.extend({
        defaults: {
            order: null,
            lat: null,
            lng: null
        },

        getLatLng: function() {
            return {
                lat: this.get('lat'),
                lng: this.get('lng')
            };
        }

  });

  return Place;

});
