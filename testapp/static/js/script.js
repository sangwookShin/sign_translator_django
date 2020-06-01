
//webcam으로 부터 데이터를 받아와 video로 보여줌
var video = document.querySelector(".videoElement");
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log(err0r)
            console.log("Something went wrong!");
        });
}

var snapshotCanvas = document.getElementById('snapshot');
var captureButton = document.getElementById('video_start');

captureButton.addEventListener('click', function () {

});

var time = 1;
autoCapture = setInterval(function () {
    captureButton.click()

    console.log(time)

    if (time == 50) clearInterval(autoCapture)
    time++;
    //document.test3.submit()
}, 100);

function sendImage() {
    var context = snapshotCanvas.getContext('2d');
    // Draw the video frame to the canvas.
    context.drawImage(video, 0, 0, snapshotCanvas.width,
        snapshotCanvas.height);
    //이미지 전송
    var dataUrl = snapshotCanvas.toDataURL("image/jpg", 1.0)
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: 'POST',
        url: '',
        data: {'img': dataUrl, 'csrfmiddlewaretoken': csrftoken}
    })
}

var video_start = document.getElementById("video_start")
var video_close = document.getElementById("video_close")

video_start.addEventListener('click', function () {
    console.log('start')
    sendImage()
})

video_close.addEventListener('click', function () {
    console.log('close')

})