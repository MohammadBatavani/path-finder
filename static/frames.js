const modal_container = document.querySelector('.modal-container');
const confirm_selectMap_btn = document.querySelector('#confirm-selectMap-btn');
const confirm_uploadMap_btn = document.querySelector('#confirm-uploadMap-btn');
const close_modal_buttons = document.querySelectorAll('.close-modal');

const new_calculate_btn = document.querySelector('.new-calculate');

const show_history_btn = document.querySelector('.show-history');
const show_home_btn = document.querySelector('.show-home');

const map_select = document.getElementById('map_select');

new_calculate_btn.addEventListener('click', show_map_form);

show_history_btn.addEventListener('click', show_history);
show_home_btn.addEventListener('click', show_home);


for (const close of close_modal_buttons) {

    close.addEventListener('click', hide_modal_container);
}

function show_map_form() {
    document.querySelector('.map-result').style.display = 'none';
    document.querySelector('.map-form').style.display = 'flex';
}

function show_calculated_map() {
    document.querySelector('.map-form').style.display = 'none';
    document.querySelector('.map-result').style.display = 'flex';
}

function hide_modal_container() {

    modal_container.querySelector('.modal.visible').classList.remove('visible');
    modal_container.classList.remove('visible');
}

function show_history() {
    show_history_btn.classList.add('active');
    show_home_btn.classList.remove('active');
    document.querySelector('.map-result').style.display = 'none';
    document.querySelector('.map-form').style.display = 'none';
    document.querySelector('.history-section').style.display = 'flex';
}

function show_home() {
    show_home_btn.classList.add('active');
    show_history_btn.classList.remove('active');
    document.querySelector('.history-section').style.display = 'none';
    document.querySelector('.map-form').style.display = 'flex';
}

map_select.addEventListener('change', (evt) => {
    map_calculate.setAttributeNS(null, 'href', visual_map[map_select.value]);
});

if (result) {
    show_calculated_map();
}