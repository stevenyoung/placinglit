#!/usr/bin/env coffee
window.PlacingLit =
  Models: {}
  Collections: {}
  Views: {}


class PlacingLit.Models.Location extends Backbone.Model
  defaults:
    title: 'Put Title Here'
    author: 'Someone\'s Name goes here'

  url: '/places/add'


class PlacingLit.Models.Metadata extends Backbone.Model
  url: '/places/count'

  initialize: ->


class PlacingLit.Collections.Locations extends Backbone.Collection
  model: PlacingLit.Models.Location

  url: '/places/show'

  initialize: ->
    this.on 'add', (model)->
      alert 'adding model'


class PlacingLit.Collections.NewestLocations extends Backbone.Collection
  model: PlacingLit.Models.Location

  url :'/places/recent'


class PlacingLit.Collections.NewestLocationsByDate extends Backbone.Collection
  model: PlacingLit.Models.Location

  url :'/places/allbydate'


class PlacingLit.Views.MapView extends Backbone.View
  infowindows: []

  settings:
    zoomLevel:
      'wide' : 4
      'default': 10
      'close': 14
      'tight' : 21
      'increment' : 1

  model: PlacingLit.Models.Location

  mapOptions:
    #TODO styled maps?
    #https://developers.google.com/maps/documentation/javascript/styling#creating_a_styledmaptype
    zoom: 4
    #google.maps.MapTypeId.SATELLITE | ROADMAP | HYBRID
    mapTypeId: google.maps.MapTypeId.ROADMAP
    mapTypeControlOptions:
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
    maxZoom: 25
    minZoom: 2
    zoomControl: true
    zoomControlOptions:
      style: google.maps.ZoomControlStyle.DEFAULT
      position: google.maps.ControlPosition.TOP_LEFT
    panControlOptions:
      position: google.maps.ControlPosition.TOP_LEFT

  googlemap: (id)->
    return @gmap if @gmap?
    # console.log('new page map', id)
    @gmap = new google.maps.Map(document.getElementById(id), @mapOptions)
    google.maps.event.addListener(@gmap, 'click', (event) =>
      @handleMapClick(event)
    )
    return @gmap

  marker: ->
    @placeInfowindow.close() if @placeInfowindow?
    return new google.maps.Marker()

  infowindow: ->
    #return new google.maps.InfoWindow()
    @closeInfowindows() if @infowindows.length
    iw = new google.maps.InfoWindow()
    @infowindows.push(iw)
    return iw

  closeInfowindows: ->
    iw.close() for iw in @infowindows

  mappoint: (latitude, longitude)->
    return new google.maps.LatLng(latitude, longitude)

  markerFromMapLocation: (map, location)->
    markerSettings =
      position: location
      map: map
      animation: google.maps.Animation.DROP
      draggable: true
    return new google.maps.Marker(markerSettings)

  updateInfoWindow: (text, location, @map = @googlemap('hpmap')) ->
    infowindow = @infowindow()
    infowindow.setContent(text)
    infowindow.setPosition(location)
    infowindow.open(map)

  setUserPlaceFromLocation: (location) ->
    @userPlace = location

  showInfowindowFormAtLocation: (map, marker, location) ->
    @closeInfowindows()
    @userInfowindow = @infowindow()
    @userInfowindow.setContent(document.getElementById('iwcontainer').innerHTML)
    @userInfowindow.setPosition(location)
    @userInfowindow.open(map)
    if not Modernizr.input.placeholder
      google.maps.event.addListener(@userInfowindow, 'domready', () =>
      @clearPlaceholders()
      )
    document.getElementById('guidelines').addEventListener 'click', (event) =>
      $('#helpmodal').modal()


  clearPlaceholders: () ->
    # console.log('clearPlaceholders')
    $('#title').one('keypress', ()-> $('#title').val(''))
    $('#author').one('keypress', ()-> $('#author').val(''))
    $('#place_name').one('keypress', ()-> $('#place_name').val(''))
    $('#date').one('keypress', ()-> $('#date').val(''))
    $('#actors').one('keypress', ()-> $('#actors').val(''))
    $('#symbols').one('keypress', ()-> $('#symbols').val(''))
    $('#scene').one('keypress', ()-> $('#scene').val(''))
    $('#notes').one('keypress', ()-> $('#notes').val(''))
    $('#image_url').one('keypress', ()-> $('#image_url').val(''))

  closeInfowindows: ->
    @userInfowindow.close() if @userInfowindow?
    @placeInfowindow.close() if @placeInfowindow?

  clearMapMarker: (marker) ->
    marker.setMap(null)
    marker = null

  initialize: ->
    @userMapsMarker = null


class PlacingLit.Views.HomepagemapView extends PlacingLit.Views.MapView
  el: 'hpmap'
  locations: null
  settings:
    zoomLevel:
      'homepagedefault': 14

  cities:
    'newhaven':
      lat: 41.3060969411
      lng: -72.9260498285
    'duluth':
      lat: 46.7833
      lng: -92.1064
    'sanfrancisco':
      lat: 37.7750
      lng: -122.4183

  googlemap: (id)->
    # @mapOptions.disableDefaultUI = 'true'
    # super(id)

    # console.log('home page map view googlemap', @gmap)
    return @gmap if @gmap?
    @gmap = new google.maps.Map(document.getElementById(id), @mapOptions)
    # console.log('new home page map view googlemap', @gmap)
    mapStyle = 'toner-lite'
    @gmap.mapTypes.set(mapStyle, new google.maps.StamenMapType(mapStyle));
    @gmap.setMapTypeId(mapStyle);
    return @gmap

  mapMarkers: (locations) ->
    # @googlemap('hpmap')
    # console.log('hp map with markers', locations)
    @gmap ?= @googlemap('hpmap')
    @dropMarkerForStoredLocation(location) for location in locations
    mapcenter = new google.maps.LatLng(@cities.newhaven.lat, @cities.newhaven.lng)
    # console.log('map markers', @gmap)
    @gmap.setCenter(mapcenter)
    @gmap.setZoom(@settings.zoomLevel.homepagedefault)

  dropMarkerForStoredLocation: (location) ->
    pos = new google.maps.LatLng location.latitude, location.longitude
    markerParams =
      position: pos
      draggable: false
      animation: google.maps.Animation.DROP
      icon : '/img/book.png'
      title : "#{ location.title } by #{ location.author }"
    marker = new google.maps.Marker(markerParams)
    marker.setMap(@gmap)

  initialize: () ->
    @places ?= new PlacingLit.Collections.Locations
    @listenTo @places, 'all', @render
    @places.fetch()

  render: (event) ->
    # console.log(event)
    @mapMarkers(@places.models) if event is 'sync'


class PlacingLit.Views.MapCanvasView extends PlacingLit.Views.MapView
  el: 'map_canvas'
  locations: null
  userInfowindow: null
  placeInfowindow: null

  initialize: () ->
    # @collection ?= new PlacingLit.Collections.Locations
    @collection ?= new PlacingLit.Collections.Locations(url: '/places/1')
    # console.log(@collection)
    @listenTo @collection, 'all', @render
    @collection.fetch()

    # setup handler for geocoder searches
    @attachSearchHandler()

  render: (event) ->
    # console.log(event, this)
    @mapWithMarkers() if event is 'sync'

  suggestTitles: () ->
    title_data = []
    $.ajax
      url: "/places/titles"
      success: (data) ->
        $.each data, (key, value) ->
          title_data.push(value.title.toString())
        $('#title').typeahead({source: title_data})

  suggestAuthors: () ->
    author_data = []
    $.ajax
      url: "/places/authors"
      success: (data) ->
        $.each data, (key, value) ->
          author_data.push(value.author.toString())
        $('#author').typeahead({source: author_data})

  mapWithMarkers: () ->
    @gmap ?= @googlemap('map_canvas')

    # DROP ONE MARKER AT A TIME
    @collection.each (model) => @dropMarkerForStoredLocation(model)

    # OR BUILD ARRAY OF MARKERS
    # @allMarkers = @markerArrayFromCollection(@collection)
    # cluster_styles =  [
    #   {
    #     url: 'img/bigbook.png',
    #     height: 35,
    #     width: 35,
    #     # anchor: [16, 0],
    #     textColor: '#ff0000',
    #     textSize: 24
    #   }, {
    #     url: 'img/bigbook.png',
    #     height: 45,
    #     width: 45,
    #     # anchor: [24, 0],
    #     textColor: '#00ffff',
    #     textSize: 30
    #   }, {
    #     url: 'img/bigbook.png',
    #     height: 55,
    #     width: 55,
    #     # anchor: [32, 0],
    #     textColor: '#ffffff',
    #     textSize: 36
    #   }
    # ]

    # cluster_options =
    #   minimumClusterSize: 8
    #   # imagePath: document.location.origin + '/img/book'
    #   imagePath: document.location.origin + '/img/book'
    #   styles: cluster_styles

    # allMarkerCluster = new MarkerClusterer(@gmap, @allMarkers, cluster_options)
    # console.log('cluster style', allMarkerCluster, cluster_options)

    @positionMap()

  markerArrayFromCollection: (collection) ->
    markerParams =
        draggable: false
        animation: google.maps.Animation.DROP
        icon : '/img/book.png'
    buildMarker = (model) ->
        title= "#{ model.get('title') } by #{ model.get('author')}"
        markerParams.title = "#{ model.get('title') } by #{ model.get('author')}"
        markerParams.position = new google.maps.LatLng model.get('latitude'), model.get('longitude')
        marker = new google.maps.Marker(markerParams)
    return (buildMarker(model) for model in collection.models)

  positionMap: () ->
    if CENTER?
      mapcenter = new google.maps.LatLng(CENTER.lat, CENTER.lng)
      @gmap.setCenter(mapcenter)
      if (window.location.pathname.indexOf('collections') != -1)
        @gmap.setZoom(@settings.zoomLevel.wide)
      else
        @gmap.setZoom(@settings.zoomLevel.default)
    else
      usacenterCoords =
        lat: 39.8282
        lng: -98.5795
      usacenter = new google.maps.LatLng(usacenterCoords.lat, usacenterCoords.lng)
      @gmap.setCenter(usacenter)
      @gmap.setZoom(2)
    if PLACEKEY?
      @openInfowindowForPlace(PLACEKEY, mapcenter)

  handleMapClick: (event) ->
    @setUserMapMarker(@gmap, event.latLng)

  setUserMapMarker: (map, location) ->
    @userMapsMarker.setMap(null) if @userMapsMarker?
    @userInfowindow.close() if @userInfowindow?
    @userMapsMarker = @markerFromMapLocation(map, location)
    @userMapsMarker.setMap(map)
    google.maps.event.addListener(@userMapsMarker, 'click', (event) =>
      @isUserLoggedIn()
    )

  isUserLoggedIn: () ->
    $.ajax
      datatype: 'json',
      url: '/user/status',
      success: (data) =>
        if data.status == 'logged in'
          @dropMarkerForNewLocation()
        else
          @showLoginInfoWindow()

  showLoginInfoWindow: () ->
    @closeInfowindows()
    @userInfowindow = @infowindow()
    content = '<div id="maplogin">'
    content += '<div>You must be logged in to add content.</div>'
    login_url = document.getElementById('loginlink').href
    content += '<a href="' + login_url + '"><button>log in</button></a></p>'
    @userInfowindow.setContent(content)
    @userInfowindow.setPosition(@userMapsMarker.getPosition())
    @userInfowindow.open(@gmap)

  dropMarkerForNewLocation: () ->
    location = @userMapsMarker.getPosition()
    @showInfowindowFormAtLocation(@gmap, @userMapsMarker, location)
    @setUserPlaceFromLocation(location)
    @handleInfowindowButtonClick()
    @suggestTitles()
    @suggestAuthors()

  updateInfowindowWithMessage: (infowindow, text) ->
    textcontainer = '<div id="thankswindow">' + text.message + '</div>'
    infowindow.setContent(textcontainer)
    google.maps.event.addListener(infowindow, 'closeclick', () =>
      @showUpdatedMap()
    )

  showUpdatedMap: () ->
    m = new MapCanvasView

  handleInfowindowButtonClick : ()->
    # console.log('handle info window button')
    $addPlaceButton = $('#addplacebutton')
    # console.log('add place button', $addPlaceButton)
    $addPlaceButton = $('#map_canvas .infowindowform').find('.btn')
    # console.log('add place button', $addPlaceButton)
    $addPlaceButton.on('click', @addPlace) if $addPlaceButton?

  #TODO Why am I using => here? (jun 27)
  addPlace: () =>
    #remove 'add placebutton'
    message = '<span>adding... please wait...</span>'
    $('#addplacebutton').replaceWith(message)
    form_data =
      title: $('#title').val()
      author: $('#author').val()
      place_name: $('#place_name').val()
      # date: $('#date').val()
      # actors: $('#actors').val()
      # symbols: $('#symbols').val()
      scene: $('#scene').val()
      notes: $('#notes').val()
      image_url: $('#image_url').val()
      check_in: $('#check_in').prop('checked')
    form_data.latitude = @userPlace.lat()
    form_data.longitude = @userPlace.lng()
    # console.log('form data', form_data)
    required_fields = ['author', 'notes', 'place_name', 'scene', 'title']
    for field in required_fields
      if form_data[field].length == 0
        response =
          message: '<p>This feels incomplete. <br>
                    Close this window and drop a marker to start over. <br>
                    Fill out some of these fields so we can add your scene. <br>
                    Thanks.</p>'
        @updateInfowindowWithMessage(@userInfowindow, response)
        return false

    location = new PlacingLit.Models.Location()
    status = location.save(
      form_data,
        error: (model, xhr, options) =>
          console.log('add place error - map canvas view', model, xhr, options)
        success: (model, response, options) =>
          @updateInfowindowWithMessage(@userInfowindow, response)
    )

  geocoderSearch: () ->
    address = document.getElementById('gcf').value
    if address
      geocoder = new google.maps.Geocoder()
      geocoder.geocode({'address':address}, (results, status) =>
        if (status == google.maps.GeocoderStatus.OK)
          position = results[0].geometry.location
          @gmap.setCenter(position)
          @gmap.setZoom(@settings.zoomLevel.default)
          # @setUserMapMarker(@gmap, position)
        else
          alert("geocode was not successful: " + status)
      )

  attachSearchHandler: ->
    document.getElementById('gcf').addEventListener('keydown',
      (event) =>
        if (event.which == 13 || event.keyCode == 13)
          event.preventDefault()
          @geocoderSearch()
      )
    document.getElementById('search').addEventListener 'click', (event) =>
      @geocoderSearch()

  infowindowContent: (data, updateButton) ->
    # console.log(data)
    gr_books = 'http://www.goodreads.com/book/title/'
    buy_books = 'http://www.rjjulia.com/book/'
    field_format = '<br><span class="pllabel"><%= label %></span>'
    field_format += '<br><span class="plcontent"><%= content %></span>'
    button_format = '<br><div id="checkin"><button class="btn visited" '
    button_format += 'id="<%=place_id %>">check-in</button></div>'
    image_format = '<img src="<%= image_url %>">'
    aff_span = '<span id="affbtns">'
    buybook_button =  '<a target="_blank" href="<%= buy_url %>">'
    # buybook_button += '<button class="btn" id="rjjbuy">buy this book</button></a>'
    buybook_button += '<img src="/img/ib.png" id="rjjbuy"/></a>'
    goodrd_button = '<a target="_blank" href="<%= gr_url %>">'
    goodrd_button += '<img id="grbtn" src="/img/goodrd.png"></a>'
    aff_span += buybook_button + goodrd_button + '</span>'
    infotemplate = _.template(field_format)
    content = '<div class="plinfowindow">'
    content += '<span class="lead">' + data.title + ' by ' + data.author + '</span>'
    if !!data.place_name
      content += infotemplate({label:'location', content:data.place_name})
    if !!data.scene_time
      content += infotemplate({label:'time', content:data.place_time})
    if !!data.actors
      content += infotemplate({label:'characters', content:data.actors})
    if !!data.symbols
      content += infotemplate({label:'symbols', content:data.symbols})
    if !!data.description
      content += infotemplate({label:'description', content:data.description})
    if !!data.notes
      content += infotemplate({label:'notes', content:data.notes})
    content += infotemplate({label:'visits', content:data.visits})
    if !!data.date_added
      content += infotemplate({label:'added', content:data.date_added})
    if !!data.image_url
      content += _.template(image_format, image_url:data.image_url)
    if updateButton
      content += _.template(button_format, place_id:data.id )
      @handleCheckinButtonClick()
    if !!data.isbn
      content += _.template(aff_span,
                            gr_url: gr_books + data.isbn,
                            buy_url: buy_books + data.isbn)
    content += '</div>'
    return content

  openInfowindowForPlace: (place_key, position) ->
    url = '/places/info/' + place_key
    $.getJSON url, (data) =>
      @placeInfowindow.close() if @placeInfowindow?
      iw = @infowindow()
      iw.setPosition(position)
      iw.setContent(@infowindowContent(data, true))
      iw.open(@gmap)
      @placeInfowindow = iw

  handleCheckinButtonClick: (event) ->
    $('#map_canvas').on 'click', '.visited', (event) =>
      $('.visited').hide()
      @placeInfowindow.setContent('updating...')
      $.getJSON '/places/visit/'+event.target.id, (data) =>
        @placeInfowindow.setContent(@infowindowContent(data, false))

  dropMarkerForStoredLocation: (model) ->
    pos = new google.maps.LatLng model.get('latitude'), model.get('longitude')
    markerParams =
      position: pos
      draggable: false
      animation: google.maps.Animation.DROP
      #animation: null
      icon : '/img/book.png'
      title : "#{ model.get('title') } by #{ model.get('author')}"
    marker = new google.maps.Marker(markerParams)
    marker.setMap(@gmap)
    google.maps.event.addListener marker, 'click', =>
      url = '/places/info/' + model.get('db_key')
      $.getJSON url, (data) =>
        iw = @infowindow()
        iw.setContent(@infowindowContent(data, true))
        iw.open(@gmap, marker)
        @placeInfowindow = iw
        @handleCheckinButtonClick()

  handleInputAttributes: ->
    fields = $('#iwcontainer input')
    dealWithIE9Inputs = (el) ->
      el.setAttribute('value', el.getAttribute('placeholder'))
    dealWithIE9Inputs(field) for field in fields


class PlacingLit.Views.RecentPlaces extends Backbone.View
  model: PlacingLit.Models.Location
  el: '#recentcontent'
  max_desc_length: 100

  initialize: () ->
    @collection = new PlacingLit.Collections.Locations
    @collection.fetch(url: '/places/recent')
    @listenTo @collection, 'all', @render

  render: (event) ->
    # console.log('recent places collection', event)
    @showNewestPlaces() if event is 'sync'

  showNewestPlaces: () ->
    locations = @collection.models
    listFragment = document.createDocumentFragment()
    @$el.find('li').remove()
    listItems = (@getPlaceLink(location) for location in locations)
    listFragment.appendChild(link) for link in listItems
    @$el.append(listFragment)
    return listFragment

  getPlaceLink: (place) ->
    # console.log('place', place)
    li = document.createElement('li')
    li.id = place.get('db_key')
    # li.addEventListener('click', (event) =>
    #   @getPlaceDetails(event)
    # )
    link = document.createElement('a')
    link.href = '/map/' + place.get('latitude') + ',' + place.get('longitude')
    link.href += '?key=' + place.get('db_key')
    title_text = place.get('title')
    link.textContent = place.get('title')
    if place.get('location')?
      location_text = place.get('location')
      if (location_text + title_text).length > @max_desc_length
        location_text = location_text.substr(0, @max_desc_length - title_text.length) + '...'
      link.textContent += ': ' + location_text
    li.appendChild(link)
    return li


class PlacingLit.Views.Countview extends Backbone.View
  el: '#count'

  initialize: () ->
    @model = new PlacingLit.Models.Metadata
    @model.fetch(url: '/places/count')
    @listenTo @model, 'all', @render

  render: (event) ->
    # console.log('place count view', event)
    @showCount() if event is 'change:count'

  showCount: () ->
    $(@el).text(@model.get('count') + ' scenes have been mapped')


class PlacingLit.Views.Allscenes extends Backbone.View
  el: '#scenelist'

  initialize: () ->
    @collection = new PlacingLit.Collections.NewestLocationsByDate
    @collection.fetch()
    @listenTo @collection, 'all', @render

  render: (event) ->
    @showAllScenes() if event is 'sync'

  showAllScenes: () ->
    locations = @collection.models
    listFragment = document.createDocumentFragment()
    listItems = (@getPlaceLink(location) for location in locations)
    listFragment.appendChild(link) for link in listItems
    @$el.append(listFragment)
    return listFragment

  getPlaceLink: (place) ->
    # console.log('place', place)
    li = document.createElement('li')
    li.id = place.get('db_key')
    # li.addEventListener('click', (event) =>
    #   @getPlaceDetails(event)
    # )
    link = document.createElement('a')
    link.href = '/map/' + place.get('latitude') + ',' + place.get('longitude')
    link.href += '?key=' + place.get('db_key')
    link.textContent = place.get('title') + ': ' + place.get('location')
    li.appendChild(link)
    return li


class PlacingLit.Views.MapFilterView extends PlacingLit.Views.MapCanvasView
  initialize: (scenes) ->
    @collection ?= new PlacingLit.Collections.Locations()
    @listenTo @collection, 'all', @render
    @collection.reset(scenes)

  render: (event) ->
    @mapWithMarkers()

