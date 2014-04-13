// Generated by CoffeeScript 1.7.1
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  window.PlacingLit = {
    Models: {},
    Collections: {},
    Views: {}
  };

  PlacingLit.Models.Location = (function(_super) {
    __extends(Location, _super);

    function Location() {
      return Location.__super__.constructor.apply(this, arguments);
    }

    Location.prototype.defaults = {
      title: 'Put Title Here',
      author: 'Someone\'s Name goes here'
    };

    Location.prototype.url = '/places/add';

    return Location;

  })(Backbone.Model);

  PlacingLit.Models.Metadata = (function(_super) {
    __extends(Metadata, _super);

    function Metadata() {
      return Metadata.__super__.constructor.apply(this, arguments);
    }

    Metadata.prototype.url = '/places/count';

    Metadata.prototype.initialize = function() {};

    return Metadata;

  })(Backbone.Model);

  PlacingLit.Collections.Locations = (function(_super) {
    __extends(Locations, _super);

    function Locations() {
      return Locations.__super__.constructor.apply(this, arguments);
    }

    Locations.prototype.model = PlacingLit.Models.Location;

    Locations.prototype.url = '/places/show';

    return Locations;

  })(Backbone.Collection);

  PlacingLit.Collections.NewestLocations = (function(_super) {
    __extends(NewestLocations, _super);

    function NewestLocations() {
      return NewestLocations.__super__.constructor.apply(this, arguments);
    }

    NewestLocations.prototype.model = PlacingLit.Models.Location;

    NewestLocations.prototype.url = '/places/recent';

    return NewestLocations;

  })(Backbone.Collection);

  PlacingLit.Collections.NewestLocationsByDate = (function(_super) {
    __extends(NewestLocationsByDate, _super);

    function NewestLocationsByDate() {
      return NewestLocationsByDate.__super__.constructor.apply(this, arguments);
    }

    NewestLocationsByDate.prototype.model = PlacingLit.Models.Location;

    NewestLocationsByDate.prototype.url = '/places/allbydate';

    return NewestLocationsByDate;

  })(Backbone.Collection);

  PlacingLit.Views.MapCanvasView = (function(_super) {
    __extends(MapCanvasView, _super);

    function MapCanvasView() {
      this.addPlace = __bind(this.addPlace, this);
      this.showMarkers = __bind(this.showMarkers, this);
      this.hideMarkers = __bind(this.hideMarkers, this);
      return MapCanvasView.__super__.constructor.apply(this, arguments);
    }

    MapCanvasView.prototype.model = PlacingLit.Models.Location;

    MapCanvasView.prototype.el = 'map_canvas';

    MapCanvasView.prototype.gmap = null;

    MapCanvasView.prototype.infowindows = [];

    MapCanvasView.prototype.locations = null;

    MapCanvasView.prototype.userInfowindow = null;

    MapCanvasView.prototype.placeInfowindow = null;

    MapCanvasView.prototype.userMapsMarker = null;

    MapCanvasView.prototype.allMarkers = [];

    MapCanvasView.prototype.settings = {
      zoomLevel: {
        'wide': 4,
        'default': 10,
        'close': 14,
        'tight': 21,
        'increment': 1
      },
      markerDefaults: {
        draggable: false,
        animation: google.maps.Animation.DROP,
        icon: '/img/book.png'
      }
    };

    MapCanvasView.prototype.mapOptions = {
      zoom: 4,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
      },
      maxZoom: 25,
      minZoom: 2,
      zoomControl: true,
      zoomControlOptions: {
        style: google.maps.ZoomControlStyle.DEFAULT,
        position: google.maps.ControlPosition.TOP_LEFT
      },
      panControlOptions: {
        position: google.maps.ControlPosition.TOP_LEFT
      }
    };

    MapCanvasView.prototype.initialize = function(scenes) {
      if (this.collection == null) {
        this.collection = new PlacingLit.Collections.Locations();
      }
      this.listenTo(this.collection, 'all', this.render);
      this.collection.fetch();
      return this.attachSearchHandler();
    };

    MapCanvasView.prototype.render = function(event) {
      if (event === 'sync') {
        return this.mapWithMarkers();
      }
    };

    MapCanvasView.prototype.googlemap = function() {
      var map_elem;
      if (this.gmap != null) {
        return this.gmap;
      }
      map_elem = document.getElementById(this.$el.selector);
      this.gmap = new google.maps.Map(map_elem, this.mapOptions);
      google.maps.event.addListener(this.gmap, 'click', (function(_this) {
        return function(event) {
          return _this.handleMapClick(event);
        };
      })(this));
      return this.gmap;
    };

    MapCanvasView.prototype.marker = function() {
      if (this.placeInfowindow != null) {
        this.placeInfowindow.close();
      }
      return new google.maps.Marker();
    };

    MapCanvasView.prototype.infowindow = function() {
      var iw;
      if (this.infowindows.length) {
        this.closeInfowindows();
      }
      iw = new google.maps.InfoWindow();
      this.infowindows.push(iw);
      return iw;
    };

    MapCanvasView.prototype.closeInfowindows = function() {
      var iw, _i, _len, _ref, _results;
      _ref = this.infowindows;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        iw = _ref[_i];
        _results.push(iw.close());
      }
      return _results;
    };

    MapCanvasView.prototype.mappoint = function(latitude, longitude) {
      return new google.maps.LatLng(latitude, longitude);
    };

    MapCanvasView.prototype.markerFromMapLocation = function(map, location) {
      var markerSettings;
      markerSettings = {
        position: location,
        map: map,
        animation: google.maps.Animation.DROP,
        draggable: true
      };
      return new google.maps.Marker(markerSettings);
    };

    MapCanvasView.prototype.updateInfoWindow = function(text, location, map) {
      var infowindow;
      this.map = map != null ? map : this.googlemap('hpmap');
      infowindow = this.infowindow();
      infowindow.setContent(text);
      infowindow.setPosition(location);
      return infowindow.open(map);
    };

    MapCanvasView.prototype.setUserPlaceFromLocation = function(location) {
      return this.userPlace = location;
    };

    MapCanvasView.prototype.showInfowindowFormAtLocation = function(map, marker, location) {
      this.closeInfowindows();
      this.userInfowindow = this.infowindow();
      this.userInfowindow.setContent(document.getElementById('iwcontainer').innerHTML);
      this.userInfowindow.setPosition(location);
      this.userInfowindow.open(map);
      if (!Modernizr.input.placeholder) {
        google.maps.event.addListener(this.userInfowindow, 'domready', (function(_this) {
          return function() {};
        })(this), this.clearPlaceholders());
      }
      return document.getElementById('guidelines').addEventListener('click', (function(_this) {
        return function(event) {
          return $('#helpmodal').modal();
        };
      })(this));
    };

    MapCanvasView.prototype.clearPlaceholders = function() {
      $('#title').one('keypress', function() {
        return $('#title').val('');
      });
      $('#author').one('keypress', function() {
        return $('#author').val('');
      });
      $('#place_name').one('keypress', function() {
        return $('#place_name').val('');
      });
      $('#date').one('keypress', function() {
        return $('#date').val('');
      });
      $('#actors').one('keypress', function() {
        return $('#actors').val('');
      });
      $('#symbols').one('keypress', function() {
        return $('#symbols').val('');
      });
      $('#scene').one('keypress', function() {
        return $('#scene').val('');
      });
      $('#notes').one('keypress', function() {
        return $('#notes').val('');
      });
      return $('#image_url').one('keypress', function() {
        return $('#image_url').val('');
      });
    };

    MapCanvasView.prototype.clearMapMarker = function(marker) {
      marker.setMap(null);
      return marker = null;
    };

    MapCanvasView.prototype.suggestTitles = function() {
      var title_data;
      title_data = [];
      return $.ajax({
        url: "/places/titles",
        success: function(data) {
          $.each(data, function(key, value) {
            return title_data.push(value.title.toString());
          });
          return $('#title').typeahead({
            source: title_data
          });
        }
      });
    };

    MapCanvasView.prototype.suggestAuthors = function() {
      var author_data;
      author_data = [];
      return $.ajax({
        url: "/places/authors",
        success: function(data) {
          $.each(data, function(key, value) {
            return author_data.push(value.author.toString());
          });
          return $('#author').typeahead({
            source: author_data
          });
        }
      });
    };

    MapCanvasView.prototype.markersForEachScene = function() {
      return this.collection.each((function(_this) {
        return function(model) {
          return _this.dropMarkerForStoredLocation(model);
        };
      })(this));
    };

    MapCanvasView.prototype.markerArrayFromCollection = function(collection) {
      var model;
      return (function() {
        var _i, _len, _ref, _results;
        _ref = collection.models;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          model = _ref[_i];
          _results.push(this.buildMarkerFromLocation(model));
        }
        return _results;
      }).call(this);
    };

    MapCanvasView.prototype.markerClustersForScenes = function(locations) {
      var allMarkerCluster, cluster_options;
      cluster_options = {
        minimumClusterSize: 5
      };
      return allMarkerCluster = new MarkerClusterer(this.gmap, locations, cluster_options);
    };

    MapCanvasView.prototype.hideMarkers = function() {
      var marker, _i, _len, _ref, _results;
      _ref = this.allMarkers;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        marker = _ref[_i];
        _results.push(marker.setMap(null));
      }
      return _results;
    };

    MapCanvasView.prototype.showMarkers = function() {
      var marker, _i, _len, _ref, _results;
      _ref = this.allMarkers;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        marker = _ref[_i];
        _results.push(marker.setMap(this.gmap));
      }
      return _results;
    };

    MapCanvasView.prototype.mapWithMarkers = function() {
      if (this.gmap == null) {
        this.gmap = this.googlemap();
      }
      this.allMarkers = this.markerArrayFromCollection(this.collection);
      this.markerClustersForScenes(this.allMarkers);
      return this.positionMap();
    };

    MapCanvasView.prototype.positionMap = function() {
      var mapcenter, usaCoords, usacenter;
      if (typeof CENTER !== "undefined" && CENTER !== null) {
        mapcenter = new google.maps.LatLng(CENTER.lat, CENTER.lng);
        this.gmap.setCenter(mapcenter);
        if (window.location.pathname.indexOf('collections') !== -1) {
          this.gmap.setZoom(this.settings.zoomLevel.wide);
        } else {
          this.gmap.setZoom(this.settings.zoomLevel["default"]);
        }
      } else {
        usaCoords = {
          lat: 39.8282,
          lng: -98.5795
        };
        usacenter = new google.maps.LatLng(usaCoords.lat, usaCoords.lng);
        this.gmap.setCenter(usacenter);
        this.gmap.setZoom(2);
      }
      if (typeof PLACEKEY !== "undefined" && PLACEKEY !== null) {
        return this.openInfowindowForPlace(PLACEKEY, mapcenter);
      }
    };

    MapCanvasView.prototype.handleMapClick = function(event) {
      return this.setUserMapMarker(this.gmap, event.latLng);
    };

    MapCanvasView.prototype.setUserMapMarker = function(map, location) {
      if (this.userMapsMarker != null) {
        this.userMapsMarker.setMap(null);
      }
      if (this.userInfowindow != null) {
        this.userInfowindow.close();
      }
      this.userMapsMarker = this.markerFromMapLocation(map, location);
      this.userMapsMarker.setMap(map);
      return google.maps.event.addListener(this.userMapsMarker, 'click', (function(_this) {
        return function(event) {
          return _this.isUserLoggedIn();
        };
      })(this));
    };

    MapCanvasView.prototype.isUserLoggedIn = function() {
      return $.ajax({
        datatype: 'json',
        url: '/user/status',
        success: (function(_this) {
          return function(data) {
            if (data.status === 'logged in') {
              return _this.dropMarkerForNewLocation();
            } else {
              return _this.showLoginInfoWindow();
            }
          };
        })(this)
      });
    };

    MapCanvasView.prototype.showLoginInfoWindow = function() {
      var content, login_url;
      this.closeInfowindows();
      this.userInfowindow = this.infowindow();
      content = '<div id="maplogin">';
      content += '<div>You must be logged in to add content.</div>';
      login_url = document.getElementById('loginlink').href;
      content += '<a href="' + login_url + '"><button>log in</button></a></p>';
      this.userInfowindow.setContent(content);
      this.userInfowindow.setPosition(this.userMapsMarker.getPosition());
      return this.userInfowindow.open(this.gmap);
    };

    MapCanvasView.prototype.dropMarkerForNewLocation = function() {
      var location;
      location = this.userMapsMarker.getPosition();
      this.showInfowindowFormAtLocation(this.gmap, this.userMapsMarker, location);
      this.setUserPlaceFromLocation(location);
      this.handleInfowindowButtonClick();
      this.suggestTitles();
      return this.suggestAuthors();
    };

    MapCanvasView.prototype.updateInfowindowWithMessage = function(infowindow, text, refresh) {
      var textcontainer;
      textcontainer = '<div id="thankswindow">' + text.message + '</div>';
      infowindow.setContent(textcontainer);
      if (refresh) {
        return google.maps.event.addListener(infowindow, 'closeclick', (function(_this) {
          return function() {
            return _this.showUpdatedMap();
          };
        })(this));
      }
    };

    MapCanvasView.prototype.showUpdatedMap = function() {
      var maps;
      return maps = new MapCanvasView;
    };

    MapCanvasView.prototype.handleInfowindowButtonClick = function() {
      var $addPlaceButton;
      $addPlaceButton = $('#map_canvas .infowindowform').find('#addplacebutton');
      if ($addPlaceButton != null) {
        return $addPlaceButton.on('click', this.addPlace);
      }
    };

    MapCanvasView.prototype.getFormValues = function() {
      var $form, form_data;
      $form = $('#map_canvas .infowindowform');
      form_data = {
        title: $form.find('#title').val(),
        author: $form.find('#author').val(),
        place_name: $form.find('#place_name').val(),
        scene: $form.find('#scene').val(),
        notes: $form.find('#notes').val(),
        image_url: $form.find('#image_url').val(),
        check_in: $form.find('#check_in').prop('checked')
      };
      form_data.latitude = this.userPlace.lat();
      form_data.longitude = this.userPlace.lng();
      return form_data;
    };

    MapCanvasView.prototype.isFormComplete = function(form_data) {
      var completed_entry, field, field_name, required_fields, _i, _len;
      required_fields = ['title', 'author', 'place_name', 'scene', 'notes'];
      completed_entry = true;
      this.missing_fields = '';
      for (_i = 0, _len = required_fields.length; _i < _len; _i++) {
        field = required_fields[_i];
        if (form_data[field].length === 0) {
          field_name = field.charAt(0).toUpperCase();
          field_name += field.substr(1).toLowerCase();
          field_name = field_name.replace('_', ' ');
          this.missing_fields += 'Missing ' + field_name + '.</br>';
          completed_entry = false;
        }
      }
      return completed_entry;
    };

    MapCanvasView.prototype.addPlace = function() {
      var error_msg, form_data, location, msg, response, status;
      form_data = this.getFormValues();
      if (this.isFormComplete(form_data)) {
        msg = '<span>adding... please wait...</span>';
        $('#map_canvas .infowindowform').find('#addplacebutton').replaceWith(msg);
        location = new PlacingLit.Models.Location();
        return status = location.save(form_data, {
          error: (function(_this) {
            return function(model, xhr, options) {
              return console.log('add place error', model, xhr, options);
            };
          })(this),
          success: (function(_this) {
            return function(model, response, options) {
              return _this.updateInfowindowWithMessage(_this.userInfowindow, response, true);
            };
          })(this)
        });
      } else {
        error_msg = '<p>Close this window and click the marker to start over. <br> Fill out some of these fields so we can add your scene. <br> Thanks.</p>';
        response = {
          message: this.missing_fields + error_msg
        };
        this.updateInfowindowWithMessage(this.userInfowindow, response, false);
        return false;
      }
    };

    MapCanvasView.prototype.geocoderSearch = function() {
      var address, geocoder;
      address = document.getElementById('gcf').value;
      if (address) {
        geocoder = new google.maps.Geocoder();
        return geocoder.geocode({
          'address': address
        }, (function(_this) {
          return function(results, status) {
            var position;
            if (status === google.maps.GeocoderStatus.OK) {
              position = results[0].geometry.location;
              _this.gmap.setCenter(position);
              return _this.gmap.setZoom(_this.settings.zoomLevel["default"]);
            } else {
              return alert("geocode was not successful: " + status);
            }
          };
        })(this));
      }
    };

    MapCanvasView.prototype.attachSearchHandler = function() {
      document.getElementById('gcf').addEventListener('keydown', (function(_this) {
        return function(event) {
          if (event.which === 13 || event.keyCode === 13) {
            event.preventDefault();
            return _this.geocoderSearch();
          }
        };
      })(this));
      return document.getElementById('search').addEventListener('click', (function(_this) {
        return function(event) {
          return _this.geocoderSearch();
        };
      })(this));
    };

    MapCanvasView.prototype.infowindowContent = function(data, updateButton) {
      var aff_span, button_format, buy_books, buybook_button, content, field_format, goodrd_button, gr_books, image_format, infotemplate;
      gr_books = 'http://www.goodreads.com/book/title/';
      buy_books = 'http://www.rjjulia.com/book/';
      field_format = '<br><span class="pllabel"><%= label %></span>';
      field_format += '<br><span class="plcontent"><%= content %></span>';
      button_format = '<br><div id="checkin"><button class="btn visited" ';
      button_format += 'id="<%=place_id %>">check-in</button></div>';
      image_format = '<img src="<%= image_url %>">';
      aff_span = '<span id="affbtns">';
      buybook_button = '<span class="buybook" id="<%= buy_isbn %>">';
      buybook_button += '<img src="/img/ib.png" id="rjjbuy"/></span>';
      goodrd_button = '<span class="reviewbook" id="<%= gr_isbn %>">';
      goodrd_button += '<img id="grbtn" src="/img/goodrd.png"></span>';
      aff_span += buybook_button + goodrd_button + '</span>';
      infotemplate = _.template(field_format);
      content = '<div class="plinfowindow">';
      content += '<span class="lead">' + data.title + ' by ' + data.author;
      content += '</span>';
      if (!!data.place_name) {
        content += infotemplate({
          label: 'location',
          content: data.place_name
        });
      }
      if (!!data.scene_time) {
        content += infotemplate({
          label: 'time',
          content: data.place_time
        });
      }
      if (!!data.actors) {
        content += infotemplate({
          label: 'characters',
          content: data.actors
        });
      }
      if (!!data.symbols) {
        content += infotemplate({
          label: 'symbols',
          content: data.symbols
        });
      }
      if (!!data.description) {
        content += infotemplate({
          label: 'description',
          content: data.description
        });
      }
      if (!!data.notes) {
        content += infotemplate({
          label: 'notes',
          content: data.notes
        });
      }
      content += infotemplate({
        label: 'visits',
        content: data.visits
      });
      if (!!data.date_added) {
        content += infotemplate({
          label: 'added',
          content: data.date_added
        });
      }
      if (!!data.image_url) {
        content += _.template(image_format, {
          image_url: data.image_url
        });
      }
      if (updateButton) {
        content += _.template(button_format, {
          place_id: data.id
        });
        this.handleCheckinButtonClick();
      }
      if (!!data.isbn) {
        content += _.template(aff_span, {
          gr_isbn: data.isbn,
          buy_isbn: data.isbn
        });
        this.trackButtonEvents();
      }
      content += '</div>';
      return content;
    };

    MapCanvasView.prototype.openInfowindowForPlace = function(place_key, position) {
      var url;
      url = '/places/info/' + place_key;
      return $.getJSON(url, (function(_this) {
        return function(data) {
          var iw;
          if (_this.placeInfowindow != null) {
            _this.placeInfowindow.close();
          }
          iw = _this.infowindow();
          iw.setPosition(position);
          iw.setContent(_this.infowindowContent(data, true));
          iw.open(_this.gmap);
          return _this.placeInfowindow = iw;
        };
      })(this));
    };

    MapCanvasView.prototype.mapEventTracking = function(data) {
      return ga('send', 'event', data.category, data.action, data.label, data.value);
    };

    MapCanvasView.prototype.trackButtonEvents = function() {
      $('#map_canvas').on('click', '.buybook', (function(_this) {
        return function(event) {
          var tracking;
          tracking = {
            'category': 'button',
            'action': 'click',
            'label': 'buy',
            'value': event.currentTarget.id
          };
          _this.mapEventTracking(tracking);
          return window.open('//www.rjjulia.com/book/' + event.currentTarget.id);
        };
      })(this));
      return $('#map_canvas').on('click', '.reviewbook', (function(_this) {
        return function(event) {
          var tracking;
          tracking = {
            'category': 'button',
            'action': 'click',
            'label': 'reviews',
            'value': event.currentTarget.id
          };
          _this.mapEventTracking(tracking);
          return window.open('//www.goodreads.com/book/isbn/' + event.currentTarget.id);
        };
      })(this));
    };

    MapCanvasView.prototype.handleCheckinButtonClick = function(event) {
      return $('#map_canvas').on('click', '.visited', (function(_this) {
        return function(event) {
          $('.visited').hide();
          _this.placeInfowindow.setContent('updating...');
          return $.getJSON('/places/visit/' + event.target.id, function(data) {
            return _this.placeInfowindow.setContent(_this.infowindowContent(data, false));
          });
        };
      })(this));
    };

    MapCanvasView.prototype.buildMarkerFromLocation = function(location) {
      var author, lat, lng, marker, markerParams, title;
      lat = location.get('latitude');
      lng = location.get('longitude');
      title = location.get('title');
      author = location.get('author');
      markerParams = this.settings.markerDefaults;
      markerParams.position = new google.maps.LatLng(lat, lng);
      markerParams.title = "" + title + " by " + author;
      marker = new google.maps.Marker(markerParams);
      this.locationMarkerEventHandler(location, marker);
      return marker;
    };

    MapCanvasView.prototype.locationMarkerEventHandler = function(location, marker) {
      return google.maps.event.addListener(marker, 'click', (function(_this) {
        return function(event) {
          var tracking, url;
          tracking = {
            'category': 'marker',
            'action': 'click',
            'label': 'open window'
          };
          _this.mapEventTracking(tracking);
          url = '/places/info/' + location.get('db_key');
          return $.getJSON(url, function(data) {
            var iw;
            iw = _this.infowindow();
            iw.setContent(_this.infowindowContent(data, true));
            iw.open(_this.gmap, marker);
            _this.placeInfowindow = iw;
            return _this.handleCheckinButtonClick();
          });
        };
      })(this));
    };

    MapCanvasView.prototype.dropMarkerForStoredLocation = function(location) {
      var marker;
      marker = this.buildMarkerFromLocation(location);
      return marker.setMap(this.gmap);
    };

    MapCanvasView.prototype.handleInputAttributes = function() {
      var dealWithIE9Inputs, field, fields, _i, _len, _results;
      fields = $('#iwcontainer input');
      dealWithIE9Inputs = function(el) {
        return el.setAttribute('value', el.getAttribute('placeholder'));
      };
      _results = [];
      for (_i = 0, _len = fields.length; _i < _len; _i++) {
        field = fields[_i];
        _results.push(dealWithIE9Inputs(field));
      }
      return _results;
    };

    return MapCanvasView;

  })(Backbone.View);

  PlacingLit.Views.RecentPlaces = (function(_super) {
    __extends(RecentPlaces, _super);

    function RecentPlaces() {
      return RecentPlaces.__super__.constructor.apply(this, arguments);
    }

    RecentPlaces.prototype.model = PlacingLit.Models.Location;

    RecentPlaces.prototype.el = '#recentcontent';

    RecentPlaces.prototype.max_desc_length = 100;

    RecentPlaces.prototype.initialize = function() {
      this.collection = new PlacingLit.Collections.Locations;
      this.collection.fetch({
        url: '/places/recent'
      });
      return this.listenTo(this.collection, 'all', this.render);
    };

    RecentPlaces.prototype.render = function(event) {
      if (event === 'sync') {
        return this.showNewestPlaces();
      }
    };

    RecentPlaces.prototype.showNewestPlaces = function() {
      var link, listFragment, listItems, location, locations, _i, _len;
      locations = this.collection.models;
      listFragment = document.createDocumentFragment();
      this.$el.find('li').remove();
      listItems = (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = locations.length; _i < _len; _i++) {
          location = locations[_i];
          _results.push(this.getPlaceLink(location));
        }
        return _results;
      }).call(this);
      for (_i = 0, _len = listItems.length; _i < _len; _i++) {
        link = listItems[_i];
        listFragment.appendChild(link);
      }
      this.$el.append(listFragment);
      return listFragment;
    };

    RecentPlaces.prototype.getPlaceLink = function(place) {
      var li, link, location, title;
      li = document.createElement('li');
      li.id = place.get('db_key');
      link = document.createElement('a');
      link.href = '/map/' + place.get('latitude') + ',' + place.get('longitude');
      link.href += '?key=' + place.get('db_key');
      title = place.get('title');
      link.textContent = title;
      if (place.get('location') != null) {
        location = place.get('location');
        if ((location + title).length > this.max_desc_length) {
          location = location.substr(0, this.max_desc_length - title.length) + '...';
        }
        link.textContent += ': ' + location;
      }
      li.appendChild(link);
      return li;
    };

    return RecentPlaces;

  })(Backbone.View);

  PlacingLit.Views.Countview = (function(_super) {
    __extends(Countview, _super);

    function Countview() {
      return Countview.__super__.constructor.apply(this, arguments);
    }

    Countview.prototype.el = '#count';

    Countview.prototype.initialize = function() {
      this.model = new PlacingLit.Models.Metadata;
      this.model.fetch({
        url: '/places/count'
      });
      return this.listenTo(this.model, 'all', this.render);
    };

    Countview.prototype.render = function(event) {
      if (event === 'change:count') {
        return this.showCount();
      }
    };

    Countview.prototype.showCount = function() {
      return $(this.el).text(this.model.get('count') + ' scenes have been mapped');
    };

    return Countview;

  })(Backbone.View);

  PlacingLit.Views.Allscenes = (function(_super) {
    __extends(Allscenes, _super);

    function Allscenes() {
      return Allscenes.__super__.constructor.apply(this, arguments);
    }

    Allscenes.prototype.el = '#scenelist';

    Allscenes.prototype.initialize = function() {
      this.collection = new PlacingLit.Collections.NewestLocationsByDate;
      this.collection.fetch();
      return this.listenTo(this.collection, 'all', this.render);
    };

    Allscenes.prototype.render = function(event) {
      if (event === 'sync') {
        return this.showAllScenes();
      }
    };

    Allscenes.prototype.showAllScenes = function() {
      var link, listFragment, listItems, location, locations, _i, _len;
      locations = this.collection.models;
      listFragment = document.createDocumentFragment();
      listItems = (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = locations.length; _i < _len; _i++) {
          location = locations[_i];
          _results.push(this.getPlaceLink(location));
        }
        return _results;
      }).call(this);
      for (_i = 0, _len = listItems.length; _i < _len; _i++) {
        link = listItems[_i];
        listFragment.appendChild(link);
      }
      this.$el.append(listFragment);
      return listFragment;
    };

    Allscenes.prototype.getPlaceLink = function(place) {
      var li, link;
      li = document.createElement('li');
      li.id = place.get('db_key');
      link = document.createElement('a');
      link.href = '/map/' + place.get('latitude') + ',' + place.get('longitude');
      link.href += '?key=' + place.get('db_key');
      link.textContent = place.get('title') + ': ' + place.get('location');
      li.appendChild(link);
      return li;
    };

    return Allscenes;

  })(Backbone.View);

  PlacingLit.Views.MapFilterView = (function(_super) {
    __extends(MapFilterView, _super);

    function MapFilterView() {
      return MapFilterView.__super__.constructor.apply(this, arguments);
    }

    MapFilterView.prototype.initialize = function(scenes) {
      if (this.collection == null) {
        this.collection = new PlacingLit.Collections.Locations();
      }
      this.listenTo(this.collection, 'all', this.render);
      return this.collection.reset(scenes);
    };

    MapFilterView.prototype.render = function(event) {
      return this.mapWithMarkers();
    };

    return MapFilterView;

  })(PlacingLit.Views.MapCanvasView);

}).call(this);
