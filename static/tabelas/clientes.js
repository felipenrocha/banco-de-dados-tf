$(document).ready(function() {
    $('.modal').modal();
    $('.dropdown-trigger').dropdown();
    $('.datepicker').datepicker();
    $('select').formSelect();
    mapboxgl.accessToken = 'pk.eyJ1IjoiZmVsaXBlbnJvY2hhIiwiYSI6ImNqcmdqMGF1MTFvM3ozeWxweDNicDU5eWUifQ.3RTgEndlcpmgIvCjguuY7A';
    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-47.92778, -15.793889], // starting position [lng, lat]
        zoom: 11 // starting zoom
    });
    map.on('load', function() {
        map.resize();
    });
    var geolocate = new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        trackUserLocation: true
    });
    let el = document.createElement('div');
    el.className = 'marker';

    var marker = new mapboxgl.Marker(el)
    map.addControl(geolocate);
    map.on('load', function() {
        geolocate.trigger();
    });
    map.on('click', function(data) {
        $("#posicao_origem_latitude").val(data.lngLat.lat)
        $("#posicao_origem_longitude").val(data.lngLat.lng)


        console.log(data.lngLat);
        var marker = new mapboxgl.Marker(el)
            .setLngLat(data.lngLat)
            .addTo(map);
    });




    var map2 = new mapboxgl.Map({
        container: 'map2', // container id
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-47.92778, -15.793889], // starting position [lng, lat]
        zoom: 11 // starting zoom
    });
    map2.on('load', function() {
        map2.resize();
    });
    var geolocate = new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        trackUserLocation: true
    });
    let el2 = document.createElement('div');
    el2.className = 'marker2';

    var marker2 = new mapboxgl.Marker(el2)
    map2.on('click', function(data) {
        $("#posicao_destino_latitude").val(data.lngLat.lat)
        $("#posicao_destino_longitude").val(data.lngLat.lng)


        console.log(data.lngLat);
        var marker2 = new mapboxgl.Marker(el)
            .setLngLat(data.lngLat)
            .addTo(map2);
    });




});