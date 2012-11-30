define([
  'jquery',
  'underscore',
  'backbone',

  'leaflet',

  // Models
  'models/user'

], function($, _, Backbone, L, User) {

  var MapView = Backbone.View.extend({

        el: "#map-container",

        events: {'click #set-new-pos': 'setNewPosition'},

        initialize: function() {
            var self = this,
                map = L.map('map', {
                    center: [50.451, 30.523],
                    zoom: 13
                });

            this.map = map;

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            this.getMyLocation();

            map.on('click', function(data){
                if (!User.get('isFigured')) {

                    var circleOptions = {
                        color: 'green',
                        fillColor: 'green',
                        fillOpacity: 0.5
                    };

                    L.marker(data.latlng).bindPopup("You are here").addTo(map);

                    self.updateUserCoordinates(data.latlng);
                }
            });
        },

        getMyLocation: function() {
            var self = this,
                map = this.map;

            map.locate({setView: true, maxZoom: 15});

            map.on('locationfound', function(data) {
                var circleOptions = {
                    color: 'green',
                    fillColor: 'green',
                    fillOpacity: 0.5
                };
                L.circle(data.latlng, data.accuracy, circleOptions).addTo(map);

                L.marker(data.latlng).bindPopup("You are here").addTo(map);

                self.updateUserCoordinates(data.latlng);
            });

            map.on('locationerror', function() {
                console.log('Enable to find your location');
            });
        },

        setNewPosition: function() {
            User.set({isFigured: false});
            console.log(User);

            // Delete old marker
        },

        updateUserCoordinates: function(coordinates) {
            User.set({
                coordinates: coordinates,
                isFigured: true
            });
        }

  });

  return MapView;
});
