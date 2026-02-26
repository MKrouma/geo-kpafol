var map = L.map('map').setView([6.68047763, -4.1245604], 8);

// Base layers
var OpenStreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var Esri_WorldImagery = L.tileLayer(
  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  {
    attribution:
      'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  }
);


// AOI layer from backend
fetch('/api/aoi')
  .then(res => {
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    return res.json();
  })
  .then(geojson => {
    const aoiLayer = L.geoJSON(geojson, {
      style: {
        color: '#335CFF',
        weight: 2,
        fillOpacity: 0.08
      },
      onEachFeature: function(feature, layer) {
        if (feature.properties && Object.keys(feature.properties).length) {
          const html = Object.entries(feature.properties)
            .map(([k, v]) => `<strong>${k}</strong>: ${v}`)
            .join('<br>');
          layer.bindPopup(html);
        }
      }
    }).addTo(map);

    // Simple layer control with base maps and AOI overlay
    const baseMaps = {
      'OpenStreetMap': OpenStreetMap,
      'Esri World Imagery': Esri_WorldImagery
    };

    const overlayMaps = {
      'AOI': aoiLayer
    };

    L.control.layers(baseMaps, overlayMaps).addTo(map);

    // Fit map to AOI if possible
    const bounds = aoiLayer.getBounds();
    if (bounds.isValid && !bounds.isEmpty()) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  })
  .catch(err => console.error('Failed to load AOI:', err));

