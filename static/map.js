const map_container = document.getElementById('map_container');
const map_calculate = document.getElementById('map_calculate');
const map_path = document.getElementById('map_path');
const start_x = document.getElementById('start_x');
const start_y = document.getElementById('start_y');
const destination_x = document.getElementById('destination_x');
const destination_y = document.getElementById('destination_y');

var set_location_flag = false;
var start_point = false;
var destination_point = false;
var calculating = false;
instance = panzoom(map_container);

map_calculate.addEventListener('mousedown', (ev) => {
    set_location_flag = true;
});

instance.on('transform', function (e) {
    set_location_flag = false;
});

map_calculate.addEventListener('mouseup', (evt) => {
    if (!calculating) {
        if ((set_location_flag == true) & (evt.which == 1)) {
            var e = evt.target;
            var dim = e.getBoundingClientRect();
            let x = Math.round((evt.clientX - dim.left) / instance.getTransform().scale);
            let y = Math.round((evt.clientY - dim.top) / instance.getTransform().scale);
            start_x.value = y;
            start_y.value = x;
            if (start_point) {
                var circle = document.getElementById('red_pin');
                circle.setAttributeNS(null, 'cx', x);
                circle.setAttributeNS(null, 'cy', y);
            } else {
                var svgns = "http://www.w3.org/2000/svg";
                var circle = document.createElementNS(svgns, 'circle');
                circle.setAttributeNS(null, 'cx', x);
                circle.setAttributeNS(null, 'cy', y);
                circle.setAttributeNS(null, 'r', '10');
                circle.setAttributeNS(null, 'fill', 'red');
                circle.setAttributeNS(null, 'id', 'red_pin');
                map_container.appendChild(circle);
                start_point = true;
            }
        }
    }
});

map_calculate.addEventListener('contextmenu', function (evt) {
    if (!calculating) {
        evt.preventDefault();
        if (set_location_flag == true) {
            let e = evt.target;
            let dim = e.getBoundingClientRect();
            let x = Math.round((evt.clientX - dim.left) / instance.getTransform().scale);
            let y = Math.round((evt.clientY - dim.top) / instance.getTransform().scale);
            destination_x.value = y;
            destination_y.value = x;
            if (destination_point) {
                let circle = document.getElementById('green_pin');
                circle.setAttributeNS(null, 'cx', x);
                circle.setAttributeNS(null, 'cy', y);
            } else {
                let svgns = "http://www.w3.org/2000/svg";
                let circle = document.createElementNS(svgns, 'circle');
                circle.setAttributeNS(null, 'cx', x);
                circle.setAttributeNS(null, 'cy', y);
                circle.setAttributeNS(null, 'r', '10');
                circle.setAttributeNS(null, 'fill', 'green');
                circle.setAttributeNS(null, 'id', 'green_pin');
                map_container.appendChild(circle);
                destination_point = true;
            }
        }
    }
}, false);

if (!result) {
    map_calculate.setAttributeNS(null, 'href', visual_map[map_select.value]);
}

function removePath() {
    let paras = document.getElementsByClassName('path');
    while (paras[0]) {
        paras[0].parentNode.removeChild(paras[0]);
    }
}

function show_history(id) {
    show_calculated_map();
}

function drawPath(data) {
    if (!data['done']) {
        removePath();
        data['response'].forEach((location) => {
            let svgns = "http://www.w3.org/2000/svg";
            let pixel = document.createElementNS(svgns, 'rect');
            pixel.setAttributeNS(null, 'height', 1);
            pixel.setAttributeNS(null, 'width', 1);
            pixel.setAttributeNS(null, 'x', location[1]);
            pixel.setAttributeNS(null, 'y', location[0]);
            pixel.setAttributeNS(null, 'class', 'path');
            map_container.appendChild(pixel);
        });
    } else {
        $('#map-distance-calculate').html(Math.round(data['response'][0]));
        $('#map-path-distance-calculate').html(Math.round(data['response'][1]));
        $('#map-time-calculate').html(Math.round(data['response'][2]));
        $('#calculate_options').hide();
        $('#response_detail').show();
        $('#calculate_btn').hide();
        $('#recalculate_btn').show();
        
        console.log(data['response']);
    }
}