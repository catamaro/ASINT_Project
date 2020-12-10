var pathname = window.location.pathname;
var video_id = pathname.split("/")[2]

function updateQuestiontable() {
  $.ajax({
    url: '/API/proxy_question/',
    type: "GET",
    dataType: "json",
    success: function (data) {
      console.log(data);
      $('#questionTable > tbody:last-child').empty()
      data["qa"].forEach(q => {
        $('#questionTable > tbody:last-child').
          append('<tr> <td>' + q["Question"] + '</td><td>' + q["video_id"] + '</td><td>' + q["curr_time"] + '</td><td>' + q["user"] + '</td><td>' + q["text"] + '</td><td>' + "<button type='button' onclick='showanswers(this);' class='btn btn-default'>" + "Show answers" + "</button>" + '</td></tr>');
      });
    }
  });
}
var question_num = 0;
function showanswers(ctl) {
  var _row = $(ctl).parents("tr");
  var cols = _row.children("td");
  question_num = _row.children("td")[0].innerHTML

  updateAnswertable(question_num)
  answershow()
}
function updateAnswertable(question_num) {
  $.ajax({
    url: '/API/proxy_answer/' + question_num + '/',
    type: "GET",
    dataType: "json",
    success: function (data) {
      $('#answerTable > tbody:last-child').empty()
      data["answer"].forEach(a => {
        console.log(a["Answer"] + " " + a["question_id"] + " " + a["a_user"] + " " + a["a_text"])
        $('#answerTable > tbody:last-child').
          append('<tr> <td>' + a["Answer"] + '</td><td>' + a["question_id"] + '</td><td>' + a["a_user"] + '</td><td>' + a["a_text"] + '</td></tr>');
      });
    }
  });
}
function addNewQuestion(curr_time, user, text) {
  let requestData = { "curr_time": curr_time, "user": user, "text": text }
  $.ajax({
    url: '/API/proxy_question/' + video_id + '/',
    type: "POST",
    dataType: "json",
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function (data) {
      console.log("response for question creation" + data)
      console.log(data)
      updateQuestiontable()
    }
  });
}
function addNewAnswer(a_user, a_text) {

  let requestData = { "a_user": a_user, "a_text": a_text }
  $.ajax({
    url: '/API/proxy_answer/' + question_num + '/',
    type: "POST",
    dataType: "json",
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function (data) {
      console.log("response for Answer creation" + data)
      console.log(data)
      updateAnswertable(question_num)
    }
  });
}
$(document).ready(function () {
  updateQuestiontable()
  answerhide()
  addquestionhide()
  loadVideo()
  $("#buttonUpdateQuestiontable").click(
    function () {
      updateQuestiontable()
    }
  )
  $("#buttonUpdateAnswertable").click(
    function () {
      updateAnswertable(question_num)
    }
  )
    
  $("#buttonAddQuestion").click(function () {
    vPlayer.pause()  
    addquestionshow()
  })

  $("#buttonSubmitQuestion").click(function () {
    var pauseTime = vPlayer.currentTime()
    newCurrTime = pauseTime
    newUser = $("#newUser").val()
    newText = $("#newText").val()
    addNewQuestion(newCurrTime, newUser, newText)
    addquestionhide()
    vPlayer.currentTime(parseFloat($("#resumetime").val()))
    vPlayer.play()
  })
  $("#buttonAddAnswer").click(function () {
    newAUser = $("#newAUser").val()
    newAText = $("#newAText").val()
    addNewAnswer(newAUser, newAText)
  })

  var vPlayer = videojs('videoPlayer');

  function loadVideo() {

    $.ajax({
      url: '/API/proxy_videos/' + video_id + '/',
      type: "GET",
      dataType: "json",
      success: function (data) {
        url = data['url']

        vPlayer.src({ "type": "video/youtube", "src": url });
        vPlayer.play()

        $.ajax({
          url: '/API/proxy_videos/' + video_id + '/views',
          type: "PUT",
          dataType: "json",
        })
      }
    });
  }

  $("#buttonVideoPause").click(function () {
    vPlayer.pause()
    var pauseTime = vPlayer.currentTime()
    $("#resumetime").val(pauseTime)

  })
  $("#buttonVideoResume").click(function () {
    vPlayer.currentTime(parseFloat($("#resumetime").val()))
    vPlayer.play()
  })
});

function addquestionshow() {
    document.getElementById("add_question_div").style.display = "block";
  }
  function addquestionhide() {
    document.getElementById("add_question_div").style.display = "none";
  }
function answershow() {
  document.getElementById("answers_div").style.display = "block";
}
function answerhide() {
  document.getElementById("answers_div").style.display = "none";
}