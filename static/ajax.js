// this is the id of the form
$("#calculate_form").submit(function (e) {
    calculating = true;
    
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        xhrFields: {
            onprogress: (e) => {
                $('#algorithm-select').attr('disabled', 'disabled');
                $('#solider-type-select').attr('disabled', 'disabled');
                $('#map_select').attr('disabled', 'disabled')
                // console.log(e); // show response from the php script.
                var response = e.currentTarget.response;
                console.log(response);
                response = JSON.parse(response.slice(response.lastIndexOf('{')).replaceAll("'", '"').replaceAll("F", "f").replaceAll("T", "t").replaceAll("(", "[").replaceAll(")", "]"));
                
                drawPath(response);
            }
        }
    });

});