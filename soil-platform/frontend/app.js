const map = L.map('map').setView([39.9, 116.4], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let sensorLayer = null;

function loadGeoJSON(url) {
  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (sensorLayer) map.removeLayer(sensorLayer);
      sensorLayer = L.geoJSON(data, {
        pointToLayer: (feature, latlng) => {
          const pH = feature.properties.ph;
          let color = "#ff5722";
          if (pH < 6) color = "red";
          else if (pH > 7) color = "green";

          return L.circleMarker(latlng, {
            radius: 6,
            fillColor: color,
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          });
        },
        onEachFeature: (feature, layer) => {
          const pH = feature.properties.ph;
          layer.bindPopup(`pH 值：<b>${pH}</b>`);
        }
      }).addTo(map);

      map.fitBounds(sensorLayer.getBounds());
    });
}

function uploadData() {
  const file = document.getElementById("file-input").files[0];
  if (!file) return alert("select CSV file");
  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      if (data.status !== "success") {
        alert("上传失败：" + data.status);
        return;
      }
      alert("上传成功！");
      loadGeoJSON(data.geojson);
    })
    .catch(err => alert("上传失败：" + err.message));
}
