
function getVideoViews(videoID) {
    $.ajax({
        url: '/API/proxy_videos/' + videoID + '/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#nviews" + videoID).html(data['views'])
        },
    })
}
function updateVideostable() {
    $.ajax({
        url: '/API/proxy_videos/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            $('#videosTable > tbody:last-child').empty()
            data["videos"].forEach(v => {
                $('#videosTable > tbody:last-child').
                    append('<tr> <td>' + v["video_id"] + '</td><td>' + v["description"] + '</td><td id="nviews' + v["video_id"] + '">'+ '</td><td>' + "<a href='/QA/"+ v["video_id"] + "'>" + "Select" + "</a>" + '</td></tr>');
                getVideoViews(v["video_id"])
            });

            max = document.getElementById('videosTable').rows.length - 1
            $("#playVideoID").attr({"max": max});   
        }
    });

}
function addNewVideo(url, description) {
    let requestData = { "description": description, 'url': url }
    $.ajax({
        url: '/API/proxy_videos/',
        type: "POST",
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (data) {
            console.log("resppnse for video creation" + data)
            console.log(data)
            updateVideostable()
        }
    });
}
$(document).ready(function () {
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
        addNewVideo(newVideoURl, newVideoDESC)
    })
});

