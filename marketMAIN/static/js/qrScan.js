var isQuaggaStarted = false; // Variable global para rastrear si QuaggaJS está activo

function playBeep() {
  if (window.AudioContext || window.webkitAudioContext) {
    var context = new (window.AudioContext || window.webkitAudioContext)();
    var oscillator = context.createOscillator();
    oscillator.frequency.setValueAtTime(1000, context.currentTime);
    oscillator.connect(context.destination);
    oscillator.start();
    setTimeout(function () {
      oscillator.stop();
    }, 500);
  } else {
    console.error('El navegador no soporta la reproducción de sonidos.');
  }
}

function startCamera() {
  if (isQuaggaStarted) {
    Quagga.stop(); // Detener QuaggaJS si ya está activo
    isQuaggaStarted = false;
  }

  function calcularAncho() {
    var defaultWidthPercentage = 57.2;
    return (window.innerWidth * defaultWidthPercentage) / 100;
  }

  Quagga.init({
    inputStream: {
      name: "Live",
      type: "LiveStream",
      target: document.querySelector("#camera"),
      constraints: {
        width: calcularAncho(),
        height: 220,
        marginTop: '5%',
        marginRight: 0,
        marginBottom: 0,
        marginLeft: 0,
        padding: '10px'
      },
      area: {
        top: "0%",
        right: "0%",
        left: "0%",
        bottom: "0%"
      },
      singleChannel: false,
      zoom: {
        max: 3,
        min: 1,
        defaultValue: 3,
        pinchToZoom: true
      }
    },
    decoder: {
      readers: ["ean_reader", "ean_8_reader", "code_39_reader", "code_39_vin_reader", "codabar_reader", "upc_reader", "upc_e_reader", "i2of5_reader"]
    }
  }, function (err) {
    if (err) {
      console.error('Error al iniciar QuaggaJS:', err);
      alert('Error al iniciar QuaggaJS. Por favor, asegúrate de permitir el acceso a la cámara.');
      return;
    }
    console.log('QuaggaJS iniciado correctamente.');
    Quagga.start();
    isQuaggaStarted = true;
  });

  var scannedCodes = {};

  function addMostCommonCodeToList() {
    if (Object.keys(scannedCodes).length === 0) {
      console.log('No hay códigos de barras escaneados.');
      return;
    }

    var mostCommonCodes = Object.keys(scannedCodes).reduce(function (a, b) {
      return scannedCodes[a] > scannedCodes[b] ? a : b;
    });

    var last6Digits = mostCommonCodes.substring(Math.max(mostCommonCodes.length - 6, 0));

    console.log('Últimos 6 dígitos del código de barras más común:', last6Digits);

    var select = document.getElementById("qrCodes");
    var optionExists = Array.from(select.options).some(function (option) {
      return option.value === last6Digits;
    });

    if (!optionExists) {
      var option = document.createElement("option");
      option.text = last6Digits;
      select.add(option);
      playBeep();
    }

    scannedCodes = {};
  }

  var scanInterval;

  function startScanInterval() {
    scanInterval = setInterval(addMostCommonCodeToList, 1000);
  }

  function stopScanInterval() {
    clearInterval(scanInterval);
  }

  Quagga.onDetected(function (result) {
    var code = result.codeResult.code;
    console.log('Código de barras detectado:', code);

    if (code.length === 13) {
      console.log('Código de barras detectado:', code);

      scannedCodes[code] = (scannedCodes[code] || 0) + 1;

      Quagga.pause();

      setTimeout(function () {
        addMostCommonCodeToList();
        Quagga.start();
      }, 2000);
    }
  });

  Quagga.onProcessed(function (result) {
    var drawingCtx = Quagga.canvas.ctx.overlay,
      drawingCanvas = Quagga.canvas.dom.overlay;

    drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));

    if (result && result.boxes && result.boxes.length > 0) {
      var area = result.boxes[0];

      drawingCtx.strokeStyle = "#00f";
      drawingCtx.lineWidth = 2;
      drawingCtx.strokeRect(area.left, area.top, area.width, area.height);

      if (area) {
        drawingCtx.strokeStyle = "#00f";
        drawingCtx.lineWidth = 2;
        drawingCtx.beginPath();
        drawingCtx.moveTo(area[0][0], area[0][1]);
        for (var i = 1; i < area.length; i++) {
          drawingCtx.lineTo(area[i][0], area[i][1]);
        }
        drawingCtx.closePath();
        drawingCtx.stroke();
      }
    }
  });
}

var resizeTimer;
window.addEventListener('resize', function () {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function () {
    if (isQuaggaStarted) {
      stopCamera(); // Detener QuaggaJS al cambiar el tamaño de la ventana
      startCamera(); // Volver a iniciar QuaggaJS para ajustarse al nuevo tamaño
    }
  }, 200);
});

var myModal = document.getElementById('createmodal');
myModal.addEventListener('shown.bs.modal', function () {
  startCamera(); // Iniciar QuaggaJS cuando se abre el modal
});

myModal.addEventListener('hidden.bs.modal', function () {
  stopCamera(); // Detener QuaggaJS cuando se cierra el modal
});
