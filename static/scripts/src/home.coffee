class Home

  constructor: ->
    @ENTER_KEY = 13
    @elements =
      cityInput:  $('#gcf')
      authorInput: $('#authorq')
      mapButtons: $('#hpbuttons').find('a')

  geocoderSearch: =>
    deferred = $.Deferred()
    location = @elements.cityInput.val()
    geocoder = new google.maps.Geocoder()
    geocoder.geocode({'address': location}, deferred.resolve)
    return deferred.promise()

  attachEvents: ->
    # city/location search
    @elements.cityInput.on 'keydown', (event) =>
      if (event.which == @ENTER_KEY) || (event.keyCode == @ENTER_KEY)
        event.preventDefault()
        @geocoderSearch()
        .then(@useGeocodedLocation)

    # filter by author
    @elements.authorInput.on 'keydown', (event) =>
      if (event.which == @ENTER_KEY) || (event.keyCode == @ENTER_KEY)
        event.preventDefault()
        @reloadWithFilteredMap('author', @elements.authorInput.val())

  suggestAuthors: ->
    authors = []
    authorInput = @elements.authorInput
    $.ajax
      url: "/places/authors"
      success: (data) ->
        $.each data, (key, value) ->
          authors.push(value.author.toString())
        authorInput.typeahead({source: authors})

  updateMapLinksWithLocation: (position) ->
    lat = position.coords.latitude
    lng = position.coords.longitude
    @elements.mapButtons.attr('href', 'map?lat=' + lat + '&lng=' + lng)

  getUserLocation: ->
    if navigator.geolocation
      navigator.geolocation.getCurrentPosition(
        updateMapLinksWithLocation, positionError)

  positionError: (error) ->
    console.log('error', error)
    console.log('client ip', window.REMOTE_ADDR)

  useGeocodedLocation: (results, status) =>
    if status == google.maps.GeocoderStatus.OK
      position = results[0].geometry.location
      location =
        lat:  position[Object.keys(position)[0]]
        lng:  position[Object.keys(position)[1]]
      @reloadWithLocatedMap(location)
    else
      alert("geocode was not successful: " + status)

  reloadWithLocatedMap: (location) ->
    @relocateWindowToMap('/map/' + location.lat + ',' + location.lng)

  reloadWithFilteredMap: (filter, value)->
    @relocateWindowToMap('/map/filter/' + filter + '/' + value)

  relocateWindowToMap: (path) ->
    mapUrl = window.location.protocol + '//' + window.location.host + path
    window.location = mapUrl

$ ->
  home = new Home()
  home.attachEvents()
  home.suggestAuthors()
  new PlacingLit.Views.RecentPlaces
  new PlacingLit.Views.Countview
  $('.carousel').carousel()  # bootstrap carousel
