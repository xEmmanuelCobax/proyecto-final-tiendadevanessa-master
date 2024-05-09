function limpiarModal() {
  // Código para limpiar los campos del formulario modal
  document.getElementById("nombre").value = "";
  document.getElementById("presentacion").selectedIndex = 0;
  document.getElementById("cantidadInput").value = "";
  document.getElementById("compania").selectedIndex = 0;
  document.getElementById("cantidadSelect").value = 0;
  document.getElementById("precio").value = "";
  document.getElementById("qrCodes").innerHTML = "";
  // Detener la captura de QuaggaJS si está activa
  // Detener la captura de QuaggaJS si está activa
  // Agregar un evento cuando el modal se oculta
  var myModalEl = document.getElementById('createmodal');
  myModalEl.addEventListener('hidden.bs.modal', function (event) {
    // Detener QuaggaJS si está activo
    if (window.Quagga) {
      Quagga.stop();
      stopCamera(); // Detener QuaggaJS al cambiar el tamaño de la ventana

    }
  });
}

function actualizarCantidadOptions() {
  var presentacion = document.getElementById("presentacion").value;
  console.log("Presentación seleccionada:", presentacion); // Agregar este console.log() para depurar
  var cantidadSelect = document.getElementById("cantidadSelect");
  cantidadSelect.innerHTML = ""; // Limpiar las opciones existentes

  switch (presentacion) {
    case "botella":
      // Opciones específicas para botella
      addOption(cantidadSelect, "300 ml", "300ml");
      addOption(cantidadSelect, "1 litro", "1l");
      addOption(cantidadSelect, "500 ml", "500ml");
      addOption(cantidadSelect, "175 ml", "175ml");
      break;
    case "empaquetado":
      // Opciones específicas para empaquetado
      addOption(cantidadSelect, "10 unidades", "10 unidades");
      addOption(cantidadSelect, "20 unidades", "20 unidades");
      addOption(cantidadSelect, "50 unidades", "50 unidades");
      addOption(cantidadSelect, "100 unidades", "100 unidades");
      break;
    case "granel":
      // Opciones específicas para granel
      addOption(cantidadSelect, "1 kg", "1kg");
      addOption(cantidadSelect, "500 g", "500g");
      addOption(cantidadSelect, "250 g", "250g");
      addOption(cantidadSelect, "100 g", "100g");
      break;
    default:
      // Opciones por defecto
      addOption(cantidadSelect, "1", "1");
      addOption(cantidadSelect, "2", "2");
      addOption(cantidadSelect, "3", "3");
      break;
  }
  cantidadSelect.selectedIndex = 0;
}

// Función auxiliar para agregar opciones a un elemento select
function addOption(selectElement, text, value) {
  var option = document.createElement("option");
  option.text = text;
  option.value = value;
  selectElement.appendChild(option);
}

// Bloquear números negativos en el campo de precio
document.getElementById('precio').addEventListener('input', function () {
  if (this.value < 0) {
    this.value = '';
  }
});

// Bloquear números negativos en el campo de cantidad
document.getElementById('cantidadInput').addEventListener('input', function () {
  if (this.value < 0) {
    this.value = '';
  }
});