#!/usr/bin/env coffee


$(document).on('ready', ->
  $('#mapmodal').modal() if location.search == '?modal=1'
  if window.SCENES
    query = decodeURIComponent(window.location.pathname.replace('/map/filter/author/',''))
    if window.SCENES.length == 0
      mapCanvas = new PlacingLit.Views.MapCanvasView
      alertMessage = 'Whoa! No places found for ' + query + '. '
      alertMessage += 'But that\'s ok!. Be the first to map this author. '
      alertMessage += 'Click the map to add a book and author.'
      alert alertMessage
    else
      $('#querymodal').modal()
      mapCanvas = new PlacingLit.Views.MapFilterView(window.SCENES)
  else
    mapCanvas = new PlacingLit.Views.MapCanvasView
  mapCanvas.handleInputAttributes() if not Modernizr.input.placeholder
  mapCanvas.showInfowindowFormAtLocation()
)
