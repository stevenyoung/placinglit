#!/usr/bin/env coffee
describe "Location Model", ->
  it "should exist", ->
    expect(PlacingLit.Models.Location).toBeDefined()
  describe "Attributes", ->
    place = new PlacingLit.Models.Location
    it "should have default attributes", ->
      expect(place.attributes.name).toBeDefined()
      expect(place.attributes.title).toBeDefined()
