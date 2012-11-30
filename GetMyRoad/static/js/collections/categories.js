define([
    'underscore',
    'backbone',

    'models/category'
], function(_, Backbone, Category) {

  var Categories = Backbone.Collection.extend({
        model: Category
  });

  return new Categories();

});
