#!/usr/bin/env coffee

class PlacingLit.Models.Location extends Backbone.Model
  defaults:
    title: 'Put Title Here'
    author: 'Someone\'s Name goes here'

  url: '/places/add'


class PlacingLit.Collections.Locations extends Backbone.Collection
  model: PlacingLit.Models.Location

  url: '/places/show'

  initialize: ->
    this.on 'add', (model)->
      alert 'adding model'
