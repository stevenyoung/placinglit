/**!
 * The MIT License
 *
 * Copyright (c) 2013 the angular-leaflet-directive Team, http://tombatossals.github.io/angular-leaflet-directive
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * angular-google-maps
 * https://github.com/tombatossals/angular-leaflet-directive
 *
 * @authors https://github.com/tombatossals/angular-leaflet-directive/graphs/contributors
 */

/*! angular-leaflet-directive 24-11-2013 */
!function() {
    "use strict";
    angular.module("leaflet-directive", []).directive("leaflet", ["$log", "$q", "leafletData", "leafletMapDefaults", "leafletHelpers", "leafletEvents", function(a, b, c, d, e, f) {
        var g;
        return {
            restrict: "EA",
            replace: !0,
            scope: {
                center: "=center",
                defaults: "=defaults",
                maxBounds: "=maxbounds",
                bounds: "=bounds",
                marker: "=marker",
                markers: "=markers",
                legend: "=legend",
                geojson: "=geojson",
                paths: "=paths",
                tiles: "=tiles",
                layers: "=layers",
                controls: "=controls",
                eventBroadcast: "=eventBroadcast"
            },
            template: '<div class="angular-leaflet-map"></div>',
            controller: ["$scope", function(a) {
                g = b.defer(), this.getMap = function() {
                    return g.promise
                }, this.getLeafletScope = function() {
                    return a
                }
            }
            ],
            link: function(b, h, i) {
                var j = e.isDefined, k = d.setDefaults(b.defaults, i.id), l = f.genDispatchMapEvent, m = f.getAvailableMapEvents();
                j(b.maxBounds) && (k.minZoom = void 0), j(i.width) && (isNaN(i.width) ? h.css("width", i.width) : h.css("width", i.width + "px")), j(i.height) && (isNaN(i.height) ? h.css("height", i.height) : h.css("height", i.height + "px")), j(i.marker) && a.warn("[AngularJS - Leaflet] The 'marker' property is currently deprecated, please use the 'markers' property instead.");
                var n = new L.Map(h[0], {
                    maxZoom: k.maxZoom,
                    minZoom: k.minZoom,
                    keyboard: k.keyboard,
                    dragging: k.dragging,
                    zoomControl: k.zoomControl,
                    doubleClickZoom: k.doubleClickZoom,
                    scrollWheelZoom: k.scrollWheelZoom,
                    attributionControl: k.attributionControl,
                    crs: k.crs
                });
                if (g.resolve(n), c.setMap(n, i.id)
                    , j(i.center) || (a.warn("[AngularJS - Leaflet] 'center' is undefined in the current scope, did you forget to initialize it?"), n.setView([k.center.lat, k.center.lng], k.center.zoom)), !j(i.tiles)&&!j(i.layers)) {
                    var o = L.tileLayer(k.tileLayer, k.tileLayerOptions);
                    o.addTo(n), c.setTiles(o)
                }
                if (j(n.zoomControl) && j(k.zoomControlPosition) && n.zoomControl.setPosition(k.zoomControlPosition), !j(i.eventBroadcast)
                    )for (var p = "broadcast", q = 0; q < m.length; q++) {
                    var r = m[q];
                    n.on(r, l(b, r, p), {
                        eventName: r
                    })
                }
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("center", ["$log", "$parse", "leafletMapDefaults", "leafletHelpers", function(a, b, c, d) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(e, f, g, h) {
                {
                    var i = d.isDefined, j = (d.isNumber, d.safeApply), k = d.isValidCenter, l = h.getLeafletScope(), m = l.center;
                    d.equalsBounds, d.createLeafletBounds, l.bounds
                }
                h.getMap().then(function(d) {
                    c.getDefaults(g.id).then(function(c) {
                        if (i(m)) {
                            m.autoDiscover===!0 && d.locate({
                                setView: !0,
                                maxZoom: c.maxZoom
                            });
                            var e = {
                                lat: b("center.lat"),
                                lng: b("center.lng"),
                                zoom: b("center.zoom")
                            }
                        } else
                            a.warn("[AngularJS - Leaflet] 'center' is undefined in the current scope, did you forget to initialize it?"), d.setView([c.center.lat, c.center.lng], c.center.zoom);
                        var f=!1;
                        l.$watch("center", function(b) {
                            return k(b) ? (f || d.setView([b.lat, b.lng], b.zoom), void 0) : (a.warn("[AngularJS - Leaflet] invalid 'center'"), d.setView([c.center.lat, c.center.lng], c.center.zoom), void 0)
                        }, !0), d.on("movestart", function() {
                            f=!0
                        }), d.on("moveend", function() {
                            f=!1, j(l, function(a) {
                                e && (e.lat.assign(a, d.getCenter().lat), e.lng.assign(a, d.getCenter().lng), e.zoom.assign(a, d.getZoom()))
                            })
                        })
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("tiles", ["$log", "leafletData", "leafletMapDefaults", "leafletHelpers", function(a, b, c, d) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(e, f, g, h) {
                var i = d.isDefined, j = h.getLeafletScope(), k = j.tiles;
                h.getMap().then(function(d) {
                    c.getDefaults(g.id).then(function(c) {
                        if (!i(k)&&!i(k.url))
                            return a.warn("[AngularJS - Leaflet] The 'tiles' definition doesn't have the 'url' property."), void 0;
                        var e;
                        j.$watch("tiles", function(a) {
                            var f = c.tileLayerOptions, h = c.tileLayer;
                            return !i(a.url) && i(e) ? (d.removeLayer(e), void 0) : i(e) ? i(a.url) && i(a.options)&&!angular.equals(a.options, f) ? (d.removeLayer(e), f = c.tileLayerOptions, angular.copy(a.options, f), h = a.url, e = L.tileLayer(h, f), e.addTo(d), b.setTiles(e, g.id), void 0) : (i(a.url) && e.setUrl(a.url), void 0) : (i(a.options) && angular.copy(a.options, f), i(a.url) && (h = a.url), e = L.tileLayer(h, f), e.addTo(d), b.setTiles(e, g.id), void 0)
                        }, !0)
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("legend", ["$log", "leafletHelpers", function(a, b) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(c, d, e, f) {
                var g = b.isArray, h = b.isDefined, i = f.getLeafletScope(), j = i.legend;
                h(j) && f.getMap().then(function(b) {
                    if (g(j.colors) && g(j.labels) && j.colors.length === j.labels.length) {
                        var c = j.legendClass ? j.legendClass: "legend", d = j.position || "bottomright", e = L.control({
                            position: d
                        });
                        e.onAdd = function() {
                            for (var a = L.DomUtil.create("div", c), b = 0; b < j.colors.length; b++)
                                a.innerHTML += '<div><i style="background:' + j.colors[b] + '"></i>' + j.labels[b] + "</div>";
                            return a
                        }, e.addTo(b)
                    } else
                        a.warn("[AngularJS - Leaflet] legend.colors and legend.labels must be set.")
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("geojson", ["$log", "$rootScope", "leafletData", "leafletHelpers", function(a, b, c, d) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(a, e, f, g) {
                var h = d.safeApply, i = d.isDefined, j = g.getLeafletScope(), k = {};
                g.getMap().then(function(a) {
                    j.$watch("geojson", function(e) {
                        if (i(k) && a.hasLayer(k) && a.removeLayer(k), i(e) && i(e.data)
                            ) {
                            var f = e.resetStyleOnMouseout, g = e.onEachFeature;
                            g || (g = function(a, c) {
                                d.LabelPlugin.isLoaded() && i(e.label) && c.bindLabel(a.properties.description), c.on({
                                    mouseover: function(c) {
                                        h(j, function() {
                                            e.selected = a, b.$broadcast("leafletDirectiveMap.geojsonMouseover", c)
                                        })
                                    },
                                    mouseout: function(a) {
                                        f && k.resetStyle(a.target), h(j, function() {
                                            e.selected = void 0, b.$broadcast("leafletDirectiveMap.geojsonMouseout", a)
                                        })
                                    },
                                    click: function(a) {
                                        h(j, function() {
                                            b.$broadcast("leafletDirectiveMap.geojsonClick", e.selected, a)
                                        })
                                    }
                                })
                            }), e.options = {
                                style: e.style,
                                onEachFeature: g
                            }, k = L.geoJson(e.data, e.options), c.setGeoJSON(k), k.addTo(a)
                        }
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("layers", ["$log", "$q", "leafletData", "leafletHelpers", "leafletMapDefaults", function(a, b, c, d, e) {
        var f;
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            controller: ["$scope", function() {
                f = b.defer(), this.getLayers = function() {
                    return f.promise
                }
            }
            ],
            link: function(b, g, h, i) {
                var j = d, k = d.isDefined, l = d.isString, m = {}, n = i.getLeafletScope(), o = n.layers;
                i.getMap().then(function(b) {
                    e.getDefaults(h.id).then(function(d) {
                        function e(b) {
                            if (!l(b.type))
                                return a.error("[AngularJS - Leaflet] A base layer must have a type"), null;
                            if ("xyz" !== b.type && "wms" !== b.type && "group" !== b.type && "markercluster" !== b.type && "google" !== b.type && "bing" !== b.type && "imageOverlay" !== b.type)
                                return a.error('[AngularJS - Leaflet] A layer must have a valid type: "xyz, wms, group, google"'), null;
                            if (("xyz" === b.type || "wms" === b.type || "imageOverlay" === b.type)&&!l(b.url))
                                return a.error("[AngularJS - Leaflet] A base layer must have an url"), null;
                            if ("imageOverlay" === b.type && void 0 === b.bounds&&!l(b)
                                )return a.error("[AngularJS - Leaflet] An imageOverlay layer must have bounds"), null;
                            if (!l(b.name))
                                return a.error("[AngularJS - Leaflet] A base layer must have a name"), null;
                            (void 0 === b.layerParams || null === b.layerParams || "object" != typeof b.layerParams) && (b.layerParams = {}), (void 0 === b.layerOptions || null === b.layerOptions || "object" != typeof b.layerOptions) && (b.layerOptions = {});
                            var c = null;
                            for (var d in b.layerParams)
                                b.layerOptions[d] = b.layerParams[d];
                            switch (b.type) {
                            case"xyz":
                                c = g(b.url, b.layerOptions);
                                break;
                            case"wms":
                                c = i(b.url, b.layerOptions);
                                break;
                            case"group":
                                c = p();
                                break;
                            case"markercluster":
                                c = q(b.layerOptions);
                                break;
                            case"google":
                                c = r(b.layerType, b.layerOptions);
                                break;
                            case"bing":
                                c = s(b.bingKey, b.layerOptions);
                                break;
                            case"imageOverlay":
                                c = t(b.url, b.bounds, b.layerOptions);
                                break;
                            default:
                                c = null
                            }
                            return c
                        }
                        function g(a, b) {
                            var c = L.tileLayer(a, b);
                            return c
                        }
                        function i(a, b) {
                            var c = L.tileLayer.wms(a, b);
                            return c
                        }
                        function p() {
                            var a = L.layerGroup();
                            return a
                        }
                        function q(a) {
                            if (j.MarkerClusterPlugin.isLoaded()) {
                                var b = new L.MarkerClusterGroup(a);
                                return b
                            }
                            return null
                        }
                        function r(a, b) {
                            if (a = a || "SATELLITE", j.GoogleLayerPlugin.isLoaded()
                                ) {
                                var c = new L.Google(a, b);
                                return c
                            }
                            return null
                        }
                        function s(a, b) {
                            if (j.BingLayerPlugin.isLoaded()) {
                                var c = new L.BingLayer(a, b);
                                return c
                            }
                            return null
                        }
                        function t(a, b, c) {
                            var d = L.imageOverlay(a, b, c);
                            return d
                        }
                        if (k(o)) {
                            if (!k(o.baselayers) || Object.keys(o.baselayers).length <= 0)
                                return a.error("[AngularJS - Leaflet] At least one baselayer has to be defined"), void 0;
                            f.resolve(m), c.setLayers(m, h.id), m.baselayers = {}, m.controls = {}, m.controls.layers = new L.control.layers, m.controls.layers.setPosition(d.controlLayersPosition), m.controls.layers.addTo(b);
                            var u=!1;
                            for (var v in o.baselayers) {
                                var w = e(o.baselayers[v]);
                                null !== w && (m.baselayers[v] = w, o.baselayers[v].top===!0 && (b.addLayer(m.baselayers[v]), u=!0), m.controls.layers.addBaseLayer(m.baselayers[v], o.baselayers[v].name))
                            }
                            !u && Object.keys(m.baselayers).length > 0 && b.addLayer(m.baselayers[Object.keys(o.baselayers)[0]]), m.overlays = {};
                            for (v in o.overlays) {
                                var x = e(o.overlays[v]);
                                null !== x && (m.overlays[v] = x, o.overlays[v].visible===!0 && b.addLayer(m.overlays[v]), m.controls.layers.addOverlay(m.overlays[v], o.overlays[v].name))
                            }
                            n.$watch("layers.baselayers", function(c) {
                                for (var d in m.baselayers)
                                    void 0 === c[d] && (m.controls.layers.removeLayer(m.baselayers[d]), b.hasLayer(m.baselayers[d]) && b.removeLayer(m.baselayers[d]), delete m.baselayers[d]);
                                for (var f in c)
                                    if (void 0 === m.baselayers[f]) {
                                        var g = e(c[f]);
                                        null !== g && (m.baselayers[f] = g, c[f].top===!0 && b.addLayer(m.baselayers[f]), m.controls.layers.addBaseLayer(m.baselayers[f], c[f].name))
                                    }
                                if (Object.keys(m.baselayers).length <= 0)
                                    a.error("[AngularJS - Leaflet] At least one baselayer has to be defined");
                                else {
                                    var h=!1;
                                    for (var i in m.baselayers)
                                        if (b.hasLayer(m.baselayers[i])) {
                                            h=!0;
                                            break
                                        }
                                    h || b.addLayer(m.baselayers[Object.keys(o.baselayers)[0]])
                                }
                            }, !0), n.$watch("layers.overlays", function(a) {
                                for (var c in m.overlays)
                                    void 0 === a[c] && (m.controls.layers.removeLayer(m.overlays[c]), b.hasLayer(m.overlays[c]) && b.removeLayer(m.overlays[c]), delete m.overlays[c]);
                                for (var d in a)
                                    if (void 0 === m.overlays[d]) {
                                        var f = e(a[d]);
                                        null !== f && (m.overlays[d] = f, m.controls.layers.addOverlay(m.overlays[d], a[d].name), a[d].visible===!0 && b.addLayer(m.overlays[d]))
                                    }
                            }, !0)
                        }
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("bounds", ["$log", "leafletHelpers", function(a, b) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(c, d, e, f) {
                {
                    var g = b.isDefined, h = (b.isNumber, b.createLeafletBounds), i = f.getLeafletScope();
                    b.safeApply, i.bounds
                }
                f.getMap().then(function(b) {
                    b.whenReady(function() {
                        i.$watch("bounds", function(c) {
                            if (!g(c))
                                return a.error("[AngularJS - Leaflet] Invalid bounds"), void 0;
                            var d = h(c);
                            b.getBounds().equals(d) || b.fitBounds(d)
                        }, !0)
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("markers", ["$log", "$rootScope", "$q", "leafletData", "leafletHelpers", "leafletMapDefaults", "leafletEvents", function(a, b, c, d, e, f, g) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: ["leaflet", "?layers"],
            link: function(h, i, j, k) {
                var l = k[0], m = e, n = e.isDefined, o = e.isDefinedAndNotNull, p = e.isString, q = e.isNumber, r = e.safeApply, s = l.getLeafletScope(), t = s.markers, u = g.getAvailableMarkerEvents();
                l.getMap().then(function(g) {
                    f.getDefaults(j.id).then(function(f) {
                        var h, i = {}, l = {};
                        h = n(k[1]) ? k[1].getLayers : function() {
                            var a = c.defer();
                            return a.resolve(), a.promise
                        };
                        var v = L.Icon.extend({
                            options: {
                                iconUrl: f.icon.url,
                                iconRetinaUrl: f.icon.retinaUrl,
                                iconSize: f.icon.size,
                                iconAnchor: f.icon.anchor,
                                labelAnchor: f.icon.labelAnchor,
                                popupAnchor: f.icon.popup,
                                shadowUrl: f.icon.shadow.url,
                                shadowRetinaUrl: f.icon.shadow.retinaUrl,
                                shadowSize: f.icon.shadow.size,
                                shadowAnchor: f.icon.shadow.anchor
                            }
                        });
                        n(t) && h().then(function(c) {
                            function f(d, f, g) {
                                function i(a, c) {
                                    return function(e) {
                                        var g = "leafletDirectiveMarker." + a, h = d.replace("markers.", "");
                                        "click" === a ? r(s, function() {
                                            b.$broadcast("leafletDirectiveMarkersClick", h)
                                        }) : "dragend" === a && (r(s, function() {
                                            f.lat = j.getLatLng().lat, f.lng = j.getLatLng().lng
                                        }), f.message && f.focus===!0 && j.openPopup()), r(s, function(a) {
                                            "emit" === c ? a.$emit(g, {
                                                markerName: h,
                                                leafletEvent: e
                                            }) : b.$broadcast(g, {
                                                markerName: h,
                                                leafletEvent: e
                                            })
                                        })
                                    }
                                }
                                var j = h(f);
                                if (n(f.layer)) {
                                    if (!p(f.layer))
                                        return a.error("[AngularJS - Leaflet] A layername must be a string"), null;
                                    if (!o(c))
                                        return a.error("[AngularJS - Leaflet] You must add layers to the directive if used in a marker"), null;
                                    if (!o(c.overlays))
                                        return a.error("[AngularJS - Leaflet] You must add layers overlays to the directive if used in a marker"), null;
                                    if (!o(c.overlays[f.layer]))
                                        return a.error("[AngularJS - Leaflet] You must use a name of an existing layer"), null;
                                    var k = c.overlays[f.layer];
                                    if (!(k instanceof L.LayerGroup))
                                        return a.error('[AngularJS - Leaflet] A marker can only be added to a layer of type "group"'), null;
                                    k.addLayer(j), g.hasLayer(j) && f.focus===!0 && j.openPopup()
                                } else
                                    n(f.group) ? (n(l[f.group]) || (l[f.group] = L.markerClusterGroup(), g.addLayer(l[f.group])), l[f.group].addLayer(j)) : g.addLayer(j), e.LabelPlugin.isLoaded() && n(f.label) && n(f.label.options) && f.label.options.noHide===!0 && j.showLabel(), f.focus===!0 && j.openPopup();
                                var t, w, x = [], y = "broadcast";
                                if (void 0 === s.eventBroadcast || null === s.eventBroadcast)
                                    x = u;
                                else if ("object" != typeof s.eventBroadcast)
                                    a.warn("[AngularJS - Leaflet] event-broadcast must be an object check your model.");
                                else if (void 0 === s.eventBroadcast.marker || null === s.eventBroadcast.marker)
                                    x = u;
                                else if ("object" != typeof s.eventBroadcast.marker)
                                    a.warn("[AngularJS - Leaflet] event-broadcast.marker must be an object check your model.");
                                else {
                                    void 0 !== s.eventBroadcast.marker.logic && null !== s.eventBroadcast.marker.logic && ("emit" !== s.eventBroadcast.marker.logic && "broadcast" !== s.eventBroadcast.marker.logic ? a.warn("[AngularJS - Leaflet] Available event propagation logic are: 'emit' or 'broadcast'.") : "emit" === s.eventBroadcast.marker.logic && (y = "emit"));
                                    var z=!1, A=!1;
                                    if (void 0 !== s.eventBroadcast.marker.enable && null !== s.eventBroadcast.marker.enable && "object" == typeof s.eventBroadcast.marker.enable && (z=!0)
                                        , void 0 !== s.eventBroadcast.marker.disable && null !== s.eventBroadcast.marker.disable && "object" == typeof s.eventBroadcast.marker.disable && (A=!0), z && A)a.warn("[AngularJS - Leaflet] can not enable and disable events at the same time");
                                    else if (z || A)
                                        if (z)
                                            for (t = 0; t < s.eventBroadcast.marker.enable.length; t++)
                                                w = s.eventBroadcast.marker.enable[t], -1 !== x.indexOf(w) ? a.warn("[AngularJS - Leaflet] This event " + w + " is already enabled") : -1 === u.indexOf(w) ? a.warn("[AngularJS - Leaflet] This event " + w + " does not exist") : x.push(w);
                                        else
                                            for (x = u, t = 0; t < s.eventBroadcast.marker.disable.length; t++) {
                                                w = s.eventBroadcast.marker.disable[t];
                                                var B = x.indexOf(w);
                                                -1 === B ? a.warn("[AngularJS - Leaflet] This event " + w + " does not exist or has been already disabled") : x.splice(B, 1)
                                            } else
                                                a.warn("[AngularJS - Leaflet] must enable or disable events")
                                        }
                                for (t = 0; t < x.length; t++)
                                    w = x[t], j.on(w, i(w, y), {
                                    eventName: w,
                                    scope_watch_name: d
                                });
                                var C = s.$watch(d, function(b, d) {
                                    if (!o(b)) {
                                        if (j.closePopup(), o(c) && n(c.overlays)
                                            )for (var e in c.overlays)
                                            c.overlays[e]instanceof L.LayerGroup && c.overlays[e].hasLayer(j) && c.overlays[e].removeLayer(j);
                                        return g.removeLayer(j), C(), void 0
                                    }
                                    if (n(d)) {
                                        if (p(b.layer)) {
                                            if (o(d.layer) || d.layer !== b.layer)
                                                if ("string" == typeof d.layer && void 0 !== c.overlays[d.layer] && c.overlays[d.layer].hasLayer(j) && c.overlays[d.layer].removeLayer(j)
                                                    , j.closePopup(), g.hasLayer(j) && g.removeLayer(j), void 0 !== c.overlays[b.layer]) {
                                                var f = c.overlays[b.layer];
                                                f instanceof L.LayerGroup ? (f.addLayer(j), g.hasLayer(j) && b.focus===!0 && j.openPopup()) : a.error('[AngularJS - Leaflet] A marker can only be added to a layer of type "group"')
                                            } else
                                                a.error("[AngularJS - Leaflet] You must use a name of an existing layer")
                                            } else
                                                p(d.layer) && (n(c.overlays[d.layer]) && c.overlays[d.layer].hasLayer(j) && (c.overlays[d.layer].removeLayer(j), j.closePopup()), g.hasLayer(j) || g.addLayer(j));
                                        if (void 0 === b.draggable || null === b.draggable || b.draggable!==!0 ? void 0 !== d.draggable && null !== d.draggable && d.draggable===!0 && j.dragging && j.dragging.disable()
                                            : (void 0 === d.draggable || null === d.draggable || d.draggable!==!0) && (j.dragging ? j.dragging.enable() : L.Handler.MarkerDrag && (j.dragging = new L.Handler.MarkerDrag(j), j.options.draggable=!0, j.dragging.enable())), void 0 === b.icon || null === b.icon || "object" != typeof b.icon)void 0 !== d.icon && null !== d.icon && "object" == typeof d.icon && (j.setIcon(new v), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message));
                                        else if (void 0 === d.icon || null === d.icon || "object" != typeof d.icon) {
                                            var h=!1;
                                            j.dragging && (h = j.dragging.enabled()), m.AwesomeMarkersPlugin.is(b.icon) ? j.setIcon(b.icon) : m.Leaflet.DivIcon.is(b.icon) || m.Leaflet.Icon.is(b.icon) ? j.setIcon(b.icon) : j.setIcon(new v(b.icon)), h && j.dragging.enable(), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message)
                                        } else if (m.AwesomeMarkersPlugin.is(b.icon)) {
                                            if (!m.AwesomeMarkersPlugin.equal(b.icon, d.icon)) {
                                                var i=!1;
                                                j.dragging && (i = j.dragging.enabled()), j.setIcon(b.icon), i && j.dragging.enable(), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message)
                                            }
                                        } else if (m.Leaflet.DivIcon.is(b.icon)) {
                                            if (!m.Leaflet.DivIcon.equal(b.icon, d.icon)) {
                                                var k=!1;
                                                j.dragging && (k = j.dragging.enabled()), j.setIcon(b.icon), k && j.dragging.enable(), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message)
                                            }
                                        } else if (m.Leaflet.Icon.is(b.icon)) {
                                            if (!m.Leaflet.Icon.equal(b.icon, d.icon)) {
                                                var l=!1;
                                                j.dragging && (l = j.dragging.enabled()), j.setIcon(b.icon), l && j.dragging.enable(), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message)
                                            }
                                        } else if (JSON.stringify(b.icon) !== JSON.stringify(d.icon)) {
                                            var r=!1;
                                            j.dragging && (r = j.dragging.enabled()), j.setIcon(new v(b.icon)), r && j.dragging.enable(), j.closePopup(), j.unbindPopup(), void 0 !== b.message && null !== b.message && "string" == typeof b.message && "" !== b.message && j.bindPopup(b.message)
                                        }
                                        if (void 0 === b.message || null === b.message || "string" != typeof b.message || "" === b.message ? void 0 !== d.message && null !== d.message && "string" == typeof d.message && "" !== d.message && (j.closePopup()
                                            , j.unbindPopup()) : void 0 === d.message || null === d.message || "string" != typeof d.message || "" === d.message ? (j.bindPopup(b.message), b.focus===!0 && j.openPopup()) : b.message !== d.message && j.setPopupContent(b.message), void 0 === b.focus || null === b.focus || b.focus!==!0 ? void 0 !== d.focus && null !== d.focus && d.focus===!0 && j.closePopup() : void 0 === d.focus || null === d.focus || d.focus!==!0 ? j.openPopup() : d.focus===!0 && b.focus===!0 && j.openPopup(), q(b.lat) && q(b.lng)) {
                                            var s = j.getLatLng();
                                            if (s.lat !== b.lat || s.lng !== b.lng) {
                                                var t=!1;
                                                p(b.layer) && m.MarkerClusterPlugin.is(c.overlays[b.layer]) && (c.overlays[b.layer].removeLayer(j), t=!0), j.setLatLng([b.lat, b.lng]), t && c.overlays[b.layer].addLayer(j)
                                            }
                                        } else {
                                            if (a.warn("There are problems with lat-lng data, please verify your marker model"), o(c) && o(c.overlays)
                                                )for (var u in c.overlays)(c.overlays[u]instanceof L.LayerGroup || m.MarkerClusterPlugin.is(c.overlays[u])
                                                ) && c.overlays[u].hasLayer(j) && c.overlays[u].removeLayer(j);
                                            g.removeLayer(j)
                                        }
                                    }
                                }, !0);
                                return j
                            }
                            function h(a) {
                                var b = null;
                                b = a.icon ? a.icon : new v;
                                var c = {
                                    icon: b,
                                    draggable: a.draggable?!0: !1,
                                    clickable: n(a.clickable) ? a.clickable: !0,
                                    riseOnHover: n(a.riseOnHover) ? a.riseOnHover: !1
                                };
                                a.title && (c.title = a.title);
                                var d = new L.marker(a, c);
                                return a.message && d.bindPopup(a.message), e.LabelPlugin.isLoaded() && n(a.label) && n(a.label.message) && d.bindLabel(a.label.message, a.label.options), d
                            }
                            d.setMarkers(i, j.id), s.$watch("markers", function(a) {
                                for (var b in i)
                                    if (!n(a) ||!n(a[b])) {
                                        if (i[b].closePopup(), o(c) && n(c.overlays)
                                            )for (var d in c.overlays)
                                                c.overlays[d]instanceof L.LayerGroup && c.overlays[d].hasLayer(i[b]) && c.overlays[d].removeLayer(i[b]);
                                                if (o(l))
                                                    for (var e in l)
                                                        l[e].hasLayer(i[b]) && l[e].removeLayer(i[b]);
                                                        g.removeLayer(i[b]), delete i[b]
                                    }
                                for (var h in a)
                                    if (!n(i[h])) {
                                        var j = f("markers." + h, a[h], g);
                                        null !== j && (i[h] = j)
                                    }
                            }, !0)
                        })
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("paths", ["$log", "leafletData", "leafletMapDefaults", "leafletHelpers", function(a, b, c, d) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(a, e, f, g) {
                var h = d.isDefined, i = g.getLeafletScope(), j = i.paths, k = d.convertToLeafletLatLng, l = d.convertToLeafletLatLngs, m = d.convertToLeafletMultiLatLngs;
                g.getMap().then(function(d) {
                    c.getDefaults(f.id).then(function(c) {
                        function e(b, c, d, e) {
                            function f(a) {
                                if (h(a.latlngs))
                                    switch (a.type) {
                                    default:
                                    case"polyline":
                                    case"polygon":
                                        g.setLatLngs(l(a.latlngs));
                                        break;
                                    case"multiPolyline":
                                    case"multiPolygon":
                                        g.setLatLngs(m(a.latlngs));
                                        break;
                                    case"rectangle":
                                        g.setBounds(new L.LatLngBounds(l(a.latlngs)));
                                        break;
                                    case"circle":
                                    case"circleMarker":
                                        g.setLatLng(k(a.latlngs)), h(a.radius) && g.setRadius(a.radius)
                                    }
                                h(a.weight) && g.setStyle({
                                    weight: a.weight
                                }), h(a.color) && g.setStyle({
                                    color: a.color
                                }), h(a.opacity) && g.setStyle({
                                    opacity: a.opacity
                                })
                            }
                            var g, i = {
                                weight: e.path.weight,
                                color: e.path.color,
                                opacity: e.path.opacity
                            };
                            switch (h(c.stroke) && (i.stroke = c.stroke), h(c.fill) && (i.fill = c.fill),
                            h(c.fillColor) && (i.fillColor = c.fillColor),
                            h(c.fillOpacity) && (i.fillOpacity = c.fillOpacity),
                            h(c.smoothFactor) && (i.smoothFactor = c.smoothFactor),
                            h(c.noClip) && (i.noClip = c.noClip),
                            h(c.type) || (c.type = "polyline"),
                            c.type) {
                            default:
                            case"polyline":
                                g = new L.Polyline([], i);
                                break;
                            case"multiPolyline":
                                g = new L.multiPolyline([[[0, 0], [1, 1]]], i);
                                break;
                            case"polygon":
                                g = new L.Polygon([], i);
                                break;
                            case"multiPolygon":
                                g = new L.MultiPolygon([[[0, 0], [1, 1], [0, 1]]], i);
                                break;
                            case"rectangle":
                                g = new L.Rectangle([[0, 0], [1, 1]], i);
                                break;
                            case"circle":
                                g = new L.Circle([0, 0], 1, i);
                                break;
                            case"circleMarker":
                                g = new L.CircleMarker([0, 0], i)
                            }
                            d.addLayer(g);
                            var j = a.$watch("paths." + b, function(a) {
                                return h(a) ? (f(a), void 0) : (d.removeLayer(g), j(), void 0)
                            }, !0);
                            return g
                        }
                        if (h(j)) {
                            var g = {};
                            b.setPaths(g, f.id), a.$watch("paths", function(a) {
                                for (var b in a)
                                    h(g[b]) || (g[b] = e(b, a[b], d, c));
                                for (var f in g)
                                    h(a[f]) || delete g[f]
                            }, !0)
                        }
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("controls", ["$log", "leafletHelpers", function(a, b) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(a, c, d, e) {
                var f = b.isDefined, g = e.getLeafletScope(), h = g.controls;
                e.getMap().then(function(a) {
                    if (f(L.Control.Draw) && f(h.draw)) {
                        var b = new L.Control.Draw(h.draw.options);
                        a.addControl(b)
                    }
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("eventBroadcast", ["$log", "$rootScope", "leafletHelpers", "leafletEvents", function(a, b, c, d) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(b, e, f, g) {
                var h = (c.safeApply, c.isDefinedAndNotNull, c.isDefined, c.isObject), i = g.getLeafletScope(), j = i.eventBroadcast, k = d.getAvailableMapEvents(), l = d.genDispatchMapEvent;
                g.getMap().then(function(b) {
                    var c, d, e = [], f = "broadcast";
                    if (h(j)) {
                        if (void 0 === j.map || null === j.map)
                            e = k;
                        else if ("object" != typeof j.map)
                            a.warn("[AngularJS - Leaflet] event-broadcast.map must be an object check your model.");
                        else {
                            void 0 !== j.map.logic && null !== j.map.logic && ("emit" !== j.map.logic && "broadcast" !== j.map.logic ? a.warn("[AngularJS - Leaflet] Available event propagation logic are: 'emit' or 'broadcast'.") : "emit" === j.map.logic && (f = "emit"));
                            var g=!1, m=!1;
                            if (void 0 !== j.map.enable && null !== j.map.enable && "object" == typeof j.map.enable && (g=!0)
                                , void 0 !== j.map.disable && null !== j.map.disable && "object" == typeof j.map.disable && (m=!0), g && m)a.warn("[AngularJS - Leaflet] can not enable and disable events at the time");
                            else if (g || m)
                                if (g)
                                    for (c = 0; c < j.map.enable.length; c++)
                                        d = j.map.enable[c], -1 !== e.indexOf(d) ? a.warn("[AngularJS - Leaflet] This event " + d + " is already enabled") : -1 === k.indexOf(d) ? a.warn("[AngularJS - Leaflet] This event " + d + " does not exist") : e.push(d);
                                else
                                    for (e = k, c = 0; c < j.map.disable.length; c++) {
                                        d = j.map.disable[c];
                                        var n = e.indexOf(d);
                                        -1 === n ? a.warn("[AngularJS - Leaflet] This event " + d + " does not exist or has been already disabled") : e.splice(n, 1)
                                    } else
                                        a.warn("[AngularJS - Leaflet] must enable or disable events")
                                    }
                        for (c = 0; c < e.length; c++)
                            d = e[c], b.on(d, l(i, d, f), {
                            eventName: d
                        })
                    } else
                        a.warn("[AngularJS - Leaflet] event-broadcast must be an object, check your model.")
                        })
            }
        }
    }
    ]), angular.module("leaflet-directive").directive("maxbounds", ["$log", "leafletMapDefaults", "leafletHelpers", function(a, b, c) {
        return {
            restrict: "A",
            scope: !1,
            replace: !1,
            require: "leaflet",
            link: function(a, b, d, e) {
                {
                    var f = c.isDefined, g = c.isNumber, h = e.getLeafletScope();
                    h.maxBounds
                }
                e.getMap().then(function(a) {
                    function b(a) {
                        return f(a.southWest) && f(a.northEast) && g(a.southWest.lat) && g(a.southWest.lng) && g(a.northEast.lat) && g(a.northEast.lng)
                    }
                    h.$watch("maxBounds", function(c) {
                        return b(c) ? (a.setMaxBounds(new L.LatLngBounds(new L.LatLng(c.southWest.lat, c.southWest.lng), new L.LatLng(c.northEast.lat, c.northEast.lng)), c.options), void 0) : (a.setMaxBounds(), void 0)
                    })
                })
            }
        }
    }
    ]), angular.module("leaflet-directive").service("leafletData", ["$log", "$q", "leafletHelpers", function(a, b, c) {
        var d = (c.isDefined, c.getDefer), e = c.getUnresolvedDefer, f = c.setResolvedDefer, g = {}, h = {}, i = {}, j = {}, k = {}, l = {};
        this.setMap = function(a, b) {
            var c = e(g, b);
            c.resolve(a), f(g, b)
        }, this.getMap = function(a) {
            var b = d(g, a);
            return b.promise
        }, this.getPaths = function(a) {
            var b = d(j, a);
            return b.promise
        }, this.setPaths = function(a, b) {
            var c = e(j, b);
            c.resolve(a), f(j, b)
        }, this.getMarkers = function(a) {
            var b = d(k, a);
            return b.promise
        }, this.setMarkers = function(a, b) {
            var c = e(k, b);
            c.resolve(a), f(k, b)
        }, this.getLayers = function(a) {
            var b = d(i, a);
            return b.promise
        }, this.setLayers = function(a, b) {
            var c = e(i, b);
            c.resolve(a), f(i, b)
        }, this.setTiles = function(a, b) {
            var c = e(h, b);
            c.resolve(a), f(h, b)
        }, this.getTiles = function(a) {
            var b = d(h, a);
            return b.promise
        }, this.setGeoJSON = function(a, b) {
            var c = e(l, b);
            c.resolve(a), f(l, b)
        }, this.getGeoJSON = function(a) {
            var b = d(l, a);
            return b.promise
        }
    }
    ]), angular.module("leaflet-directive").factory("leafletMapDefaults", ["$q", "leafletHelpers", function(a, b) {
        function c() {
            return {
                keyboard: !0,
                dragging: !0,
                doubleClickZoom: !0,
                scrollWheelZoom: !0,
                zoomControl: !0,
                attributionControl: !0,
                zoomsliderControl: !1,
                zoomControlPosition: "topleft",
                controlLayersPosition: "topright",
                crs: L.CRS.EPSG3857,
                tileLayer: "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                tileLayerOptions: {
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                },
                icon: {
                    url: "http://cdn.leafletjs.com/leaflet-0.6.4/images/marker-icon.png",
                    retinaUrl: "http://cdn.leafletjs.com/leaflet-0.6.4/images/marker-icon-2x.png",
                    size: [25, 41],
                    anchor: [12, 40],
                    labelAnchor: [10, -20],
                    popup: [0, -40],
                    shadow: {
                        url: "http://cdn.leafletjs.com/leaflet-0.6.4/images/marker-shadow.png",
                        retinaUrl: "http://cdn.leafletjs.com/leaflet-0.6.4/images/marker-shadow.png",
                        size: [41, 41],
                        anchor: [12, 40]
                    }
                },
                path: {
                    weight: 10,
                    opacity: 1,
                    color: "#0000ff"
                },
                center: {
                    lat: 0,
                    lng: 0,
                    zoom: 1
                }
            }
        }
        var d = b.isDefined, e = b.getDefer, f = b.getUnresolvedDefer, g = {};
        return {
            getDefaults: function(a) {
                var b = e(g, a);
                return b.promise
            },
            setDefaults: function(a, b) {
                var e = c();
                d(a) && (e.doubleClickZoom = d(a.doubleClickZoom) ? a.doubleClickZoom : e.doubleClickZoom, e.scrollWheelZoom = d(a.scrollWheelZoom) ? a.scrollWheelZoom : e.doubleClickZoom, e.zoomControl = d(a.zoomControl) ? a.zoomControl : e.zoomControl, e.attributionControl = d(a.attributionControl) ? a.attributionControl : e.attributionControl, e.tileLayer = d(a.tileLayer) ? a.tileLayer : e.tileLayer, e.zoomControlPosition = d(a.zoomControlPosition) ? a.zoomControlPosition : e.zoomControlPosition, e.keyboard = d(a.keyboard) ? a.keyboard : e.keyboard, e.dragging = d(a.dragging) ? a.dragging : e.dragging, e.controlLayersPosition = d(a.controlLayersPosition) ? a.controlLayersPosition : e.controlLayersPosition, d(a.crs) && d(L.CRS[a.crs]) && (e.crs = L.CRS[a.crs]), d(a.tileLayerOptions) && angular.copy(a.tileLayerOptions, e.tileLayerOptions), d(a.maxZoom) && (e.maxZoom = a.maxZoom), d(a.minZoom) && (e.minZoom = a.minZoom));
                var h = f(g, b);
                return h.resolve(e), e
            }
        }
    }
    ]), angular.module("leaflet-directive").factory("leafletEvents", ["$rootScope", "$q", "leafletHelpers", function(a, b, c) {
        var d = c.safeApply;
        return {
            getAvailableMapEvents: function() {
                return ["click", "dblclick", "mousedown", "mouseup", "mouseover", "mouseout", "mousemove", "contextmenu", "focus", "blur", "preclick", "load", "unload", "viewreset", "movestart", "move", "moveend", "dragstart", "drag", "dragend", "zoomstart", "zoomend", "zoomlevelschange", "resize", "autopanstart", "layeradd", "layerremove", "baselayerchange", "overlayadd", "overlayremove", "locationfound", "locationerror", "popupopen", "popupclose"]
            },
            genDispatchMapEvent: function(b, c, e) {
                return function(f) {
                    var g = "leafletDirectiveMap." + c;
                    d(b, function(b) {
                        "emit" === e ? b.$emit(g, {
                            leafletEvent: f
                        }) : "broadcast" === e && a.$broadcast(g, {
                            leafletEvent: f
                        })
                    })
                }
            },
            getAvailableMarkerEvents: function() {
                return ["click", "dblclick", "mousedown", "mouseover", "mouseout", "contextmenu", "dragstart", "drag", "dragend", "move", "remove", "popupopen", "popupclose"]
            },
            genDispatchMarkerEvent: function(b, c, e, f) {
                return function(g) {
                    var h = "leafletDirectiveMarker." + c;
                    d(b, function(b) {
                        "emit" === e ? b.$emit(h, {
                            leafletEvent: g,
                            markerName: f
                        }) : "broadcast" === e && a.$broadcast(h, {
                            leafletEvent: g,
                            markerName: f
                        })
                    })
                }
            }
        }
    }
    ]), angular.module("leaflet-directive").factory("leafletHelpers", ["$q", "$log", function(a, b) {
        function c(a, c) {
            var d, e;
            if (angular.isDefined(c))
                d = c;
            else if (1 === Object.keys(a).length)
                for (e in a)
                    a.hasOwnProperty(e) && (d = e);
            else
                0 === Object.keys(a).length ? d = "main" : b.error("[AngularJS - Leaflet] - You have more than 1 map on the DOM, you must provide the map ID to the leafletData.getXXX call");
            return d
        }
        function d(b, d) {
            var e, f = c(b, d);
            return angular.isDefined(b[f]) && b[f].resolvedDefer!==!0 ? e = b[f].defer : (e = a.defer(), b[f] = {
                defer : e, resolvedDefer : !1
            }), e
        }
        function e(a) {
            return a.filter(function(a) {
                return !!a.lat&&!!a.lng
            }).map(function(a) {
                return new L.LatLng(a.lat, a.lng)
            })
        }
        return {
            isDefined: function(a) {
                return angular.isDefined(a)
            },
            isNumber: function(a) {
                return angular.isNumber(a)
            },
            isDefinedAndNotNull: function(a) {
                return angular.isDefined(a) && null !== a
            },
            isString: function(a) {
                return angular.isString(a)
            },
            isArray: function(a) {
                return angular.isArray(a)
            },
            isObject: function(a) {
                return angular.isObject(a)
            },
            equals: function(a, b) {
                return angular.equals(a, b)
            },
            isValidCenter: function(a) {
                return angular.isDefined(a) && angular.isNumber(a.lat) && angular.isNumber(a.lng) && angular.isNumber(a.zoom)
            },
            createLeafletBounds: function(a) {
                return angular.isDefined(a) && angular.isDefined(a.southWest) && angular.isDefined(a.northEast) && angular.isNumber(a.southWest.lat) && angular.isNumber(a.southWest.lng) && angular.isNumber(a.northEast.lat) && angular.isNumber(a.northEast.lng) ? L.latLngBounds([a.southWest.lat, a.southWest.lng], [a.northEast.lat, a.northEast.lng]) : !1
            },
            convertToLeafletLatLngs: e,
            convertToLeafletLatLng: function(a) {
                return new L.LatLng(a.lat, a.lng)
            },
            convertToLeafletMultiLatLngs: function(a) {
                return a.map(function(a) {
                    return e(a)
                })
            },
            safeApply: function(a, b) {
                var c = a.$root.$$phase;
                "$apply" === c || "$digest" === c ? a.$eval(b) : a.$apply(b)
            },
            obtainEffectiveMapId: c,
            getDefer: function(a, b) {
                var e, f = c(a, b);
                return e = angular.isDefined(a[f]) && a[f].resolvedDefer!==!1 ? a[f].defer : d(a, b)
            },
            getUnresolvedDefer: d,
            setResolvedDefer: function(a, b) {
                var d = c(a, b);
                a[d].resolvedDefer=!0
            },
            AwesomeMarkersPlugin: {
                isLoaded: function() {
                    return void 0 !== L.AwesomeMarkers ? void 0 !== L.AwesomeMarkers.Icon : !1
                },
                is: function(a) {
                    return this.isLoaded() ? a instanceof L.AwesomeMarkers.Icon : !1
                },
                equal: function(a, b) {
                    return this.isLoaded() ? this.is(a) ? angular.equals(a, b) : !1 : !1
                }
            },
            LabelPlugin: {
                isLoaded: function() {
                    return angular.isDefined(L.Label)
                },
                is: function(a) {
                    return this.isLoaded() ? a instanceof L.MarkerClusterGroup : !1
                }
            },
            MarkerClusterPlugin: {
                isLoaded: function() {
                    return angular.isDefined(L.MarkerClusterGroup)
                },
                is: function(a) {
                    return this.isLoaded() ? a instanceof L.MarkerClusterGroup : !1
                }
            },
            GoogleLayerPlugin: {
                isLoaded: function() {
                    return angular.isDefined(L.Google)
                },
                is: function(a) {
                    return this.isLoaded() ? a instanceof L.Google : !1
                }
            },
            BingLayerPlugin: {
                isLoaded: function() {
                    return angular.isDefined(L.BingLayer)
                },
                is: function(a) {
                    return this.isLoaded() ? a instanceof L.BingLayer : !1
                }
            },
            Leaflet: {
                DivIcon: {
                    is: function(a) {
                        return a instanceof L.DivIcon
                    },
                    equal: function(a, b) {
                        return this.is(a) ? angular.equals(a, b) : !1
                    }
                },
                Icon: {
                    is: function(a) {
                        return a instanceof L.Icon
                    },
                    equal: function(a, b) {
                        return this.is(a) ? angular.equals(a, b) : !1
                    }
                }
            }
        }
    }
    ])
}();
