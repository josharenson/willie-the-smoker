function handleRelay(relay_active) {
    var image_name = relay_active ? "flame_on.svg" : "flame_off.svg";
    $("#relay").html("<img src='static/images/" + image_name + "' height=50 width=50 />");
}


function handleTemps(current_temps) {
    function createGauge(temp) {
        var id_name = temp.sensor_name.replace(' ', '-');
        $('#temp-gauges').append("<canvas id='" + id_name + "'></canvas>");
        new TemperatureGauge({destCanvasId: id_name, title: temp.sensor_name}).draw();
    }

    if (Array.isArray(current_temps) && current_temps.length) {
        current_temps.forEach(function(temp){
            var id_name = temp.sensor_name.replace(' ', '-');
            if ($("#" + id_name).length) {
                TemperatureGauge.updateTemp(id_name, temp.sensor_value);
            } else {
                createGauge(temp)
            }
        })
    }
}


function initializeDashboard() {
    var source = new EventSource('/stream');
    source.onmessage = function(m) {
        console.log(m.data)
        var current_temps = JSON.parse(m.data)["current_temps"]
        var relay_active = JSON.parse(m.data)["relay_active"]

        handleRelay(relay_active)
        handleTemps(current_temps)
    }
}
