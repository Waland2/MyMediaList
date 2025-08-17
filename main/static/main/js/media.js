function applyFilters() {
    let filters = {};
    // sort filter
    var sortBy = document.querySelector('#sort');
    let sortval = sortBy.attributes['data-sort-value'].value, sortdir = sortBy.attributes['data-sort-dir'].value;
    if (sortval) {
        let sf = sortval;
        if (sortdir === '1') sf = "-" + sortval;
        filters['sort'] = sf;
    }


    // other filters 
    boxes = document.querySelectorAll('input[type="checkbox"]:checked');
    boxes.forEach(el => {
        filtertype = el.attributes['data-filtertype'].value;
        filterval = el.id;

        if (filters[filtertype]) {
            filters[filtertype] += "," + filterval;
        }else {
            filters[filtertype] = filterval;
        }
    })

    var newUrl = window.location.origin + window.location.pathname + "?" + new URLSearchParams(filters).toString();
    history.pushState({}, '', newUrl);

    filters['media_only'] = 1;
    let filtersUrl = new URLSearchParams(filters).toString();

    fetch(`?${filtersUrl}`)
    .then(response => response.text())
    .then(html => {
        c_entries = document.querySelector(".catalogue");
        c_entries.innerHTML = html;
    })
}


function closeSortSelect(event) {
    if (!document.querySelector(".sortopt").contains(event.target)) {
        document.removeEventListener('click', closeSortSelect);
    }else {
        openSortMenuButton = document.querySelector("#sort");
        if (openSortMenuButton.contains(event.target)) return;

        let sortval = event.target.attributes['data-sort-type'].value, sortdir = 0;
        
        if (event.target.classList.contains('activesort')) {

            sortdir = 1 - openSortMenuButton.attributes['data-sort-dir'].value;
            openSortMenuButton.querySelector(".sort-typedir").classList.toggle(`sortdir-${1 - sortdir}`);
        }else {
            document.querySelector(".activesort").classList.toggle("activesort");
            event.target.classList.toggle("activesort");

            if (openSortMenuButton.attributes['data-sort-dir'].value === '1') openSortMenuButton.querySelector(".sort-typedir").classList.toggle(`sortdir-1`);
        }

        openSortMenuButton.querySelector(".sort-typename").innerText = event.target.innerText;
        openSortMenuButton.querySelector(".sort-typedir").classList.toggle(`sortdir-${sortdir}`);

        openSortMenuButton.attributes['data-sort-value'].value = sortval;
        openSortMenuButton.attributes['data-sort-dir'].value = sortdir;
        applyFilters();
    }
    sortSelect.classList.remove("open");
}

function showSortSelect() {
    sortSelect = document.querySelector(".hiddenopt");
    sortSelect.classList.toggle("open")
    document.addEventListener('click', closeSortSelect);
}

function resetFilters() {
    var baseUrl = window.location.href.split('?')[0];
    window.location.href = baseUrl;
}

document.addEventListener('DOMContentLoaded', (event) => {
    let getQueries = {};
    const urlParams = new URLSearchParams(window.location.search);
    for (const [key, value] of urlParams) {
        getQueries[key] = value;
    }

    // Sort filter
    let sortval, sortdir = 0;
    if (getQueries['sort']) {
        sortval = getQueries['sort']
        if (sortval[0] === '-') {
            sortval = sortval.replace('-', '');
            sortdir = 1;
        }
    }else {
        sortval = "rating";
        sortdir = 0;
    }

    sortType = document.querySelector(`[data-sort-type=${sortval}]`);
    sortType.classList.toggle("activesort");


    openSortMenuButton = document.querySelector("#sort");
    openSortMenuButton.querySelector(".sort-typename").innerText = sortType.innerText;
    openSortMenuButton.querySelector(".sort-typedir").classList.toggle(`sortdir-${sortdir}`);

    openSortMenuButton.attributes['data-sort-value'].value = sortval;
    openSortMenuButton.attributes['data-sort-dir'].value = sortdir;

    // Other filters
    boxes = document.querySelector(".filter-setting").querySelectorAll("input");

    titleFilt = "";
    boxes.forEach(el => {
        filtertype = el.attributes['data-filtertype'].value;
        q = getQueries[filtertype];
        if (q) {
            if (q.includes(',')) {
                for (let i of q.split(',')) {
                    if (i == el.id) el.checked = true;
                }
            }else if (q == el.id) el.checked = true;

        }

        el.addEventListener('click', (event) => {
            applyFilters();
        })
    });
})