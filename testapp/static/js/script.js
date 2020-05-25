var video = document.querySelector(".videoElement");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then(function (stream) {
            video.srcObject = stream;

            var snapshotCanvas = document.getElementById('snapshot');
            var captureButton = document.getElementById('capture');
            var image_input = document.getElementsByClassName("file_test")

            captureButton.addEventListener('click', function () {
                var context2 = snapshot.getContext('2d');
                // Draw the video frame to the canvas.
                context2.drawImage(video, 0, 0, snapshotCanvas.width,
                    snapshotCanvas.height);
                console.log(typeof (video))
            });

            autoCapture = setInterval(function () {
                captureButton.click()

                //document.test3.submit()
            }, 1000);
        })
        .catch(function (err0r) {
            console.log(err0r)
            console.log("Something went wrong!");
        });
}

var file_input = document.querySelector(".file_test");


