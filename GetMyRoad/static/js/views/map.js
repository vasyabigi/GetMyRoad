define([
  'jquery',
  'underscore',
  'backbone',

  'leaflet',

  // Models
  'models/user',
  'collections/trip',

  'vendor/csrf'

], function($, _, Backbone, L, user, Trip) {

  var MapView = Backbone.View.extend({

        el: "#map-container",

        events: {
          'click #set-new-pos': 'setNewPosition',
          'click #find_places': 'fetchPlaces'
        },

        initialize: function() {
            user.on('change:isFigured', this.updateMapControl, this);

            var self = this,
                map = L.map('map', {
                    center: [50.451, 30.523],
                    zoom: 13
                });

            this.map = map;

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            //-- Create infoblock
            this.infoBlock = this.createInfoBlock();
            this.infoBlock.addTo(map);

            //-- Create FindMe Control
            this.findMeControl = this.createFindMeControl();
            this.findMeControl.addTo(map);

            //-- Find my location
            this.getMyLocation();

            //-- Set New Position
            map.on('click', function(data){
                if (!user.get('isFigured')) {
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

        createFindMeControl: function() {
            var self = this,
                map = self.map;

            var findMe = L.control({
                position: 'topleft'
            });

            findMe.onAdd = function(map) {
                var wrapper = L.DomUtil.create('div', 'leaflet-control-locate-wrap');
                var link = L.DomUtil.create('a', 'leaflet-control-locate', wrapper);
                link.href = '#';
                link.title = 'Show me where I am';

                L.DomEvent
                    .on(link, 'click', L.DomEvent.stopPropagation)
                    .on(link, 'click', L.DomEvent.preventDefault)
                    .on(link, 'click', function() {
                        self.getMyLocation();
                    })

                return wrapper;
            };

            return findMe;
        },

        getMyLocation: function() {
            var self = this,
                map = this.map;

            map.locate({setView: true, maxZoom: 13});

            map.on('locationfound', function(data) {
                if (self.currentPos) return;

                var circleOptions = {
                        color: 'green',
                        fillColor: 'green',
                        fillOpacity: 0.5
                    },
                    markerOptions = {
                        color: 'green',
                        fillColor: 'green',
                        fillOpacity: 0.7,
                        radius: 4
                    }

                user.set({currentPos: data.latlng});

                var accurCircle = L.circle(data.latlng, data.accuracy/2, circleOptions),
                    meMarker = L.circleMarker(data.latlng, markerOptions).bindPopup("You are within " + (data.accuracy/2).toFixed(0) + " meters from this point");
                self.currentPos = L.layerGroup([accurCircle, meMarker]).addTo(map);


                self.position = L.marker(data.latlng).addTo(map);

                self.updateUserCoordinates(data.latlng);
            });

            map.on('locationerror', function() {
                console.log('Enable to find your location');
            });
        },

        setNewPosition: function() {

            this.map.removeLayer(this.position);

            this.map.setZoom(10);

            user.set({ isFigured: false });
        },

        updateUserCoordinates: function(coordinates) {
            user.set({
                coordinates: coordinates,
                isFigured: true
            });
        },

        updateMapControl: function() {
            if (user.get('isFigured')) {
                this.infoBlock.update('Ready to find a road.');
            } else {
                this.infoBlock.update('Need to choose start position.');
            }
        },

        fetchPlaces: function() {
            var self = this,
                coordinates = user.get('coordinates');
            $.ajax({
              type: "POST",
              url: 'find-places/',
              async: false,
              dataType: 'json',
              data: {
                "lat": coordinates.lat,
                "lng": coordinates.lng
              }
            }).then(function(contents) {
                var trip = new Trip(),
                    data = [];

                trip.on('add', self.addPlaceMarker, self);

                $.each(contents, function(i, e) {
                    data[i] = {
                      'order': i,
                      'lat': e.place__lat,
                      'lng': e.place__lon
                    };
                });
                trip.add(data);
                self.buildRoad(trip);
            });
        },

        addPlaceMarker: function(place) {
            console.log(place.toJSON());
            L.marker(place.getLatLng()).addTo(this.map);
        },

        buildRoad: function(trip) {
          var self = this;
          var presentPoint = user.getLatLng();
          trip.each(function(place) {

              // Build piece of road
              self.buildRoadPice(presentPoint, place.getLatLng());

              // Make last poin active
              presentPoint = place.getLatLng();
          });
          self.buildRoadPice(presentPoint, user.getLatLng());

        },

        buildRoadPice: function(start, end) {
          var self = this;

          console.log(this);
          var data = {
              "start_lat": start.lat,
              "start_lng": start.lng,
              "end_lat": end.lat,
              "end_lng": end.lng
          };

          $.ajax({
              type: "POST",
              url: 'build-road/',
              data: data,
              dataType: 'json'
          }).then(function(data) {
              L.polyline(data.route_geometry, {color: 'blue'}).addTo(self.map);
          });
        }
  });

  return MapView;
});
