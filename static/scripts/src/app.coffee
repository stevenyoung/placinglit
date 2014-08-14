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
  initialMapView: true

  field_labels:
    place_name: 'location'
    scene_time: 'time'
    actors: 'characters'
    symbols: 'symbols'
    description: 'description'
    notes: 'notes'
    visits: 'visits'
    date_added: 'added'

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
    maxTerrainZoom: 15


  mapOptions:
    #TODO styled maps?
    #https://developers.google.com/maps/documentation/javascript/styling#creating_a_styledmaptype
    zoom: 4
    #google.maps.MapTypeId.SATELLITE | ROADMAP | HYBRID
    mapTypeId: google.maps.MapTypeId.TERRAIN
    mapTypeControlOptions:
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
      position: google.maps.ControlPosition.TOP_RIGHT
    maxZoom: 25
    minZoom: 2
    zoomControl: true
    zoomControlOptions:
      style: google.maps.ZoomControlStyle.DEFAULT
      # position: google.maps.ControlPosition.TOP_LEFT
      position: google.maps.ControlPosition.LEFT_CENTER
    panControlOptions:
      # position: google.maps.ControlPosition.TOP_LEFT
      position: google.maps.ControlPosition.LEFT_CENTER

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
    @mapCenter = @gmap.getCenter()
    google.maps.event.addListener(@gmap, 'bounds_changed', @handleViewportChange)
    return @gmap

  handleViewportChange: (event) =>
    center = @gmap.getCenter()
    centerGeoPt =
      lat: center[Object.keys(center)[0]]
      lon: center[Object.keys(center)[1]]
    if @gmap.getZoom() >= @settings.maxTerrainZoom
      @gmap.setMapTypeId(google.maps.MapTypeId.ROADMAP)
    else
      @gmap.setMapTypeId(google.maps.MapTypeId.TERRAIN)

  updateCollection: (event) ->
    center = @gmap.getCenter()
    centerGeoPt =
      lat: center[Object.keys(center)[0]]
      lng: center[Object.keys(center)[1]]
    zoom = @gmap.getZoom()
    console.log('pan/zoom idle', centerGeoPt, zoom)
    if window.CENTER?
      console.log(window.CENTER)
      console.log(Math.abs(window.CENTER.lat - centerGeoPt.lat))
      console.log(Math.abs(window.CENTER.lng - centerGeoPt.lng))
    else
      window.CENTER = centerGeoPt

    query = '?lat=' + centerGeoPt.lat + '&lon=' + centerGeoPt.lng
    collection_url = '/places/near' + query
    update = false
    if Math.abs(window.CENTER.lat - centerGeoPt.lat) > 5
      update = true
    if Math.abs(window.CENTER.lng - centerGeoPt.lng) > 5
      update = true

    # window.CENTER = centerGeoPt
    if update
      window.CENTER = centerGeoPt
      @collection.reset(collection_url)

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
    @userInfowindow.open(map, @userMapsMarker)
    if not Modernizr.input.placeholder
      google.maps.event.addListener(@userInfowindow, 'domready', () =>
      @clearPlaceholders()
      )
    $('#map_canvas').find('#guidelines').on 'click', (event) =>
      $('#helpmodal').modal()
    google.maps.event.addListenerOnce @userInfowindow, 'closeclick', () =>
      @userMapsMarker.setMap(null)


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
        $('#map_canvas').find('#title').typeahead({source: title_data})

  suggestAuthors: () ->
    author_data = []
    $.ajax
      url: "/places/authors"
      success: (data) ->
        $.each data, (key, value) ->
          author_data.push(value.author.toString())
        $('#map_canvas').find('#author').typeahead({source: author_data})

  markersForEachScene: (markers) ->
    markers.each (model) => @dropMarkerForStoredLocation(model)

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
    # @markersForEachScene(@collection)
    @markerClustersForScenes(@allMarkers)
    @positionMap()
    $('#addscenebutton').on('click', @handleAddSceneButtonClick)
    $('#addscenebutton').show()

    # $('#hidemarkers').on('click', @hideMarkers)
    # $('#showmarkers').on('click', @showMarkers)

  positionMap: () ->
    if window.CENTER?
      mapcenter = new google.maps.LatLng(window.CENTER.lat, window.CENTER.lng)
      @gmap.setCenter(mapcenter)
      if (window.location.pathname.indexOf('collections') != -1)
        @gmap.setZoom(@settings.zoomLevel.wide)
      else
        @gmap.setZoom(@settings.zoomLevel.default)
      if (window.location.pathname.indexOf('author') != -1)
        @gmap.setZoom(@settings.zoomLevel.wide)
    else
      usaCoords =
        lat: 39.8282
        lng: -98.5795
      usacenter = new google.maps.LatLng(usaCoords.lat, usaCoords.lng)
      @gmap.setCenter(usacenter)
      @gmap.setZoom(2)
    if window.PLACEKEY?
      windowOptions = position: mapcenter
      @openInfowindowForPlace(window.PLACEKEY, windowOptions)
    @initialMapView = false

  handleMapClick: (event) ->
    @setUserMapMarker(@gmap, event.latLng)

  handleAddSceneButtonClick: =>
    @closeInfowindows() if @infowindows.length
    @setUserMapMarker(@gmap, @gmap.getCenter())
    # $('#addscenebutton').hide()
    # console.log('all markers', @allMarkers)
    # marker.setMap(null) for marker in @allMarkers

  setUserMapMarker: (map, location) ->
    @userMapsMarker.setMap(null) if @userMapsMarker?
    @userInfowindow.close() if @userInfowindow?
    @userMapsMarker = @markerFromMapLocation(map, location)
    @userMapsMarker.setMap(map)
    google.maps.event.addListenerOnce @userMapsMarker, 'click', (event) =>
      @isUserLoggedIn(@dropMarkerForNewLocation)
    @showUserMarkerHelp()

  showUserMarkerHelp: ->
    if @userMapsMarker
      loginWindowPosition = @userMapsMarker.getPosition()
      @closeInfowindows()
      @userInfowindow = @infowindow()
      content = '<div id="usermarker">'
      content += '<div>Drag this marker to place.<br>'
      content += 'Click the marker to add the scene</div></div>'
      @userInfowindow.setContent(content)
      @userInfowindow.setPosition(loginWindowPosition)
      @userInfowindow.open(@gmap, @userMapsMarker)
      google.maps.event.addListenerOnce @userInfowindow, 'closeclick', () =>
        @userMapsMarker.setMap(null)

  isUserLoggedIn: (callback) ->
    $.ajax
      datatype: 'json',
      url: '/user/status',
      success: (data) =>
        if data.status == 'logged in'
          callback.call(this)
        else
          @showLoginInfoWindow()

  showLoginInfoWindow: () ->
    if @userMapsMarker
      loginWindowPosition = @userMapsMarker.getPosition()
    else
      loginWindowPosition = @gmap.getCenter()
    @closeInfowindows()
    @userInfowindow = @infowindow()
    content = '<div id="usermarker">'
    content += '<div>You must be logged in to update content.</div><br>'
    login_url = document.getElementById('loginlink').href
    content += '<a href="' + login_url + '"><button>log in</button></a></p>'
    content += '</div>'
    @userInfowindow.setContent(content)
    @userInfowindow.setPosition(loginWindowPosition)
    @userInfowindow.open(@gmap, @userMapsMarker)
    google.maps.event.addListener @userInfowindow, 'closeclick', () =>
      @userMapsMarker.setMap(null)

  dropMarkerForNewLocation: () ->
    location = @userMapsMarker.getPosition()
    @showInfowindowFormAtLocation(@gmap, @userMapsMarker, location)
    @setUserPlaceFromLocation(location)
    @handleInfowindowButtonClick()
    @suggestTitles()
    @suggestAuthors()

  updateInfowindowWithMessage: (infowindow, response, refresh) ->
    console.log('new marker', response, refresh)
    textcontainer = '<div id="thankswindow">' + response.message + '</div>'
    infowindow.setContent(textcontainer)
    if refresh
      google.maps.event.addListenerOnce infowindow, 'closeclick', () =>
        @userMapsMarker.setMap(null)
        @showUpdatedMap()

  showUpdatedMapWithNewScene: (scene) ->


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
    $('#gcf').on('keydown', (event) =>
        if (event.which == 13 || event.keyCode == 13)
          event.preventDefault()
          @geocoderSearch()
      )
    $('#search').on 'click', (event) =>
      @geocoderSearch()

  sceneFieldsTemplate: ->
    field_format = '<br><span class="pllabel"><%= label %></span>'
    field_format += '<br><span class="plcontent"><%= content %></span>'
    return _.template(field_format)

  sceneButtonTemplate: ->
    aff_span = '<span id="affbtns">'
    buybook_button =  '<span class="buybook" id="<%= buy_isbn %>">'
    buybook_button += '<img src="/img/ib.png" id="rjjbuy"/></span>'
    goodrd_button = '<span class="reviewbook" id="<%= gr_isbn %>">'
    goodrd_button += '<img id="grbtn" src="/img/goodrd.png"></span>'
    aff_span += buybook_button + goodrd_button + '</span>'
    return _.template(aff_span)

  sceneCheckinButtonTemplate: ->
    button_format = '<br><div id="checkin"><button class="btn visited"'
    button_format += 'id="<%=place_id %>">check-in</button></div>'
    return _.template(button_format)

  sceneUserImageTemplate: ->
    img = '<img class="infopic" src="<%= image_url %>">'
    return _.template(img)

  sceneAPIImageTemplate: ->
    img = '<a target="_blank" href="//www.panoramio.com/photo/<%= image_id %>">'
    img += '<img class="infopic" src="//mw2.google.com/mw-panoramio/photos/'
    img += 'small/<%= image_id %>.jpg"></a>'
    return _.template(img)

  sceneTitleTemplate: ->
    return _.template('<span class="lead"><%= title %> by <%= author %></span>')

  buildInfowindow: (data, updateButton) ->
    @clearInfowindowClickEvents()
    content = '<div class="plinfowindow">'

    if !!data.image_url
      content += @sceneUserImageTemplate()(image_url: data.image_url)

    if !!data.image_data
      content += @sceneAPIImageTemplate()(image_id: data.image_data.photo_id)

    content += @sceneTitleTemplate()({title: data.title, author:data.author})
    for field of @field_labels
      label = @field_labels[field]
      if data[field]
        content += @sceneFieldsTemplate()({label: label, content:data[field]})
    if updateButton
      content += @sceneCheckinButtonTemplate()(place_id: data.id)
      @handleCheckinButtonClick()
    if !!data.isbn
      content += @sceneButtonTemplate()(gr_isbn: data.isbn, buy_isbn: data.isbn)
      @handleInfowindowButtonEvents()
    content += '</div>'
    return content

  openInfowindowForPlace: (place_key, windowOptions) ->
    console.log('open', windowOptions)
    # this can be triggered by a deep link or map marker click
    # TODO: marker clicks are tracked as events, deep links as pages- RESOLVE
    url = '/places/info/' + place_key
    window.PLACEKEY = null
    # console.log('open window', windowOptions)
    if windowOptions.marker
      tracking =
        'category': 'marker'
        'action': 'open window'
        'label': windowOptions.scene.get('title') + ':' + place_key
        'value' : 1
      @mapEventTracking(tracking)
    $.getJSON url, (data) =>
      @placeInfowindow.close() if @placeInfowindow?
      iw = @infowindow()
      iw.setContent(@buildInfowindow(data, true))
      if windowOptions.position
        iw.setPosition(windowOptions.position)
        iw.open(@gmap)
        @gmap.setCenter(windowOptions.position)
      else
        iw.open(@gmap, windowOptions.marker)
      @placeInfowindow = iw

      @handleCheckinButtonClick

  mapEventTracking: (data)->
    ga('send', 'event', data.category, data.action, data.label, data.value)

  handleInfowindowButtonEvents: () ->
    buy_url = '//www.rjjulia.com/aff/PlacingLiterature/book/v/'
    $('#map_canvas').on 'click', '.buybook', (event) =>
      tracking =
        'category': 'button'
        'action': 'buy'
        'label': event.currentTarget.id
        'value' : 1
      @mapEventTracking(tracking)
      window.open(buy_url + event.currentTarget.id)
    $('#map_canvas').on 'click', '.reviewbook', (event) =>
      tracking =
        'category': 'button'
        'action': 'reviews'
        'label': event.currentTarget.id
        'value' : 1
      @mapEventTracking(tracking)
      window.open('//www.goodreads.com/book/isbn/' + event.currentTarget.id)

  clearInfowindowClickEvents: ->
    $('#map_canvas').off 'click', '.visited'
    $('#map_canvas').off 'click', '.buybook'
    $('#map_canvas').off 'click', '.reviewbook'

  handleCheckinButtonClick: (event) ->
    $('#map_canvas').on 'click', '.visited', (event) =>
      @isUserLoggedIn( =>
        $('.visited').hide()
        @placeInfowindow.setContent('updating...')
        $.getJSON '/places/visit/'+event.target.id, (data) =>
          @placeInfowindow.setContent(@buildInfowindow(data, false))
      )

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
      windowOptions =
        marker: marker
        scene: location
      @openInfowindowForPlace(location.get('db_key'), windowOptions)

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
    editLink = document.createElement('a')
    editLink.href = '/admin/edit?key=' + place.get('db_key')
    editImage = document.createElement('img')
    editImage.src = '/img/edit-icon.png'
    editImage.style.height = '16px'
    editImage.className = 'editicon'
    editLink.appendChild(editImage)
    li.appendChild(editLink)
    li.appendChild(link)
    return li


class PlacingLit.Views.MapFilterView extends PlacingLit.Views.MapCanvasView
  #TODO - FIX THIS MONSTROSITY!!!
  filteredViewGeocoderSearch: () ->
    # console.log('geocoder search')
    address = document.getElementById('gcf').value
    # console.log('address')
    if address
      geocoder = new google.maps.Geocoder()
      geocoder.geocode {'address':address}, (results, status) =>
        if (status == google.maps.GeocoderStatus.OK)
          position = results[0].geometry.location
          lat = position[Object.keys(position)[0]]
          lng = position[Object.keys(position)[1]]
          mapUrl = window.location.protocol + '//' + window.location.host
          mapUrl += '/map/' + lat + ',' + lng
          # mapUrl += '/map?lat=' + lat + '&lon=' + lng
          window.location = mapUrl
        else
          alert("geocode was not successful: " + status)

  attachFilteredViewSearchHandler: ->
    $('#gcf').on('keydown',
      (event) =>
        if (event.which == 13 || event.keyCode == 13)
          event.preventDefault()
          @filteredViewGeocoderSearch()
      )
    $('#search').on 'click', (event) =>
      @filteredViewGeocoderSearch()

  initialize: (scenes) ->
    # console.log('filtered view', scenes)
    @collection ?= new PlacingLit.Collections.Locations()
    @listenTo @collection, 'all', @render
    @collection.reset(scenes)

  render: (event) ->
    @gmap ?= @googlemap()
    @allMarkers = @markerArrayFromCollection(@collection)
    @markerClustersForScenes(@allMarkers)
    # @markersForEachScene(@collection)
    @attachFilteredViewSearchHandler()
    mapcenter = new google.maps.LatLng(window.CENTER.lat, window.CENTER.lng)
    @gmap.setCenter(mapcenter)
    # console.log('zoom', @gmap.getZoom())
    @gmap.setZoom(@settings.zoomLevel.wide)
    $('#addscenebutton').on('click', @handleAddSceneButtonClick)
    $('#addscenebutton').show()

  updateCollection: (event) ->
    center = @gmap.getCenter()
    centerGeoPt =
      lat: center[Object.keys(center)[0]]
      lng: center[Object.keys(center)[1]]
    zoom = @gmap.getZoom()
    console.log('pan/zoom idle', centerGeoPt, zoom, @collection.length)
    if window.CENTER?
      console.log(window.CENTER)
      console.log(Math.abs(window.CENTER.lat - centerGeoPt.lat))
      console.log(Math.abs(window.CENTER.lng - centerGeoPt.lng))
    else
      window.CENTER = centerGeoPt

    update = false
    if Math.abs(window.CENTER.lat - centerGeoPt.lat) > 5
      update = true
    if Math.abs(window.CENTER.lng - centerGeoPt.lng) > 5
      update = true

    if update
      console.log('adding new scenes')
      query = '?lat=' + centerGeoPt.lat + '&lon=' + centerGeoPt.lng
      collection_url = '/places/near' + query
      new_markers = new PlacingLit.Collections.Locations
      new_markers.url = collection_url
      current_collection = @collection
      window.CENTER = centerGeoPt
      new_markers.fetch(
        success: (collection, response, options) =>
          console.log('current', current_collection.length,
                       current_collection.models)
          console.log('new', collection.length, collection.models)
          union = _.union(current_collection.models, collection.models)
          set_options =
            add: true
            remove: false
            merge: false
          @collection.reset(union, set_options)
          # @allMarkers = @markerArrayFromCollection(@collection)
          # @markersForEachScene(@allMarkers)
          # updated_collection = _.union(current_collection, collection)
          # console.log('updated', updated_collection.length)
          # @allMarkers = @markerArrayFromCollection(updated_collection)
          # @markersForEachScene(@collection)
          # @markerClustersForScenes(@allMarkers)
        error: (collection, response, options) =>
          console.log('error', collection, response, options)
        )

