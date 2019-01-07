var nMsgs = 0;
var maxMsgs = 5;


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
                $('#byrange').html("<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>");
                $('#br_form').hide();
            }
            else {
                $('#byrange').html(html_data);
                $('#br_form').show();
            }
        }],
        error: [function () {
            $('#byrange').html("<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>");
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
                $('#bybuilding').html("<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>");
                $('#bb_form').hide();
            }
            else {
                $('#bybuilding').html(html_data);
                $('#bb_form').show();
            }
        }],
        error: [function () {
            $('#bybuilding').html("<div class='col-md-12 col-sm-12 mb-12'><p>Nothing to show.</p></div>");
        }]
    });
};

function get_new_messages(){
    $.ajax({
        url: u_id + '/recv',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        success: [function (data) {
            console.log(data);
            var html_data = "";
            var i;
            for (i = 0; i < data.length; i++) {
                var from = data[i]['from'];
                var text = data[i]['text'];
                var datetime = data[i]['datetime'];
                html_data += "<div class='row msg'><div class='col-md-12 col-sm-12 mb-12'><p><div style='font-weight: bold;'>"+from+"</div>"+text+"</p><span class='time-right'>"+datetime+"</span></div></div>";
            }
            if(i != 0) {
                if(nMsgs >= maxMsgs) {
                    $('#new_msgs').html(html_data);
                    nMsgs = 0;
                }
                else {
                    $('#new_msgs').append(html_data);
                }
                nMsgs += data.length;
                var response = 1; // OK
                $.ajax({
                    url: u_id + '/ok',
                    type: 'POST',
                    data: JSON.stringify(response),
                })
            }
        }],
        error: [function () {

        }]
    });
};

function get_all_messages(){
    $.ajax({
        url: u_id + '/recvall',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        success: [function (data) {
            console.log(data);
            var html_data = "";
            var i;
            for (i = 0; i < data.length; i++) {
                var from = data[i]['from'];
                var text = data[i]['text'];
                var datetime = data[i]['datetime'];
                html_data += "<div class='row msg'><div class='col-md-12 col-sm-12 mb-12'><p><div style='font-weight: bold;'>"+from+"</div>"+text+"</p><span class='time-right'>"+datetime+"</span></div></div>";
            }
            $('#all_msgs').html(html_data);
        }],
        error: [function () {

        }]
    });
};

function validateInputLocation() {

    var lat = document.getElementById("lat").value;
    var long = document.getElementById("long").value;

    if (isNaN(lat) || lat < 0 || lat > 90) {
        alert("Input not valid");
    }
    else if (isNaN(long) || long < 0 || long > 180) {
        alert("Input not valid");
    }
    else {
        $.ajax({
            url: u_id + '/location',
            type: 'POST',
            data: { lat: lat, long: long },
            success: [function () {
                location.reload();
            }]
        })
    }
}

function validateInputRange() {

    var range = document.getElementById("range").value;

    if (isNaN(range) || range < 0 || range > 1000) {
        alert("Input not valid");
    }
    else {
        $.ajax({
            url: u_id + '/range',
            type: 'POST',
            data: { range: range },
            success: [function () {
                location.reload();
            }]
        })
    }
}

$(document).ready(function() {

    var nearbyUpdateTime = 60000;
    var msgsUpdateTime = 2000;
    $('#bb_form').hide();
    $('#br_form').hide();
    get_nearby_range();
    get_nearby_building();
    $('#recvall').click(function () {
        get_all_messages();
    });

    setInterval(get_nearby_range, nearbyUpdateTime);
    setInterval(get_nearby_building, nearbyUpdateTime);
    setInterval(get_new_messages, msgsUpdateTime);
});