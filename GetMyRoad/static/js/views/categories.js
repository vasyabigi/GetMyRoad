define([
  'jquery',
  'underscore',
  'backbone',

  // Collections
  'collections/categories',

  // Views
  'views/category'

], function($, _, Backbone, categories, CategoryView) {

  var CategoriesView = Backbone.View.extend({

    el: '#categories',

    initialize: function() {
      categories.on('add', this.render, this);
    },

    render: function() {
      var self = this;
      self.$el.html("");
      categories.each(function(el) {
          elView = new CategoryView({ model: el });
          self.$el.prepend(elView.render().el);
      });
    }

  });

  return CategoriesView;
});
