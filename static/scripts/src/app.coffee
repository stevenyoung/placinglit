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


class PlacingLit.Collections.NewestLocations extends Backbone.Collection
  model: PlacingLit.Models.Location

  url :'/places/recent'


class PlacingLit.Collections.NewestLocationsByDate extends Backbone.Collection
  model: PlacingLit.Models.Location

  url :'/places/allbydate'


class PlacingLit.Views.MapCanvasView extends Backbone.View
  model: PlacingLit.Models.Location
  el: 'map_canvas'

  gmap: null
  infowindows: []
  locations: null
  userInfowindow: null
  placeInfowindow: null
  userMapsMarker: null
  allMarkers: []

  settings:
    zoomLevel:
      'wide' : 4
      'default': 10
      'close': 14
      'tight' : 21
      'increment' : 1
    markerDefaults:
      draggable: false
      animation: google.maps.Animation.DROP
      icon : '/img/book.png'

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

  initialize: (scenes) ->
    @collection ?= new PlacingLit.Collections.Locations()
    @listenTo @collection, 'all', @render
    @collection.fetch()
    # setup handler for geocoder searches
    @attachSearchHandler()

  render: (event) ->
    @mapWithMarkers() if event is 'sync'

  googlemap: ()->
    return @gmap if @gmap?
    map_elem = document.getElementById(@$el.selector)
    @gmap = new google.maps.Map(map_elem, @mapOptions)
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
    $('#map_canvas').find('#guidelines').on 'click', (event) =>
      $('#helpmodal').modal()


  clearPlaceholders: () ->
    $('#title').one('keypress', ()-> $('#title').val(''))
    $('#author').one('keypress', ()-> $('#author').val(''))
    $('#place_name').one('keypress', ()-> $('#place_name').val(''))
    $('#date').one('keypress', ()-> $('#date').val(''))
    $('#actors').one('keypress', ()-> $('#actors').val(''))
    $('#symbols').one('keypress', ()-> $('#symbols').val(''))
    $('#scene').one('keypress', ()-> $('#scene').val(''))
    $('#notes').one('keypress', ()-> $('#notes').val(''))
    $('#image_url').one('keypress', ()-> $('#image_url').val(''))

  clearMapMarker: (marker) ->
    marker.setMap(null)
    marker = null

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

  markersForEachScene: () ->
    @collection.each (model) => @dropMarkerForStoredLocation(model)

  markerArrayFromCollection: (collection) ->
    return (@buildMarkerFromLocation(model) for model in collection.models)

  markerClustersForScenes: (locations) ->
    cluster_options =
      minimumClusterSize: 5
    allMarkerCluster = new MarkerClusterer(@gmap, locations, cluster_options)

  hideMarkers: =>
    marker.setMap(null) for marker in @allMarkers

  showMarkers: =>
    marker.setMap(@gmap) for marker in @allMarkers

  mapWithMarkers: () ->
    @gmap ?= @googlemap()
    @allMarkers = @markerArrayFromCollection(@collection)
    # @markersForEachScene()
    @markerClustersForScenes(@allMarkers)
    @positionMap()
    # $('#hidemarkers').on('click', @hideMarkers)
    # $('#showmarkers').on('click', @showMarkers)

  positionMap: () ->
    if CENTER?
      mapcenter = new google.maps.LatLng(CENTER.lat, CENTER.lng)
      @gmap.setCenter(mapcenter)
      if (window.location.pathname.indexOf('collections') != -1)
        @gmap.setZoom(@settings.zoomLevel.wide)
      else
        @gmap.setZoom(@settings.zoomLevel.default)
    else
      usaCoords =
        lat: 39.8282
        lng: -98.5795
      usacenter = new google.maps.LatLng(usaCoords.lat, usaCoords.lng)
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

  updateInfowindowWithMessage: (infowindow, text, refresh) ->
    textcontainer = '<div id="thankswindow">' + text.message + '</div>'
    infowindow.setContent(textcontainer)
    if refresh
      google.maps.event.addListener(infowindow, 'closeclick', () =>
        @showUpdatedMap()
      )

  showUpdatedMap: () ->
    maps = new MapCanvasView

  handleInfowindowButtonClick : ()->
    $addPlaceButton = $('#map_canvas .infowindowform').find('#addplacebutton')
    $addPlaceButton.on('click', @addPlace) if $addPlaceButton?

  getFormValues: () ->
    $form = $('#map_canvas .infowindowform')
    form_data =
      title: $form.find('#title').val()
      author: $form.find('#author').val()
      place_name: $form.find('#place_name').val()
      # date: $('#date').val()
      # actors: $('#actors').val()
      # symbols: $('#symbols').val()
      scene: $form.find('#scene').val()
      notes: $form.find('#notes').val()
      image_url: $form.find('#image_url').val()
      check_in: $form.find('#check_in').prop('checked')
    form_data.latitude = @userPlace.lat()
    form_data.longitude = @userPlace.lng()
    return form_data

  isFormComplete: (form_data) ->
    required_fields = ['title', 'author', 'place_name', 'scene', 'notes']
    completed_entry = true
    @missing_fields = ''
    for field in required_fields
      if form_data[field].length == 0
        field_name = field.charAt(0).toUpperCase()
        field_name += field.substr(1).toLowerCase()
        field_name = field_name.replace('_', ' ')
        @missing_fields += 'Missing ' + field_name + '.</br>'
        completed_entry = false
    return completed_entry

  addPlace: () =>
    form_data = @getFormValues()
    if @isFormComplete(form_data)
      msg = '<span>adding... please wait...</span>'
      $('#map_canvas .infowindowform').find('#addplacebutton').replaceWith(msg)
      location = new PlacingLit.Models.Location()
      status = location.save(
        form_data,
          error: (model, xhr, options) =>
            console.log('add place error', model, xhr, options)
          success: (model, response, options) =>
            @updateInfowindowWithMessage(@userInfowindow, response, true)
      )
    else
      error_msg = '<p>Close this window and click the marker to start over. <br>
                  Fill out some of these fields so we can add your scene. <br>
                  Thanks.</p>'
      response =
        message: @missing_fields + error_msg
      @updateInfowindowWithMessage(@userInfowindow, response, false)
      return false


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
    gr_books = 'http://www.goodreads.com/book/title/'
    buy_books = 'http://www.rjjulia.com/book/'
    field_format = '<br><span class="pllabel"><%= label %></span>'
    field_format += '<br><span class="plcontent"><%= content %></span>'
    button_format = '<br><div id="checkin"><button class="btn visited" '
    button_format += 'id="<%=place_id %>">check-in</button></div>'
    image_format = '<img src="<%= image_url %>">'
    aff_span = '<span id="affbtns">'
    buybook_button =  '<span class="buybook" id="<%= buy_isbn %>">'
    buybook_button += '<img src="/img/ib.png" id="rjjbuy"/></span>'
    goodrd_button = '<span class="reviewbook" id="<%= gr_isbn %>">'
    goodrd_button += '<img id="grbtn" src="/img/goodrd.png"></span>'
    aff_span += buybook_button + goodrd_button + '</span>'
    infotemplate = _.template(field_format)
    content = '<div class="plinfowindow">'
    content += '<span class="lead">' + data.title + ' by ' + data.author
    content += '</span>'
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
                            gr_isbn: data.isbn,
                            buy_isbn: data.isbn)
      @trackButtonEvents()
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

  mapEventTracking: (data)->
    ga('send', 'event', data.category, data.action, data.label, data.value)

  trackButtonEvents: () ->
    $('#map_canvas').on 'click', '.buybook', (event) =>
      tracking =
        'category': 'button'
        'action': 'click'
        'label': 'buy'
        'value' : event.currentTarget.id
      @mapEventTracking(tracking)
      window.open('//www.rjjulia.com/book/' + event.currentTarget.id)
    $('#map_canvas').on 'click', '.reviewbook', (event) =>
      tracking =
        'category': 'button'
        'action': 'click'
        'label': 'reviews'
        'value' : event.currentTarget.id
      @mapEventTracking(tracking)
      window.open('//www.goodreads.com/book/isbn/' + event.currentTarget.id)


  handleCheckinButtonClick: (event) ->
    $('#map_canvas').on 'click', '.visited', (event) =>
      $('.visited').hide()
      @placeInfowindow.setContent('updating...')
      $.getJSON '/places/visit/'+event.target.id, (data) =>
        @placeInfowindow.setContent(@infowindowContent(data, false))

  buildMarkerFromLocation: (location) ->
    lat = location.get('latitude')
    lng = location.get('longitude')
    title = location.get('title')
    author = location.get('author')
    markerParams = @settings.markerDefaults
    markerParams.position = new google.maps.LatLng lat, lng
    markerParams.title = "#{ title } by #{ author }"
    marker = new google.maps.Marker(markerParams)
    @locationMarkerEventHandler(location, marker)
    return marker

  locationMarkerEventHandler: (location, marker) ->
    google.maps.event.addListener marker, 'click', (event) =>
      tracking =
        'category': 'marker'
        'action': 'click'
        'label': 'open window'
      @mapEventTracking(tracking)
      url = '/places/info/' + location.get('db_key')
      $.getJSON url, (data) =>
        iw = @infowindow()
        iw.setContent(@infowindowContent(data, true))
        iw.open(@gmap, marker)
        @placeInfowindow = iw
        @handleCheckinButtonClick()

  dropMarkerForStoredLocation: (location) ->
    marker = @buildMarkerFromLocation(location)
    marker.setMap(@gmap)

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
    li = document.createElement('li')
    li.id = place.get('db_key')
    link = document.createElement('a')
    link.href = '/map/' + place.get('latitude') + ',' + place.get('longitude')
    link.href += '?key=' + place.get('db_key')
    title = place.get('title')
    link.textContent = title
    if place.get('location')?
      location = place.get('location')
      if (location + title).length > @max_desc_length
        location = location.substr(0, @max_desc_length - title.length) + '...'
      link.textContent += ': ' + location
    li.appendChild(link)
    return li


class PlacingLit.Views.Countview extends Backbone.View
  el: '#count'

  initialize: () ->
    @model = new PlacingLit.Models.Metadata
    @model.fetch(url: '/places/count')
    @listenTo @model, 'all', @render

  render: (event) ->
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
