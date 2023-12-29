var data = document.getElementById("data").value;
data = data.replaceAll("'", '"');
data = JSON.parse(data);

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchBTN').disabled = false;
    try {
        document.getElementsByClassName('fav')[0].style.marginLeft = (document.getElementById('infocard').offsetWidth - 55).toString() + 'px';
    }
    catch{}
})

function fav() {
    document.querySelector('.fav').classList.toggle('is-active');
    const id = JSON.parse(document.getElementById('data').value.replaceAll("'", '"')).id;
    fetch('/fav', {
        method: 'PUT',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            "id": id
        })
    })
    .catch(error => {
		console.log(error);
	})
}

mapboxgl.accessToken = 'pk.eyJ1IjoiYW5kcmVzZ2FyYmFyeiIsImEiOiJja3l5eHptdWswNWhiMm9xamhxdmV5Njh4In0.FDvtKIpQntLENs8hKeHWEQ';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11?optimize=true',
    center: [data.coord.lon, data.coord.lat],
    zoom: 4
});

const marker = new mapboxgl.Marker({"color": "red"})
    .setLngLat([data.coord.lon, data.coord.lat])
    .setPopup(new mapboxgl.Popup({ offset: 25 })
        .setHTML(`<h5>${data.name}</h5><p>Click <span style="filter: grayscale(100%);">&#11088;</span> to add it to favorites</p>`)
    ).addTo(map);

map.addControl(new mapboxgl.NavigationControl());

function info(expand) {
    const summary = document.getElementById('summary').value;
    const info = document.getElementById('info').value;
    if (expand) {
        document.getElementById('infop').innerHTML = `${info} <a href="" onclick="{event.preventDefault(); info(false);}">[-]</a>`
        document.getElementById('infocard').style.height = (document.getElementById('infop').offsetHeight + 60).toString() + 'px';
    }
    else {
        document.getElementById('infop').innerHTML = `${summary} <a href="" onclick="{event.preventDefault(); info(true);}">[+]</a>`
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}