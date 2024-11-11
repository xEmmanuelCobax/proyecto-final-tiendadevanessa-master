// Obtener los elementos de audio y control de volumen
const audio = document.getElementById('audio-fondo');
const volumeControl = document.getElementById('volume');
const toggleAudio = document.getElementById("audio");
let audioEncendido = true; // Inicialmente true porque el audio está reproduciéndose

// Lista de reproducción de audios
const playlist = [
    "../../static/Audio/mavine.mp3",
    "../../static/Audio/Audio.mp3",
    "../../static/Audio/ventura.mp3"
];

let currentTrack = 0;

// Función para reproducir el siguiente audio en la lista de reproducción
function playNextTrack() {
    currentTrack++;
    if (currentTrack < playlist.length) {
        audio.src = playlist[currentTrack];
        audio.play();
    } else {
        currentTrack = 0; // Reinicia la lista de reproducción
        audio.src = playlist[currentTrack];
        audio.play();
    }
}

// Comprobar si hay un volumen guardado en localStorage
const savedVolume = localStorage.getItem('audioVolume');
if (savedVolume !== null) {
    audio.volume = savedVolume;
    volumeControl.value = savedVolume;
}

// Añadir un event listener al control de volumen
volumeControl.addEventListener('input', function () {
    const newVolume = this.value;
    audio.volume = newVolume;
    localStorage.setItem('audioVolume', newVolume);
});

// Añadir un event listener al botón de toggle audio
toggleAudio.addEventListener("click", function (event) {
    event.preventDefault(); // Evitar la acción predeterminada del enlace

    if (audioEncendido) {
        audio.pause();
        toggleAudio.innerHTML = '<i class="bi bi-music-note-beamed"></i>'; // Cambiar a icono de play
        audioEncendido = false;
    } else {
        audio.play();
        toggleAudio.innerHTML = '<i class="bi bi-pause-fill"></i>'; // Cambiar a icono de pausa
        audioEncendido = true;
    }
});

// Evento para cuando el audio termine de reproducirse
audio.addEventListener('ended', playNextTrack);

// Iniciar la reproducción del primer audio
audio.src = playlist[0];
audio.play();