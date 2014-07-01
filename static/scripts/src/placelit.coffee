#!/usr/bin/env coffee

$(document).on('ready', ->
  $('#mapmodal').modal() if location.search == '?modal=1'
  if window.SCENES
    # scenes have been preloaded from query results
    path = window.location.pathname
    if (window.SCENES.length == 0) and (path.indexOf('author') != -1)
      author_path = '/map/filter/author/'
      author = decodeURIComponent(path.replace(author_path,''))
      mapCanvas = new PlacingLit.Views.MapCanvasView
      alertMessage = 'Whoa! No places found for ' + author + '. '
      alertMessage += 'But that\'s ok!. Be the first to map this author. '
      alertMessage += 'Click the map to add a book and author.'
      alert alertMessage
    else
      if (path.indexOf('collections') != -1)
        $('#querymodal').modal()
      if (path.indexOf('author') != -1)
        $('#querymodal').modal()
      mapCanvas = new PlacingLit.Views.MapFilterView(window.SCENES)
  else
    mapCanvas = new PlacingLit.Views.MapCanvasView
  mapCanvas.handleInputAttributes() if not Modernizr.input.placeholder
  mapCanvas.showInfowindowFormAtLocation()
)
