define([
  'jquery',
  'underscore',
  'backbone',
  'handlebars',

  'text!templates/category.hbs'

], function($, _, Backbone, Handlebars, template) {

  var CategoryView = Backbone.View.extend({

    events: {
        'click': 'changeActivity'
    },

    tagName: 'li',

    template: Handlebars.compile(template),

    initialize: function() {
      this.model.on('change', this.render, this);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

    changeActivity: function() {
      this.model.set({'activated': true });
    }

  });

  return CategoryView;
});
