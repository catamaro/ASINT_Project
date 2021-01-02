function updateStatstable() {
    $.ajax({
        url: '/API/stats/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }

            $('#statsTable > tbody:last-child').empty()
            data["stats"].forEach(v => {
                $('#statsTable > tbody:last-child').
                    append('<tr> <td>' + v["id"] + '</td><td>' + v["user"] 
                            + '</td><td>' + v["n_videos"] + '</td><td>' + v["n_views"] + '</td><td>' + v["n_question"] + '</td><td>' + v["n_answers"] + '</td></tr>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Statistics service is down');
        }
    });

}

$(document).ready(function () {
    updateStatstable()

    $("#buttonUpdateStatstable").click(
        function () {
            updateStatstable()
        }
    )
});