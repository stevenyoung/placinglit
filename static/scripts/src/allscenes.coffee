#!/usr/bin/coffee

$(document).on 'ready', ->
  list = new PlacingLit.Views.Allscenes()
  editPlace = ->
    $form = $('#editform')
    key = window.location.search.split('=')[1]
    form_data =
      title: $form.find('#title').val()
      author: $form.find('#author').val()
      place_name: $form.find('#place_name').val()
      scene: $form.find('#scene').val()
      description: $form.find('#description').val()
      notes: $form.find('#notes').val()
      image_url: $form.find('#image_url').val()
      actors: $form.find('#actors').val()
      scene_time: $form.find('#scenetime').val()
      symbols: $form.find('#symbols').val()
      ug_isbn: $form.find('#ug_isbn').val()
    $.ajax
      url: '/admin/edit?key=' + key
      type: 'POST'
      data: form_data

  deletePlace = ->
    console.log('delete')
    key = window.location.search.split('=')[1]
    $.ajax
      url: '/admin/edit?key=' + key
      type: 'DELETE'

  $('#editplacebutton').on 'click', (event) ->
    editPlace()

  $('#deleteplacebutton').on 'click', (event) ->
    deletePlace()