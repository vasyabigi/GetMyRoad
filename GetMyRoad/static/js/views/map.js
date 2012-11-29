define([
  'jquery',
  'underscore',
  'backbone',

  'leaflet'
], function($, _, Backbone, L) {

  var MapView = Backbone.View.extend({

        el: "#map",

        initialize: function() {
            var map = L.map('map', {
                center: [50.451, 30.523],
                zoom: 13
            });

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);
        }

  });

  return MapView;
});
