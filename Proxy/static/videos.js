const urlParams = new URLSearchParams(window.location.search);
const ist_id = urlParams.get('ist_id')
const uname = urlParams.get('name')


function getVideoViews(videoID) {
    $.ajax({
        url: '/API/videos/' + videoID + '/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }
            $("#nviews" + videoID).html(data['views'])
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Videos service is down');
        }
    })
}
function updateVideostable() {
    $.ajax({
        url: '/API/videos/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }

            $('#videosTable > tbody:last-child').empty()
            data["videos"].forEach(v => {
                $('#videosTable > tbody:last-child').
                    append('<tr> <td>' + v["video_id"] + '</td><td>' + v["ist_id"] + '</td><td>' + v["description"] + '</td><td id="nviews' + v["video_id"] + '">' + '</td><td>' + "<a href='/QA/" + v["video_id"] + "/" + ist_id + "/" + uname + "'>" + "Select" + "</a>" + '</td></tr>');
                getVideoViews(v["video_id"])
            });

            max = document.getElementById('videosTable').rows.length - 1
            $("#playVideoID").attr({ "max": max });
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Videos service is down');
        }
    });

}
function addNewVideo(url, description) {
    let requestData = {"description": description, 'url': url , 'user': ist_id, 'name': uname}
    $.ajax({
        url: '/API/videos/',
        type: "POST",
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (data) {
            if (data === "failure" ) {
                handleError(xhr, status, ''); // manually trigger callback
            }
            updateVideostable()
        },
        error: function (xhr, textStatus, errorThrown) {
            alert('Videos service is down');
        }
    });
}
$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);

    updateVideostable()

    $("#buttonUpdateVideotable").click(
        function () {
            updateVideostable()
        }
    )

    $("#formAddVideo").submit(function (e) {
        e.preventDefault()

        newVideoURl = $("#newVideoURL").val()
        newVideoDESC = $("#newVideoDescription").val()
        newVideoUser = urlParams.get('ist_id')

        addNewVideo(newVideoURl, newVideoDESC)
    })
});

