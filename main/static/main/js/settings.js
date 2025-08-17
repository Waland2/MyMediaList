const CSRFTOKEN = Cookies.get('csrftoken');
let boxes;
function saveSetting() {
    var options = {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFTOKEN},
        mode: 'same-origin'
    }

    formData = new FormData();

    boxes.forEach(el => {
        console.log(el.checked);
        formData.append(el.id, el.checked ? 1 : 0);
    })

    options['body'] = formData;

    url = window.location.origin + "/settings/";
    fetch(url, options);

    document.querySelector('.success-save').style.display = 'inline';
}

document.addEventListener('DOMContentLoaded', event => {
    boxes = document.querySelector('.settings-list').querySelectorAll('input');

    boxes.forEach(el => {
        el.checked = settings[el.id]
    })
})