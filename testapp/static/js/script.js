//webcam으로 부터 데이터를 받아와 video로 보여줌
var video = document.querySelector(".videoElement");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia(vgaConstraints = {
        video: {width: {min: 1280}, height: {min: 720}}
    }).then(function (stream) {
        video.srcObject = stream;
    }).catch(function (err0r) {
        console.log(err0r)
        console.log("Something went wrong!");
    });
}

var snapshotCanvas = document.getElementById('snapshot');
var canvas = snapshotCanvas.getContext('2d');
canvas.width = video.videoWidth;
canvas.height = video.videoHeight;

function sendImage() {
    // Draw the video frame to the canvas
    canvas.drawImage(video, 0, 0);
    //이미지 전송
    var dataUrl = snapshotCanvas.toDataURL("image/png")
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: 'POST',
        url: '',
        data: {'img': dataUrl, 'csrfmiddlewaretoken': csrftoken}
    })
}

var video_start = document.getElementById("video_start")
var video_close = document.getElementById("video_close")
var time;
let index = 0;

video_start.addEventListener('click', function () {
    video_start.disabled = true
    time = 0;
    autoCapture = setInterval(function () {
        sendImage()
        time++;
        if (time >= 50) {
            video_close.disabled = false
        }
    }, 100);
})

video_close.addEventListener('click', function () {
    video_start.disabled = false
    video_close.disabled = true
    clearInterval(autoCapture)

    $.ajax({
        type: 'GET',
        url: '/translate/',
        data: {},
        success: function (result) {
            console.log(result);
            console.log(result.message);

            let prob = result.probability * 0.99;
            prob = prob.toFixed(7)

            $("#sign_language_div").text("");
            $("#sign_language_div").text(result.message + " " + prob);

            if(prob < 0.5){
                $("#sign_language_div").css('color', 'red');
            }else{
                $("#sign_language_div").css('color', 'black');
            }

            newTag = document.createElement("p");
            newTag.textContent = "환자 : " + result.message;
            $("#contents #final").append(newTag);
        }
    })
})