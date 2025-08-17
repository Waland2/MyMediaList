
function performGet() {
    let statusSelect = document.querySelector(".status-opt.selectednow");
    if (!statusSelect) statusSelect = document.querySelector('.status-opt.selected');
    let sortSelect = document.querySelector('.selectedsort');
    let filters = {};
    if (statusSelect) filters['status'] = statusSelect.dataset.watchStatus;

    if (sortSelect && sortSelect.dataset.sortType !== 'reset') {
        let sortType = sortSelect.dataset.sortType;
        filters['sort'] = sortType;
    }

    console.log(filters)
    let filts = new URLSearchParams(filters).toString(), url = window.location.origin + window.location.pathname + "?" + filts;

    window.location.replace(url);
}

document.addEventListener('DOMContentLoaded', event => {
    document.querySelectorAll('.status-opt').forEach(el => {
        el.addEventListener('click', event=> {
            event.target.classList.toggle('selectednow');
            performGet()
            
        })
    })

    let check = false;
    
    document.querySelectorAll('.status-opt').forEach(el => {
        if (el.dataset.watchStatus == statusID) {
            el.classList.toggle('selected');
            check = true;
        }
    })

    if (!check) {
        document.querySelector('.status-opt').classList.toggle('selected');
    }

    let count = 1;
    document.querySelectorAll('.t-index').forEach (el => {
        el.innerText = count;
        ++count;
    })

    document.querySelector('.table-head').querySelectorAll('td').forEach(el => {
        el.addEventListener('click', event => { 
            event.currentTarget.classList.add('selectedsort');
            performGet();
        })
    })
    
})