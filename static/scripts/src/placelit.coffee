class PLMap

  constructor: ->
    @elements =
      modals:
        mapmodal: $('#mapmodal')
        querymodal: $('#querymodal')
    @path = window.location.pathname
    @scenes = window.SCENES

  showModal: (element) ->
    element.modal()

  isFiltered: ->
    if (@path.indexOf('collections') == -1) and (@path.indexOf('author') == -1)
      return false
    return true

  hasScenes: ->
    return @scenes and @scenes.length > 0

  selectMapView: ->
    if @isFiltered() and @hasScenes()
      return new PlacingLit.Views.MapFilterView(@scenes)
    return new PlacingLit.Views.MapCanvasView

  displayEmptyResultsError: ->
    author_path = '/map/filter/author/'
    author = decodeURIComponent(@path.replace(author_path,''))
    alertMessage = 'Whoa! No places found for ' + author + '. '
    alertMessage += 'But that\'s ok!. Be the first to map this author. '
    alertMessage += 'Click the map to add a book and author.'
    alert alertMessage

$ ->
  plmap = new PLMap()
  view = plmap.selectMapView()
  if location.search is '?modal=1'
    plmap.showModal(plmap.elements.modals.mapmodal)
  else if plmap.isFiltered()
    if plmap.scenes.length > 0
      plmap.showModal(plmap.elements.modals.querymodal)
    else
      plmap.displayEmptyResultsError()
  view.handleInputAttributes() if not Modernizr.input.placeholder
  view.showInfowindowFormAtLocation()
