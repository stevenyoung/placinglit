class AllScenes

  constructor: (@key) ->
    @key ?= window.location.search.split("=")[1]
    @list = new PlacingLit.Views.Allscenes()
    @elements =
      inputs:       $("#editform :input")
      editButton:   $("#editplacebutton")
      deleteButton: $("#deleteplacebutton")

  apiEndpoint: -> "/admin/edit?key=#{@key}"

  post: (data) -> $.ajax {url: @apiEndpoint(), type: "POST", data}

  destroy: (data) -> $.ajax {url: @apiEndpoint(), type: "DELETE", data}

  attachEvents: ->
    @elements.editButton.on   "click.allscenes", @editPlace
    @elements.deleteButton.on "click.allscenes", @deletePlace
    this

  detachEvents: (data) =>
    @elements.deleteButton
      .off('click.allscenes')
      .text(data)
    data

  buildDataFromElements: ->
    data = {}
    # jQuery supports using a normal form element for this. But since the
    # markup is a div with inputs inside we have to reference them
    # individually.
    fields = @elements.inputs.serializeArray()
    $.each fields, (i, field) -> data[field.name] = field.value
    data

  editPlace: =>
    @post(@buildDataFromElements())
      .then(@detachEvents)

  deletePlace: =>
    @destroy()
      .then(@detachEvents)
      .then => @elements.editButton.remove()

# TODO: export AllScenes to a global namespace to allow testing
$ -> new AllScenes().attachEvents()
