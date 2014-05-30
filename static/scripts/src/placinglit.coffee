#!/usr/bin/env coffee
window.PlacingLit =
  Models: {}
  Collections: {}
  Views: {}


class PlacingLit.Models.Location extends Backbone.Models
  defaults:
    title: 'Put Title Here'
    author: 'Someone\'s Name Goes Here'

  url: '/scene'


class PlacingLit.Collections.Locations extends Backbone.Collections
  url: '/scenes'


class PlacingLit.Views.GoogleMapsView extends Backbone.Views
  model: PlacingLit.Models.Location
  el: 'map_canvas'

  initialize: ->
    @collection ?= new PlacingLit.Collections.Locations
    @listenTo