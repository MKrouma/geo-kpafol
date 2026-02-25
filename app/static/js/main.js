var map = L.map('map').setView([6.68047763, -4.1245604], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

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

    // Fit map to AOI if possible
    const bounds = aoiLayer.getBounds();
    if (bounds.isValid && !bounds.isEmpty()) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  })
  .catch(err => console.error('Failed to load AOI:', err));

