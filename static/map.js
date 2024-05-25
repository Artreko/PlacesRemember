let latitude = document.getElementById("id_latitude")
    let longitude = document.getElementById("id_longitude")
    let map = L.map('map').setView([56.010548, 92.852571], 3)
    let marker = L.marker()
    if (latitude.value && longitude.value) {
        let latlng = L.latlng(latitude.value, longitude.value)
        map.setView(latlng, 15)
        marker.setLatLng(latlng).addTo(map)
    }
    
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)

    function onMapClick(e) {
        let latlng = e.latlng
        marker
            .setLatLng(latlng)
            .addTo(map)
        latitude.value = e.latlng.lat
        longitude.value = e.latlng.lng
    }

    map.on('click', onMapClick)