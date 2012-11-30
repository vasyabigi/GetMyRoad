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

        //-- info block
            var infoblock = L.control();

            infoblock.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); // div with a class "info"
                this.update();
                return this._div;
            };

            //-- use self.infoblock.update(your_data_to_display);
            infoblock.update = function (data) {
                this._div.innerHTML = data ? data : 'Some info';
            };

            self.infoblock = infoblock;
            self.infoblock.addTo(map);

        //-- Find my location
            self.getMyLocation();

        //-- Set New Position
            map.on('click', function(data){
                if (!User.get('isFigured')) {

                    self.position = L.marker(data.latlng).bindPopup("New Position").addTo(map);

                    self.updateUserCoordinates(data.latlng);

                    self.infoblock.update('you got new position!!!')
                }
            });
        },

        getMyLocation: function() {
            var self = this,
                map = self.map;

            map.locate({setView: true, maxZoom: 15});

            map.on('locationfound', function(data) {
                var circleOptions = {
                    color: 'green',
                    fillColor: 'green',
                    fillOpacity: 0.5
                };

                var accurCircle = L.circle(data.latlng, data.accuracy, circleOptions),
                    meMarker = L.marker(data.latlng).bindPopup("You are here");

                self.position = L.layerGroup([accurCircle, meMarker]).addTo(map);

                self.updateUserCoordinates(data.latlng);
            });

            map.on('locationerror', function() {
                console.log('Enable to find your location');
            });
        },

        setNewPosition: function() {
            var self = this;

            self.map.removeLayer(self.position);
            self.map.setZoom(10);
            self.infoblock.update('put new marker position!!!')

            User.set({isFigured: false});

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
