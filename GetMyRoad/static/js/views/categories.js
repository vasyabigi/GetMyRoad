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

    el: '#category-sidebar',

    events: {
      'click #sidebar-opener': 'sliderToggle'
    },

    initialize: function() {
      categories.on('add', this.render, this);
    },
    sliderToggle : function(){
        this.$el.toggleClass('toggled');
    },

    render: function() {
      var self = this;
      self.$el.find('#categories ul').html("");
      categories.each(function(el) {
          elView = new CategoryView({ model: el });
          self.$el.find('#categories ul').prepend(elView.render().el);
      });
    }

  });

  return CategoriesView;
});
