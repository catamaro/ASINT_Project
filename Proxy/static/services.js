function updateServicestable() {
    $.ajax({
        url: '/API/services/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }

            $('#servicesTable > tbody:last-child').empty()
            data["services"].forEach(v => {
                $('#servicesTable > tbody:last-child').
                    append('<tr><td>' + v["id"] + '</td><td>' + v["name"] + '</td><td>' + v["endpoint"] + '</td></tr>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Proxy service is down');
        }
    });

}

$(document).ready(function () {
    updateServicestable()
});