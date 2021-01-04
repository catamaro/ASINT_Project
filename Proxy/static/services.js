function updateServicestable() {
    $.ajax({
        url: '/API/services',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }

            $('#servicesTable > tbody:last-child').empty()
            data["services"].forEach(v => {
                $('#servicesTable > tbody:last-child').
                    append('<tr><td>' + v["id"] + '</td><td>' + v["port"] + '</td><td>' + v["name"] + '</td><td>' + v["endpoint"] + '</td><td>' + "<button type='button' onclick='deleteMicroservice(this)' class='btn btn-default'>" + "<i class='close icon'></i>" + "</button>" + '</td></tr>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Proxy service is down');
        }
    });

}
function deleteMicroservice(ctl) {
    var _row = $(ctl).parents("tr");
    var cols = _row.children("td");
    question_num = _row.children("td")[0].innerHTML

    $.ajax({
        url: '/API/services/delete/'+question_num,
        type: "DELETE",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }
            updateServicestable()
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Proxy service is down');
        }
    });
}

$(document).ready(function () {
    updateServicestable()
});