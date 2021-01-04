function updateLogstable() {
    $.ajax({
        url: '/API/logs',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }

            $('#eventsTable > tbody:last-child').empty()
            data["events"].forEach(v => {
                $('#eventsTable > tbody:last-child').
                    append('<tr> <td>' + v["id"] + '</td><td>' + v["IP"] 
                            + '</td><td>' + v["endpoint"] + '</td><td>' + v["timestamp"] + '</td></tr>');
            });

            $('#dataCreationTable > tbody:last-child').empty()
            data["data_creation"].forEach(v => {
                $('#dataCreationTable > tbody:last-child').
                    append('<tr> <td>' + v["id"] + '</td><td>' + v["type"] 
                            + '</td><td>' + v["content"] + '</td><td>' + v["timestamp"] 
                            + '</td><td>' + v["user"] + '</td></tr>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Logs service is down');
        }
    });

}

$(document).ready(function () {
    updateLogstable()
});