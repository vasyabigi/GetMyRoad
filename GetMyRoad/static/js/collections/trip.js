define([
    'underscore',
    'backbone',

    'models/place'
], function(_, Backbone, Place) {

  var Trip = Backbone.Collection.extend({
        model: Place
  });

  return Trip;

});
