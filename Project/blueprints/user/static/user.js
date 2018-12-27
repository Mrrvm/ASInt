function get_nearby_range(){
    $.ajax({
        url: u_id + '/nearby_range',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        success: [function (data) {
            var html_data = "";
            var i;
            for (i = 0; i < data.length; i++) {
                var image = new Image();
                image.src = 'data:  image/png;base64,' + data[i]["photo"];
                var name = data[i]['name'];
                html_data += "<div class='col-md-2 col-sm-2 mb-2'><img class='contacts' src='" + image.src + "'/></div><div class='col-md-8 col-sm-8 mb-8'><p>" + name + "</p></div><div class='col-md-2 col-sm-2 mb-2'></div>";
            }
            if(i==0) {
                document.getElementById("byrange").innerHTML = "<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>";
                $('#br_form').hide();
            }
            else {
                document.getElementById("byrange").innerHTML = html_data;
                $('#br_form').show();
            }
        }],
        error: [function () {
            document.getElementById("byrange").innerHTML = "<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>";
        }]
    });
};

function get_nearby_building(){
    $.ajax({
        url: u_id + '/nearby_buildings',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        success: [function (data) {
            var html_data = "";
            var i;
            for (i = 0; i < data.length; i++) {
                var image = new Image();
                image.src = 'data:  image/png;base64,' + data[i]["photo"];
                var name = data[i]['name'];
                html_data += "<div class='col-md-2 col-sm-2 mb-2'><img class='contacts' src='" + image.src + "'/></div><div class='col-md-8 col-sm-8 mb-8'><p>" + name + "</p></div><div class='col-md-2 col-sm-2 mb-2'></div>";
            }
            if(i == 0) {
                document.getElementById("bybuilding").innerHTML = "<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>";
                $('#bb_form').hide();
            }
            else {
                document.getElementById("bybuilding").innerHTML = html_data;
                $('#bb_form').show();
            }
        }],
        error: [function () {
            document.getElementById("bybuilding").innerHTML = "<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>";
        }]
    });
};

$(document).ready(function() {
    var nearbyUpdateTime = 60000;
    $('#bb_form').hide();
    $('#br_form').hide();
    get_nearby_range();
    get_nearby_building();

    setInterval(get_nearby_range, nearbyUpdateTime);
    setInterval(get_nearby_building, nearbyUpdateTime);
});