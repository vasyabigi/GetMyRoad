define([
    'underscore',
    'backbone'
], function(_, Backbone) {

  var Category = Backbone.Model.extend({
        defaults: {
            name: null,
            activated: false
        }
  });

  return Category;

});
