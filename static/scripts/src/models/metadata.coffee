#!/usr/bin/env coffee


class PlacingLit.Models.Metadata extends Backbone.Model
  url: '/places/count'

  initialize: ->


class PlacingLit.Collections.NewestLocations extends Backbone.Collection
  model: PlacingLit.Models.Location

  url :'/places/recent'

