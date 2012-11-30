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

        isFigured: false
    }

  });

  return new User();

});
