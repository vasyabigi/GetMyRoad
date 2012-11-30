define([
  'jquery',
  'underscore',
  'backbone',

  'leaflet'
], function($, _, Backbone, L) {

  var MapView = Backbone.View.extend({

        el: "#map",

        initialize: function() {
            var self = this;

            var map = L.map('map', {
                center: [50.451, 30.523],
                zoom: 13
            });

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            self.getMyLocation(map);
        },

        getMyLocation: function(map) {
            map.locate({setView: true, maxZoom: 15});

            map.on('locationfound', function(data) {
                var circleOptions = {
                    color: 'green',
                    fillColor: 'green',
                    fillOpacity: 0.5
                };
                L.circle(data.latlng, data.accuracy, circleOptions).addTo(map);
                L.marker(data.latlng).bindPopup("You are here").addTo(map);
            });
            map.on('locationerror', function() {
                console.log('Enable to find your location')
            });
        }

  });

  return MapView;
});
