// Función para limpiar los campos del formulario de edición de producto
function limpiarEditModal() {
  // Obtener el formulario
  var form = document.getElementById("editproductform");

  // Restablecer el formulario
  form.reset();

  // Limpiar manualmente los campos que puedan necesitarlo
  document.getElementById("newmarca").value = "";
  document.getElementById("newproducto").value = "";
  document.getElementById("EditSelectUnitOfMeasure").selectedIndex = 0;
  document.getElementById("editunitquantity").value = "";
  document.getElementById("editunitLabel").textContent = "";
  document.getElementById("company-select2").selectedIndex = 0;
  document.getElementById("intermediary-select2").selectedIndex = 0;
  document.getElementById("intermediary-select2").disabled = true;
  document.getElementById("newcantidadInput").value = "";
  document.getElementById("newprecio2").value = "";

  // Remover clases de validación
  var inputs = form.querySelectorAll("input, select");
  inputs.forEach(function (input) {
    input.classList.remove("is-valid");
    input.classList.remove("is-invalid");
  });
}

// Escuchar el evento de cierre del modal
var editProductModal = document.getElementById("editproduct");
editProductModal.addEventListener("hidden.bs.modal", limpiarEditModal);

// Bloquear números negativos en el campo de precio
document.getElementById("newprecio2").addEventListener("input", function () {
  let value = this.value;

  // Permitir solo números, el punto decimal y una longitud máxima
  if (!/^\d*\.?\d*$/.test(value)) {
    this.value = value.slice(0, -1);
  }

  // Si el valor es menor a 0, ponerlo en vacío
  if (this.value <= 0) {
    this.value = "";
  }
});

// Bloquear números negativos en el campo de cantidad
document
  .getElementById("newcantidadInput")
  .addEventListener("input", function () {
    let value = this.value;

    // Permitir solo números, el punto decimal y una longitud máxima
    if (!/^\d*\.?\d*$/.test(value)) {
      this.value = value.slice(0, -1);
    }

    // Si el valor es menor a 0, ponerlo en vacío
    if (this.value <= 0) {
      this.value = "";
    }
  });
