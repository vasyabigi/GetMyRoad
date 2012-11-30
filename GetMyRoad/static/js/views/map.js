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

        events: {
          'click #set-new-pos': 'setNewPosition'
        },

        initialize: function() {
            User.on('change:isFigured', this.updateMapControl, this);

            var self = this,
                map = L.map('map', {
                    center: [50.451, 30.523],
                    zoom: 13
                });

            this.map = map;

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            this.infoBlock = this.createInfoBlock();
            this.infoBlock.addTo(map);

            //-- Find my location
            this.getMyLocation();

            //-- Set New Position
            map.on('click', function(data){
                if (!User.get('isFigured')) {
                    self.position = L.marker(data.latlng).addTo(map);
                    self.updateUserCoordinates(data.latlng);
                }
            });
        },

        createInfoBlock: function() {
          //-- info block
          var infoBlock = L.control();

          infoBlock.onAdd = function (map) {
              this._div = L.DomUtil.create('div', 'info'); // div with a class "info"
              this.update();
              return this._div;
          };

          //-- use self.infoBlock.update(your_data_to_display);
          infoBlock.update = function (data) {
              this._div.innerHTML = data ? data : '';
          };

          return infoBlock;
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

            console.log(User);

            this.map.removeLayer(this.position);

            this.map.setZoom(10);

            User.set({ isFigured: false });
        },

        updateUserCoordinates: function(coordinates) {
            User.set({
                coordinates: coordinates,
                isFigured: true
            });
        },

        updateMapControl: function() {
            if (User.get('isFigured')) {
                this.infoBlock.update('Ready to find a road.');
            } else {
                this.infoBlock.update('Need to choose start position.');
            }
        }

  });

  return MapView;
});
