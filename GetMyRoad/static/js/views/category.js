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
      if (this.model.get('activated')) {
          this.model.set({'activated': false });
      } else {
          this.model.set({'activated': true });
      }

    }

  });

  return CategoryView;
});
