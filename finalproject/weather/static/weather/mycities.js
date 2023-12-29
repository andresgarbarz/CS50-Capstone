mapboxgl.accessToken = 'pk.eyJ1IjoiYW5kcmVzZ2FyYmFyeiIsImEiOiJja3l5eHptdWswNWhiMm9xamhxdmV5Njh4In0.FDvtKIpQntLENs8hKeHWEQ';
var map = new mapboxgl.Map({
    container: 'bigmap',
    style: 'mapbox://styles/mapbox/streets-v11?optimize=true',
    zoom: 1
});

map.addControl(new mapboxgl.NavigationControl());

window.addEventListener('DOMContentLoaded', () => {
    var cities = JSON.parse(document.getElementById('cities').value.replaceAll("'", '"'))
    cities.forEach(city => {
        addCity(city);
    });
});

function addCity(city) {
    const color = "hsl(" + (Math.random() * 360) + ", 100%, 50%)";
    document.getElementById(city.id).style.backgroundColor = color;
    const marker = new mapboxgl.Marker({"color": color})
    .setLngLat([city.lon, city.lat])
    .setPopup(new mapboxgl.Popup({ offset: 25 })
        .setHTML(`<h5>${city.name}</h5><a href="" onclick="{event.preventDefault(); searchcity('${city.name.replaceAll(" ", "+")}', '${city.country.replaceAll(" ", "+")}');}">Info</a>`)
    ).addTo(map);
}

function searchcity(name, country) {
    location.href = '/search?q=' + name + '%2C+' + country;
}