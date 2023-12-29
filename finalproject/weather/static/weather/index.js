window.addEventListener('DOMContentLoaded', () => {
    try {
        document.querySelector('.loader').remove();
        document.querySelector('.loadingTXT').remove();
    }
    catch {}
});

function addLoading() {
    const msg = document.getElementById('message');
    try {
        msg.remove();
    }
    catch {}
    const loader = document.querySelector('.loader');
    const loadingTXT = document.querySelector('.loadingTXT');
    if (loader == null) {
        if (window.location.pathname != '/search' && window.location.pathname != '/mycities' && !(!!msg)) {
            const div = document.createElement('div');
            div.className = 'loader';
            if (window.location.pathname == '/') {
                div.style.marginTop = '150px';
            }
            document.body.appendChild(div);
        }
    }
    if (loadingTXT == null) {
        const h4 = document.createElement('h4');
        h4.className = 'loadingTXT text-center';
        document.body.appendChild(h4);
    }
}