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
      'Tiles &copy; Esri &mdash; Source: Esri & Co.'
  }
) 
// .addTo(map);


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
      'EsriImagery': Esri_WorldImagery,
      'OpenStreetMap': OpenStreetMap,
    };

    const overlayMaps = {
      'Zone d\'étude': aoiLayer
    };

    // keep a reference so other fetches can add overlays later
    window._layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);

    // Fit map to AOI if possible
    const bounds = aoiLayer.getBounds();
    if (bounds.isValid && !bounds.isEmpty()) {
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  })
  .catch(err => console.error('Failed to load AOI:', err));

// Alerts layer from backend (styled with color #F97316)
fetch('/api/alerts')
  .then(res => {
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    return res.json();
  })
  .then(geojson => {
    // helpers to derive style from risk category
    function getRiskCategory(props) {
      const raw = (props && props.risk != null ? String(props.risk) : '').toLowerCase();
      if (raw === 'high') return 'high';
      if (raw === 'low') return 'low';
      return 'unknown';
    }

    function styleForRisk(riskCategory) {
      if (riskCategory === 'high') {
        // High risk -> brand orange
        return {
          color: '#C2410C',   // darker orange border
          fillColor: '#F97316'
        };
      }
      if (riskCategory === 'low') {
        // Low risk -> brand blue, softer fill
        return {
          color: '#64748B',   // main app blue
          fillColor: '#CBD5F5' // light blue fill
        };
      }
      // Fallback neutral style
      return {
        color: '#64748B',
        fillColor: '#CBD5F5'
      };
    }

    // helper to compute style for vector features (polygons/lines)
    function styleForFeature(feature) {
      const props = feature.properties || {};
      const riskCategory = getRiskCategory(props);
      const colors = styleForRisk(riskCategory);
      return {
        color: colors.color,
        fillColor: colors.fillColor,
        weight: 2,
        opacity: 1,
        fillOpacity: 0.25,
        dashArray: null
      };
    }

    const alertsLayer = L.geoJSON(geojson, {
      // points as filled circle markers
      pointToLayer: function(feature, latlng) {
        const props = feature.properties || {};
        const riskCategory = getRiskCategory(props);
        const colors = styleForRisk(riskCategory);
        const prob = Number(props.probabilite || 0);
        const radius = Math.min(12, 4 + Math.round(prob / 20)); // scale by probability if available
        return L.circleMarker(latlng, {
          radius: radius,
          fillColor: colors.fillColor,
          color: colors.color,
          weight: 1.5,
          opacity: 1,
          fillOpacity: 0.95
        });
      },
      // polygons/lines styling (filled)
      style: function(feature) {
        return styleForFeature(feature);
      },
      onEachFeature: function(feature, layer) {
        const props = feature.properties || {};
        const html = Object.entries(props)
          .map(([k, v]) => `<strong>${k}</strong>: ${v}`)
          .join('<br>');
        layer.bindPopup(html || 'Alerte');

        // interactive highlight
        layer.on('mouseover', function() {
          if (layer.setStyle) layer.setStyle({ weight: 3, fillOpacity: 0.45 });
        });
        layer.on('mouseout', function() {
          if (layer.setStyle) layer.setStyle(styleForFeature(feature));
        });
      }
    }).addTo(map);
    
    // add to existing layer control if present
    if (window._layerControl && typeof window._layerControl.addOverlay === 'function') {
      window._layerControl.addOverlay(alertsLayer, 'Alertes');
    } else {
      L.control.layers(null, { 'Alertes': alertsLayer }).addTo(map);
    }
  })
  .catch(err => console.error('Failed to load alerts:', err));

