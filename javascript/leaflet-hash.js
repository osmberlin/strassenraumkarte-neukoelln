(function(window) {
	var HAS_HASHCHANGE = (function() {
		var doc_mode = window.documentMode;
		return ('onhashchange' in window) &&
			(doc_mode === undefined || doc_mode > 7);
	})();

	L.Hash = function(map, layers) {
		this.onHashChange = L.Util.bind(this.onHashChange, this);

		if (map && layers) {
			this.init(map, layers);
		}
	};

	L.Hash.parseHash = function(hash) {
		if(hash.indexOf('#') === 0) {
			hash = hash.substr(1);
		}
		var args = hash.split("/");
		if (args.length == 4) {
			var zoom = parseInt(args[0], 10),
			lat = parseFloat(args[1]),
			lon = parseFloat(args[2]),
			layer = args[3];
			if (isNaN(zoom) || isNaN(lat) || isNaN(lon)) {
				return false;
			} else {
				return {
					center: new L.LatLng(lat, lon),
					zoom: zoom,
					layer: layer
				};
			}
		} else {
			return false;
		}
	};

	L.Hash.formatHash = function(zoom, lat, lng, layer_name) {
		return "#" + [zoom, lat, lng, layer_name].join("/");
	},

	L.Hash.prototype = {
		map: null,
		layers: null,
		lastHash: null,

		parseHash: L.Hash.parseHash,
		formatHash: L.Hash.formatHash,

		init: function(map, layers) {
			this.map = map;
			this.layers = layers;

			// reset the hash
			this.lastHash = null;
			this.onHashChange();

			if (!this.isListening) {
				this.startListening();
			}
		},

		removeFrom: function(map) {
			if (this.changeTimeout) {
				clearTimeout(this.changeTimeout);
			}

			if (this.isListening) {
				this.stopListening();
			}

			this.map = null;
		},

		onMapMoveOrLayerChange: function(event) {
			// bail if we're moving the map (updating from a hash),
			// or if the map is not yet loaded

			if (this.movingMap || !this.map._loaded || event === undefined) {
				return false;
			}

			var center = map.getCenter(),
				zoom = map.getZoom(),
				precision = Math.max(0, Math.ceil(Math.log(zoom) / Math.LN2)),
				lat = center.lat.toFixed(precision),
				lng = center.lng.toFixed(precision),
				layer_name = '';

			if (event.type === "baselayerchange") {
				layer_name = event.layer.options.name
			} else {
				// event.type==moveend: when just moving, take the currently active layer
				// todo: in my case map._layers has only one entry. But this is probably false
				//   in cases that use overlays. So this will likele need another check to select the baselayer
				// TODO: this would be more elegant if we checked with map.hasLayer if a given layer from this.layers
				//   exists; but we first need to find a way to select this layer by the name in the hash.
				this.map.eachLayer(function (layer) { layer_name = layer.options.name })
			}

			var hash = this.formatHash(zoom, lat, lng, layer_name);
			if (this.lastHash != hash) {
				location.replace(hash);
				this.lastHash = hash;
			}
		},

		movingMap: false,
		update: function() {
			var hash = location.hash;
			if (hash === this.lastHash) {
				return;
			}
			var parsed = this.parseHash(hash);
			if (parsed) {
				this.movingMap = true;

				this.map.setView(parsed.center, parsed.zoom);

				Object.keys(this.layers).map(layer_key => {
					var layer = this.layers[layer_key]
					if (layer.options.name === parsed.layer) {
						this.map.addLayer(layer)
					}
				})

				this.movingMap = false;
			} else {
				this.onMapMoveOrLayerChange();
			}
		},

		// defer hash change updates every 100ms
		changeDefer: 100,
		changeTimeout: null,
		onHashChange: function() {
			// throttle calls to update() so that they only happen every
			// `changeDefer` ms
			if (!this.changeTimeout) {
				var that = this;
				this.changeTimeout = setTimeout(function() {
					that.update();
					that.changeTimeout = null;
				}, this.changeDefer);
			}
		},

		isListening: false,
		hashChangeInterval: null,
		startListening: function() {
			this.map.on("moveend baselayerchange", this.onMapMoveOrLayerChange, this);

			if (HAS_HASHCHANGE) {
				L.DomEvent.addListener(window, "hashchange", this.onHashChange);
			} else {
				clearInterval(this.hashChangeInterval);
				this.hashChangeInterval = setInterval(this.onHashChange, 50);
			}
			this.isListening = true;
		},

		stopListening: function() {
			this.map.off("moveend baselayerchange", this.onMapMoveOrLayerChange, this);

			if (HAS_HASHCHANGE) {
				L.DomEvent.removeListener(window, "hashchange", this.onHashChange);
			} else {
				clearInterval(this.hashChangeInterval);
			}
			this.isListening = false;
		}
	};
	L.hash = function(map) {
		return new L.Hash(map);
	};
	L.Map.prototype.addHash = function() {
		this._hash = L.hash(this);
	};
	L.Map.prototype.removeHash = function() {
		this._hash.removeFrom();
	};
})(window);
