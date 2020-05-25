var video = document.querySelector(".videoElement");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then(function (stream) {
            video.srcObject = stream;

            var snapshotCanvas = document.getElementById('snapshot');
            var captureButton = document.getElementById('capture');

            captureButton.addEventListener('click', function () {
                var context2 = snapshotCanvas.getContext('2d');
                // Draw the video frame to the canvas.
                context2.drawImage(video, 0, 0, snapshotCanvas.width,
                    snapshotCanvas.height);

                //이미지 전송
                    var dataUrl = snapshotCanvas.toDataURL("image/jpg", 1.0)
                console.log(dataUrl)

                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

                $.ajax({
                    type: 'POST',
                    url: '',
                    data:{'img': dataUrl , 'csrfmiddlewaretoken': csrftoken}
                })
            });

            var time = 1;
            autoCapture = setInterval(function () {
                captureButton.click()

                if(time == 4)  clearInterval(autoCapture)
                //document.test3.submit()
            }, 1000);
        })
        .catch(function (err0r) {
            console.log(err0r)
            console.log("Something went wrong!");
        });
}

var file_input = document.querySelector(".file_test");


