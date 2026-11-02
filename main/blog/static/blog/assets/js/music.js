(function () {
  'use strict';

  function formatTime(secs) {
    if (!isFinite(secs) || secs < 0) {
      secs = 0;
    }
    var hr = Math.floor(secs / 3600);
    var min = Math.floor((secs - hr * 3600) / 60);
    var sec = Math.floor(secs - hr * 3600 - min * 60);
    min = min > 9 ? min : '0' + min;
    sec = sec > 9 ? sec : '0' + sec;
    return min + ':' + sec;
  }

  function init() {
    var player = document.querySelector('.mhn-player');
    if (!player) {
      return;
    }

    var playList = player.querySelector('.play-list');
    var tracks = Array.prototype.slice.call(player.querySelectorAll('.play-list .play'));
    if (!tracks.length) {
      return;
    }

    var audioWrap = player.querySelector('.audio');
    var albumArt = player.querySelector('.album-art');
    var songArtist = player.querySelector('.current-info .song-artist');
    var songAlbum = player.querySelector('.current-info .song-album');
    var songTitle = player.querySelector('.current-info .song-title');
    var playPosition = player.querySelector('.play-position');
    var currentTimeEl = player.querySelector('.play-current-time');
    var totalTimeEl = player.querySelector('.play-total-time');
    var progressBar = player.querySelector('.progress .bar');
    var playPauseBtn = player.querySelector('.play-pause');
    var stopBtn = player.querySelector('.stop');
    var prevBtn = player.querySelector('.prev');
    var nextBtn = player.querySelector('.next');
    var volumeInput = player.querySelector('.volume');
    var toggleBtn = player.querySelector('.toggle-play-list');

    var audio = null;
    var currentIndex = -1;

    tracks.forEach(function (el) {
      var album = el.dataset.album;
      var artist = el.dataset.artist;
      var title = el.dataset.title;
      var albumart = el.dataset.albumart;
      var thumb = albumart
        ? '<div class="album-thumb pull-left"><img src="' + albumart + '" alt=""></div>'
        : '';
      var info = '<div class="songs-info pull-left">' +
        (title || 'Unknown Title') +
        '<div class="songs-detail">' +
        (artist || 'Unknown Artist') + ' - ' + (album || 'Unknown Album') +
        '</div></div>';
      el.innerHTML = thumb + info;
    });

    function ensureAudio() {
      if (audio) {
        return audio;
      }
      audio = document.createElement('audio');
      audio.className = 'music';
      audio.preload = 'metadata';
      if (volumeInput) {
        audio.volume = parseFloat(volumeInput.value);
      }
      audio.addEventListener('ended', playNext);
      audio.addEventListener('timeupdate', updateProgress);
      audio.addEventListener('loadedmetadata', function () {
        totalTimeEl.textContent = formatTime(audio.duration);
      });
      audio.addEventListener('play', function () {
        playPauseBtn.classList.add('active');
      });
      audio.addEventListener('pause', function () {
        playPauseBtn.classList.remove('active');
      });
      audioWrap.appendChild(audio);
      return audio;
    }

    function updateProgress() {
      if (!audio) {
        return;
      }
      currentTimeEl.textContent = formatTime(audio.currentTime);
      if (audio.duration) {
        progressBar.style.width = (audio.currentTime / audio.duration) * 100 + '%';
      }
    }

    function setActive(index) {
      tracks.forEach(function (el, i) {
        el.classList.toggle('active', i === index);
      });
      currentIndex = index;
      playPosition.textContent = (index + 1) + ' / ' + tracks.length;
    }

    function loadTrack(index, autoplay) {
      var el = tracks[index];
      if (!el) {
        return;
      }
      var a = ensureAudio();
      setActive(index);

      songArtist.textContent = el.dataset.artist || 'Unknown Artist';
      songAlbum.textContent = el.dataset.album || 'Unknown Album';
      songTitle.textContent = el.dataset.title || 'Unknown Title';
      albumArt.innerHTML = el.dataset.albumart
        ? '<img src="' + el.dataset.albumart + '" alt="">'
        : '';

      currentTimeEl.textContent = '00:00';
      totalTimeEl.textContent = '00:00';
      progressBar.style.width = '0%';

      a.src = el.dataset.url;
      if (autoplay !== false) {
        a.play().catch(function () {});
      }
    }

    function playPause() {
      if (!audio || currentIndex === -1) {
        loadTrack(0, true);
        return;
      }
      if (audio.paused) {
        audio.play().catch(function () {});
      } else {
        audio.pause();
      }
    }

    function playNext() {
      loadTrack((currentIndex + 1) % tracks.length, true);
    }

    function playPrev() {
      loadTrack(currentIndex <= 0 ? tracks.length - 1 : currentIndex - 1, true);
    }

    function stop() {
      if (!audio) {
        return;
      }
      audio.pause();
      audio.currentTime = 0;
      progressBar.style.width = '0%';
      currentTimeEl.textContent = '00:00';
    }

    function hidePlaylist() {
      playList.style.display = 'none';
      if (toggleBtn) {
        toggleBtn.classList.remove('active');
      }
      albumArt.classList.remove('blur');
    }

    tracks.forEach(function (el, index) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        loadTrack(index, true);
        hidePlaylist();
      });
    });

    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', function (e) {
        e.preventDefault();
        playPause();
      });
    }
    if (stopBtn) {
      stopBtn.addEventListener('click', function (e) {
        e.preventDefault();
        stop();
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', function (e) {
        e.preventDefault();
        playPrev();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function (e) {
        e.preventDefault();
        playNext();
      });
    }
    if (volumeInput) {
      volumeInput.addEventListener('input', function () {
        volumeInput.setAttribute('data-css', volumeInput.value);
        if (audio) {
          audio.volume = parseFloat(volumeInput.value);
        }
      });
    }
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (toggleBtn.classList.contains('active')) {
          hidePlaylist();
        } else {
          playList.style.display = 'block';
          toggleBtn.classList.add('active');
          albumArt.classList.add('blur');
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
