define([
    'underscore',
    'backbone',

    'models/Category'
], function(_, Backbone, Category) {

  var Categories = Backbone.Collection.extend({
        model: Category
  });

  return new Categories();

});
