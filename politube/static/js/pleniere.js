$(document).ready(function() {
  $('video').mediaelementplayer();
});

play = function (t)
{
  var video = $('video').get(0);
  video.currentTime = t;
  video.play();
}

startIfNeeded = function ()
{
  var h = window.location.hash;
  if (h != '#') {
    t = parseInt(h.replace('#', ''));
    if (t) {
      play(t);
    }
  }
}
