#!/usr/bin/coffee

$(document).on 'ready', ->
  list = new PlacingLit.Views.Allscenes()
  editPlace = ->
    $form = $('#editform')
    key = window.location.search.split('=')[1]
    form_data =
      title: $form.find('#title').val()
      author: $form.find('#author').val()
      scenelocation: $form.find('#scenelocation').val()
      scenedescription: $form.find('#scenedescription').val()
      notes: $form.find('#notes').val()
      image_url: $form.find('#image_url').val()
      actors: $form.find('#actors').val()
      scenetime: $form.find('#scenetime').val()
      symbols: $form.find('#symbols').val()
      ug_isbn: $form.find('#ug_isbn').val()
    console.log(form_data)
    $.ajax
      url: '/admin/edit?key=' + key
      type: 'POST'
      data: form_data
      success: (data, status, xhr) =>
        $('#editplacebutton').off 'click'
        $('#editplacebutton').text(data)


  deletePlace = ->
    key = window.location.search.split('=')[1]
    $.ajax
      url: '/admin/edit?key=' + key
      type: 'DELETE'
      success: (data, status, xhr) =>
        $('#deleteplacebutton').off 'click'
        $('#deleteplacebutton').text(data)
        $('#editplacebutton').remove()

  $('#editplacebutton').on 'click', (event) ->
    editPlace()

  $('#deleteplacebutton').on 'click', (event) ->
    deletePlace()