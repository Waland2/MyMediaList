// Change color of the score circle
const CSRFTOKEN = Cookies.get('csrftoken');
document.addEventListener('DOMContentLoaded', (event) => {

    let circleScore = document.querySelector(".score-in-circle");
    let circle = circleScore.parentElement;
    let score = parseFloat(circleScore.innerText);

    if (score >= 8.0) {
        circle.style.borderColor = "rgb(0 175 49 / 70%)";
        circle.style.boxShadow = "0px 0px 8px rgb(0 255 71 / 70%)"
    }
    else if (score >= 6.0) {
        circle.style.borderColor = "rgb(0 175 113 / 70%)";
        circle.style.boxShadow = "0px 0px 8px rgb(0 175 113 / 70%)"
    }
    else if (score >= 4.0) {
        circle.style.borderColor = "rgb(167 170 47 / 70%)";
        circle.style.boxShadow = "0px 0px 8px rgb(167 170 47 / 70%)"
    }
    else if (score >= 2.0) {
        circle.style.borderColor = "rgb(182 125 0 / 70%)";
        circle.style.boxShadow = "0px 0px 8px rgb(182 125 0 / 70%)"
    }
    else {
        circle.style.borderColor = "rgb(175 0 0 / 70%)";
        circle.style.boxShadow = "0px 0px 8px rgb(175 0 0 / 70%)"
    }
})

function addToList() {
    document.querySelector('.addlist-block').classList.toggle('hide');
    document.querySelector('.ml-cancel').classList.toggle('hide')
    document.querySelector('.addlist-option').classList.toggle('hide');
}

function hideList() {
    document.querySelector('.addlist-block').classList.toggle('hide');
    document.querySelector('.ml-cancel').classList.toggle('hide')
    document.querySelector('.addlist-option').classList.toggle('hide');
}

function ml_hide() {
    redButton = document.querySelector('.addlist-block');
    redButton.classList.toggle('hide');
    redButton.innerText = "Edit list"
    hideList()
}

function ml_save() {
    var options = {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFTOKEN},
        mode: 'same-origin'
    }

    let formData = new FormData();
    
    formData.append('media_item_id', mediaItemId);
    formData.append('user_id', userID);
    formData.append('status', document.querySelector("#ml-status").value);
    formData.append('score', document.querySelector("#ml-score").value);
    formData.append('comment', document.querySelector("#ml-comment").value);

    options['body'] = formData;

    url = window.location.origin + "/list/";
    fetch(url, options);

    notification("Successfully added to the list", "success")
    redButton = document.querySelector('.addlist-block');
    redButton.querySelector("button").innerText = "Edit list"
    hideList()
}

function ml_delete() {
    notification("Successfully removed from the list", "info")
    redButton = document.querySelector('.addlist-block');
    redButton.querySelector("button").innerText = "Add to list"
    hideList()

    var options = {
        method: 'POST',
        headers: {'X-CSRFToken': CSRFTOKEN},
        mode: 'same-origin'
    }

    formData = new FormData()

    formData.append('media_item_id', mediaItemId);
    formData.append('user_id', userID);
    formData.append("delete", 1);

    options['body'] = formData;

    url = window.location.origin + "/list/";
    fetch(url, options);

    document.querySelector("#ml-status").value = "1";
    document.querySelector("#ml-score").value = "null";
    document.querySelector("#ml-comment").value = "";
}
