// Generates timer for sudoku time
function startTimer(duration, display) {
    // Set timer minutes and seconds
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        // Display the timer nicely
        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    Minutes = 10 * 60;
    display = document.querySelector('#time');
    startTimer(Minutes, display);
};

// When done button gets clicked, stop timer and provide time left
$(document).ready(function() {
  $('#done').click(function(event) {
     time_left = $("#time").html();
    //alert(time_left);
    document.getElementById('timeleft').value = time_left;
  });
});

