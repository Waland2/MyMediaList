function notification(text, type) { // need to fix
    checkNotif = document.querySelector(".notif");
    console.log(checkNotif);
    if (checkNotif) {
        checkNotif.remove();
        setTimeout(notification(text, type), 2000);
        return;
    }

    myDiv = document.createElement("div");
    myDiv.className = `notif ${type}`
    myDiv.appendChild(document.createElement("div"));

    myDivContent = myDiv.querySelector("div");
    myDivContent.className = `notifcontent ${type}`;
    myDivContent.innerText = text;

    document.querySelector("header").before(myDiv);

    myDiv.style.display = 'flex';
    setTimeout(() => {
      myDiv.style.opacity = 1;
      myDivContent.style.transform = 'translateY(0)';
      myDivContent.style.opacity = 1;
      
    }, 100);

    function closePopup() {
        myDiv.style.opacity = 0;
        myDivContent.style.transform = 'translateY(-100%)';
        setTimeout(() => {
            myDiv.remove();
        }, 500);
    }

    setTimeout(() => closePopup(), 3000);

    myDiv.addEventListener("click", () => closePopup());
}

function showShadowScreen() {
    let screen = document.querySelector('#shadscreen');
    
    if (!screen.classList.contains('shadow-screen')) {
        screen.classList.add('shadow-screen');
    }
}

function getSearchResult(event) { 
    link = window.location.origin + "/search/?search=" + event.target.value
    console.log(event.target.value);
    if (event.target.value.length < 1) {
        document.querySelector(".searched-container").innerHTML = "";
        return; 
    }
    fetch(link)
    .then(response => response.text())
    .then(html => document.querySelector(".searched-container").innerHTML = html)
}

function searchKeyDown(event) {
    if (event.key === "Escape") {
        cancelSearch()
        document.querySelector('#search').blur(); 
    }
}

function cleanSearch() {
    document.querySelector('#search').value = "";
    document.querySelector(".searched-container").innerHTML = ""; 
}

function cancelSearch() {
    cleanSearch();
    document.querySelector("#shadscreen").classList.toggle("shadow-screen"); 
    if (window.getComputedStyle(document.querySelector('.search-start-btn')).getPropertyValue('display') !== 'none') {
        document.querySelector('.search-block').style.display = 'none';
    }
}

function showSearchInput() {
    let sblock = document.querySelector('.search-block');
    sblock.style.display = 'block';
    document.querySelector('#search').focus();  
}

function isAuth() {
    return userAuth;
}

