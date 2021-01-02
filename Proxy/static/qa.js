const urlParams = new URLSearchParams(window.location.search);
const user = urlParams.get('ist_id')
const video_id = urlParams.get('id')
var q_infor = {}


function updateQuestiontable() {
  $.ajax({
    url: '/API/qa/question/' + video_id +"/",
    type: "GET",
    dataType: "json",
    success: function (data) {
      i = 0
      if (data === "failure") {
        handleError(xhr, status, ''); // manually trigger callback
      }
      q_infor = data["question"]
      $('#questionTable > tbody:last-child').empty()
      data["question"].forEach(q => {
        $('#questionTable > tbody:last-child').
          append('<tr> <td>' + i + '</td><td>' + q["curr_time"] + '</td><td>' + q["text"] + '</td><td>' + "<button type='button' onclick='showanswers(this);' class='btn btn-default'>" + "Show answers" + "</button>" + '</td></tr>');
          i++
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      alert('Question and Answers service is down');
    }
  });
}
var question_num = 0;
function showanswers(ctl) {
  var _row = $(ctl).parents("tr");
  var cols = _row.children("td");
  question_num = _row.children("td")[0].innerHTML
  $('#question_info').empty()
  $('#question_info').append('<br><h3>Question: </h3>' + q_infor[question_num]["Question"] +" - "+q_infor[question_num]["text"] + '<h3>Time: </h3>'+ q_infor[question_num]["curr_time"]
        + "<h3>User: </h3>" + q_infor[question_num]["user"] + "</h3>");
  updateAnswertable(q_infor[question_num]["Question"])
  answershow()
}
function updateAnswertable(question_num) {
  $.ajax({
    url: '/API/qa/answer/' + question_num + '/',
    type: "GET",
    dataType: "json",
    success: function (data) {
      if (data === "failure") {
        handleError(xhr, status, ''); // manually trigger callback
      }

      $('#answerTable > tbody:last-child').empty()
      data["answer"].forEach(a => {
        console.log(a["Answer"] + " " + a["question_id"] + " " + a["user"] + " " + a["a_text"])
        $('#answerTable > tbody:last-child').
          append('<tr> <td>' + a["Answer"] + '</td><td>' + a["question_id"] + '</td><td>' + a["user"] + '</td><td>' + a["a_text"] + '</td></tr>');
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      alert('Question and Answers service is down');
    }
  });
}
function addNewQuestion(curr_time, text) {
  let requestData = { "curr_time": curr_time, "user": user, "text": text }
  $.ajax({
    url: '/API/qa/question/' + video_id + '/',
    type: "POST",
    dataType: "json",
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function (data) {
      if (data === "failure") {
        handleError(xhr, status, ''); // manually trigger callback
      }
      console.log("response for question creation" + data)
      console.log(data)
      updateQuestiontable()
    },
    error: function (xhr, textStatus, errorThrown) {
      alert('Question and Answers service is down');
    }
  });
}
function addNewAnswer(a_text) {

  let requestData = { "user": user, "a_text": a_text }
  $.ajax({
    url: '/API/qa/answer/' + question_num + '/',
    type: "POST",
    dataType: "json",
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function (data) {
      if (data === "failure") {
        handleError(xhr, status, ''); // manually trigger callback
      }
      updateAnswertable(question_num)
    },
    error: function (xhr, textStatus, errorThrown) {
      alert('Question and Answers service is down');
    }
  });
}
$(document).ready(function () {
  updateQuestiontable()
  answerhide()
  addquestionhide()
  loadVideo()

  $("#buttonUpdateQuestionTable").click(
    function () {
      console.log('stop clicking me!')
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
    newText = $("#newText").val()
    addNewQuestion(newCurrTime, newText)
    addquestionhide()
    vPlayer.currentTime(parseFloat(pauseTime))
    vPlayer.play()
  })
  $("#buttonAddAnswer").click(function () {
    newAText = $("#newAText").val()
    addNewAnswer(newAText)
  })

  var vPlayer = videojs('videoPlayer');

  function loadVideo() {

    $.ajax({
      url: '/API/videos/' + video_id + '/',
      type: "GET",
      dataType: "json",
      success: function (data) {
        if (data === "failure") {
          handleError(xhr, status, ''); // manually trigger callback
        }
        url = data['url']

        vPlayer.src({ "type": "video/youtube", "src": url });
        vPlayer.play()

        let requestData = {'user': user, "video_id": video_id}
        $.ajax({
          url: '/API/videos/' + video_id + '/views/',
          type: "PUT",
          dataType: "json",
          contentType: 'application/json',
          data: JSON.stringify(requestData),
          success: function (data) {
            if (data === "failure") {
              handleError(xhr, status, ''); // manually trigger callback
            }
          },
          error: function (xhr, textStatus, errorThrown) {
            alert('Question and Answers service is down');
          }
        })
      },
      error: function (xhr, textStatus, errorThrown) {
        alert('Question and Answers service is down');
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