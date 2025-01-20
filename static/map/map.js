 document.querySelectorAll('.pharmacy').forEach(function(element) {
    element.addEventListener('click', function() {
        var lat = this.getAttribute('lat');
        var lng = this.getAttribute('lng');
        var moveLatLon = new kakao.maps.LatLng(lng, lat);
        map.setCenter(moveLatLon);
    });
});