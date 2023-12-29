var standard, metric, imperial, checked, newunit, saveBTN;

window.addEventListener('DOMContentLoaded', () => {
    saveBTN = document.getElementById('saveBTN');
    saveBTN.style.display = 'none';

    standard = document.getElementById('standard').checked;
    metric = document.getElementById('metric').checked;
    imperial = document.getElementById('imperial').checked;

    if (imperial) {
        checked = "imperial";
    }
    else if (metric) {
        checked = "metric";
    }
    else {
        checked = "standard";
        document.getElementById('standard').checked = true;
    }
});

function newUnit(unit) {
    newunit = unit;
    if (unit != checked) {
        if (saveBTN.style.display === "none") {
            saveBTN.style.display = "inline";
        }
    }
    else {
        if (saveBTN.style.display === "inline") {
            saveBTN.style.display = "none";
        }
    }
}

function saveChanges() {
    fetch('/newunit', {
        method: 'PUT',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            "unit": newunit
        })
    })
    .then(response => {if (response.status == 204) {window.location.reload();}})
    .catch(error => {
		console.log(error);
	})
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