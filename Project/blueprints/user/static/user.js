function get_datetime(){
    var currentdate = new Date();
    return currentdate.toLocaleString();
}


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
            for (var i = 0; i < data.length; i++) {
                var datetime = get_datetime();
                var from = data[i]['from'];
                var text = data[i]['text'];
                html_data += "<div class='row msg'><div class='col-md-12 col-sm-12 mb-12'><p><div style='font-weight: bold;'>"+from+"</div>"+text+"</p><span class='time-right'>"+datetime+"</span></div></div>";
            }
            document.getElementById("new_msgs").innerHTML = html_data;
            var response = 1; // OK
            $.ajax({
                url: u_id + '/ok',
                type: 'POST',
                data: JSON.stringify(response),
            })
        }],
        error: [function () {

        }]
    });
};

$(document).ready(function() {
    var nearbyUpdateTime = 60000;
    var msgsUpdateTime = 2000;
    $('#bb_form').hide();
    $('#br_form').hide();
    get_nearby_range();
    get_nearby_building();

    setInterval(get_nearby_range, nearbyUpdateTime);
    setInterval(get_nearby_building, nearbyUpdateTime);
    setInterval(get_new_messages, msgsUpdateTime);
});