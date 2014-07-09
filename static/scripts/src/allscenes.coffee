#!/usr/bin/coffee

$(document).on 'ready', ->
  apiEndpoint = ->
    key = window.location.search.split('=')[1]
    "/admin/edit?key=#{key}"
  post    = (data) -> $.ajax {url: apiEndpoint(), type: "POST", data}
  destroy = (data) -> $.ajax {url: apiEndpoint(), type: "DELETE", data}

  buildDataFromElements ->
    data = {}
    # jQuery supports using a normal form element for this. But since the
    # markup is a div with inputs inside we have to reference them
    # indevidually.
    fields = $("#editform :input").serializeArray()
    $.each fields, (i, field) -> data[field.name] = field.value
    data

  list = new PlacingLit.Views.Allscenes()

  editPlace = ->
    post(buildDataFromElements())
      .then (data) ->
        $('#editplacebutton')
          .off('click.allscenes')
          .text(data)

  deletePlace = ->
    destroy()
      .then (data) ->
        $('#editplacebutton').remove()
        $('#deleteplacebutton')
          .off('click.allscenes')
          .text(data)

  $('#editplacebutton').on 'click.allscenes', editPlace
  $('#deleteplacebutton').on 'click.allscenes', deletePlace
