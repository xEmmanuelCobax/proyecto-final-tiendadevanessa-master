  // Función para limpiar los campos del formulario de creación de producto
  function limpiarCreateModal() {
    // Obtener el formulario
    var form = document.getElementById('createproductmodal');

    // Restablecer el formulario
    form.reset();

    // Limpiar manualmente los campos que puedan necesitarlo
    document.getElementById('marca').value = '';
    document.getElementById('producto').value = '';
    document.getElementById('SelectUnitOfMeasure').selectedIndex = 0;
    document.getElementById('unitquantity').value = '';
    document.getElementById('unitLabel').textContent = '';
    document.getElementById('company-select').selectedIndex = 0;
    document.getElementById('intermediary-select').selectedIndex = 0;
    document.getElementById('intermediary-select').disabled = true;
    document.getElementById('cantidadInput').value = '';
    document.getElementById('newprecio').value = '';

    // Remover clases de validación
    var inputs = form.querySelectorAll('input, select');
    inputs.forEach(function(input) {
      input.classList.remove('is-valid');
      input.classList.remove('is-invalid');
    });
  }

  // Escuchar el evento de cierre del modal
  var createProductModal = document.getElementById('createmodal');
  createProductModal.addEventListener('hidden.bs.modal', limpiarCreateModal);

// Bloquear números negativos en el campo de precio
document.getElementById("precio").addEventListener("input", function () {
  if (this.value < 0) {
    this.value = "";
  }
});

// Bloquear números negativos en el campo de cantidad
document.getElementById("cantidadInput").addEventListener("input", function () {
  if (this.value < 0) {
    this.value = "";
  }
});
