define([
  'jquery',
  'underscore',
  'backbone',

  'leaflet',

  // Models
  'models/user',
  'collections/trip',
  'collections/categories',

  // Views
  'views/categories',

  'vendor/csrf',

  'leafletPlugins'

], function($, _, Backbone, L, user, Trip, categories, CategoriesView) {

  var MapView = Backbone.View.extend({

        el: "body",

        events: {
          'click #set-new-pos': 'setNewPosition',
          'click #find_places': 'fetchPlaces',
          'click #get_categories': 'addCategories'
        },

        initialize: function() {
            user.on('change:isFigured', this.updateMapControl, this);

            var self = this,
                categoriesView = new CategoriesView({ collection: categories }),
                map = L.map('map', {
                    center: [50.451, 30.523],
                    zoom: 13
                });

            this.categoriesView = categoriesView;
            this.map = map;

            L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
                maxZoom: 18
            }).addTo(map);

            //-- Create infoblock
            this.infoBlock = this.createInfoBlock();
            this.infoBlock.addTo(map);

            //-- Create FindMe Control
            this.findMeControl = L.control.locate().addTo(map);

            //-- Find my location
            this.getMyLocation();

            //-- Set New Position
            map.on('click', function(data){
                if (!user.get('isFigured')) {
                    self.position = L.marker(data.latlng).addTo(map);
                    self.updateUserCoordinates(data.latlng);
                }
            });

            var setNewPosControl = self.createSetNewPosControl();
            setNewPosControl.addTo(map)



            map.on('click', function (data) {
                if (!user.get('isFigured')) {
                    self.position = L.marker(data.latlng).bindPopup('New position').addTo(map);
                    self.updateUserCoordinates(data.latlng);
                }
            });

        },

        createSetNewPosControl: function() {
            var self = this,
                map = self.map;

            var setNew = L.control({
                position: 'topleft'
            });

            setNew.onAdd = function(map) {
                var wrapper = L.DomUtil.create('div', 'leaflet-setnew-control-locate-wrap');
                var link = L.DomUtil.create('a', 'leaflet-setnew-control-locate', wrapper);
                link.href = '#';
                link.id = '#set-new-pos'
                link.title = 'Show me where I am';

                L.DomEvent
                    .on(link, 'click', L.DomEvent.stopPropagation)
                    .on(link, 'click', L.DomEvent.preventDefault)
                    .on(link, 'click', function() {
                        self.setNewPosition()
                    })

                return wrapper;
            };

            return setNew;
        },


        addCategories: function() {
          var coordinates = user.get('coordinates');

          $.ajax({
            type: "POST",
            url: 'select-categories/',
            async: false,
            dataType: 'json',
            data: {
              "lat": coordinates.lat,
              "lng": coordinates.lng
            },
            beforeSend: function(){
                $('#spinner').fadeToggle();
            },
            success: function() {
                $('#spinner').fadeToggle();
            }
          }).then(function(contents) {

              var data = [];

              $.each(contents.categories, function(i, e) {
                  data[i] = {
                    'name': e.name,
                    'id': e.id
                  };
              });

              categories.add(data);
              user.set({"tripId": contents.trip_id });
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
              this._div.innerHTML = data ? data : 'Choose start point.';
          };

          return infoBlock;
        },

        getMyLocation: function() {
            var self = this,
                map = this.map;

            map.locate({setView: true, maxZoom: 15});

            map.on('locationfound', function(data) {

                user.set({currentPos: data.latlng});

                // var accurCircle = L.circle(data.latlng, data.accuracy, circleOptions),
                //     meMarker = L.circleMarker(data.latlng, markerOptions).bindPopup("You are within " + (data.accuracy).toFixed(0) + " meters from this point");
                // self.currentPos = L.layerGroup([accurCircle, meMarker]).addTo(map);

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
                this.infoBlock.update('Choose new start position.');
            }
        },

        fetchPlaces: function() {

            if (!user.get('isGotTheRoad')) {

                var activatedCategories = [];
                categories.each(function(category) {
                  if (category.get('activated') === true) {
                      activatedCategories.push(category.get('id'));
                    }
                });

                console.log(activatedCategories);

                var self = this,
                    coordinates = user.get('coordinates');

                $.ajax({
                  type: "POST",
                  url: 'find-places/',
                  async: false,
                  dataType: 'json',
                  data: {
                    "id": user.get('tripId'),
                    "categories": activatedCategories
                  }
                }).then(function(contents) {
                    var trip = new Trip(),
                        data = [];

                    trip.on('add', self.addPlaceMarker, self);

                    $.each(contents, function(i, e) {
                        data[i] = {
                          'order': i,
                          'lat': e.place__lat,
                          'lng': e.place__lon,
                          'name': e.place__name,
                          'id': e.place__id
                        };
                    });
                    trip.add(data);
                    self.buildRoad(trip);
                });

                user.set({'isGotTheRoad': true });
            }
        },

        addPlaceMarker: function(place) {
            console.log(place.toJSON());
            L.marker(place.getLatLng()).bindPopup(place.get('name')).addTo(this.map);
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
