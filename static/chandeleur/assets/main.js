var images_base = "https://s3.avian-data.c-demo.xyz/HighResolutionImages/2018"
var association_summary = "./data/summary.json"
var thumbnails_base = "https://s3.avian-data.c-demo.xyz/HighResolutionImages/2018/thumbnails"
screenshots_base_gen = function (colony){
	var screenshots_base = "https://s3.avian-data.c-demo.xyz/DottedImages/2018%20LA%20Waterbird%20Colony%20Photo%20Analysis"

	if (colony.includes("Chandeleur")){
		return `${screenshots_base}/Group%202%20Deliverables/${colony.replace("Chandeleur","Chandeleur ")}`
	}else if (colony.includes("Harbor")){
		return `${screenshots_base}/Group%201%20Deliverables/New%20Harbor%20Island/${colony.replace("New Harbor Island ","NHI")}`
	}else if (colony.includes("Gosier")){
		return `${screenshots_base}/Group%202%20Deliverables/Gosier%20Islands%20New`
	}
}
var tiles = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 18,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  }),
  latlng = L.latLng(28.69, -87.44);

var map = L.map('map', {
  center: latlng,
  zoom: 5,
  layers: [tiles]
});
var markers = L.markerClusterGroup();
var prev_data = []
var createMarkers = function(addressPoints) {
  markers.clearLayers()
  var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
  points_dict = { };

  for (var i = 0; i < addressPoints.length; i++) {
    var a = addressPoints[i];
    var a_birds = null;
    if (!(a.Screenshot in points_dict))
    {
      points_dict[a.Screenshot] = {
        header: `<div class="popup_div">
                  <h3>${a.LongVersionColonyUID}, area ${a.DottingAreaNumber}, ${a.Date}</h3>
                  <a title='full resolution image' href='${images_base}/${a.Associated}' download>Download full resolution</a><br/>
          <a href='${screenshots_base_gen(a.Colony)}/${a.Screenshot}' target='blank' download><img src='${screenshots_base_gen(a.Colony)}/${a.Screenshot}' title='screenshot' width='100px'/></a>
           <a title='full resolution image' href='${images_base}/${a.Associated}' download><img src='${thumbnails_base}/${a.Associated.replace(".jpg", ".png")}' title='thumbnail' width='100px'/></a>`,
         species: `<thead><tr><th>SpeciesName</th><th>Site</th></tr></thead><tbody>`,
         Latitude: a.Latitude,
         Longitude: a.Longitude,
      }
    }
    points_dict[a.Screenshot].species += `<tr><td><a href='${birds[a.SpeciesName]?.bird_wikipage }'>
    ${a.SpeciesName} <img src='${birds[a.SpeciesName]?.bird_thumbnail}' width='50px'/></a></td><td>${a.Site}</td></tr>`
  }
  for (const [key, value] of Object.entries(points_dict)) {
    console.log(key, value);
   var marker = L.marker(new L.LatLng(value.Latitude, value.Longitude),  { title: key })
   marker.bindPopup(`${value.header}<table>${value.species}</tbody></table>`, {
    maxWidth : 560
});
   markers.addLayer(marker);
  }
  map.addLayer(markers);
  $('#table').dataTable({
    "data": addressPoints,"pageLength": 50,
    scrollX:        true,
        scrollCollapse: true,
        columnDefs: [
            { width: '20%', targets: 0 }
        ],
        fixedColumns: {left:5},
	fixedHeader: true,
    "columns":[
{"data": "Colony", title: "Colony"},
{"data": "Subcolony", title: "Subcolony"},
{"data": "Area", title: "Area"},
{"data":  "SpeciesName","title":  "SpeciesName",},
{"data": "Date", title: "Date"},
{"data": "SpeciesCode", title: "SpeciesCode"},
{"data": "PQ", title: "PQ"},
{"data": "WBN", title: "WBN"},
{"data": "ChickNest", title: "ChickNest"},
{"data": "ChickNestw/outAdult", title: "ChickNestw/outAdult"},
{"data": "Brood", title: "Brood"},
{"data": "AbandNest", title: "AbandNest"},
{"data": "EmptyNest", title: "EmptyNest"},
{"data": "PBN", title: "PBN"},
{"data": "Site", title: "Site"},
{"data": "OtherBirds", title: "OtherBirds"},
{"data": "Dotter", title: "Dotter"},
{"data": "DateDotted", title: "DateDotted"},
//{"data": "BestForBPE?", title: "BestForBPE?"},
{"data": "Notes", title: "Notes"},
{"data": "Associated", title: "Photo"},
{"data": "Latitude", title: "Latitude"},
{"data": "Longitude", title: "Longitude"},
{"data": "Year", title: "Year"},
]
  }
  )
}
load_all = function() {
  fetch(association_summary, {
      headers: {
        'Accept': 'application/json'
      }

    })
    .then(response => response.json())
    .then(data => {
      createMarkers(data);
    })
}

load_all()
