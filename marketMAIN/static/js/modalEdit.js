function limpiarEditModal() {
    // Limpiar los campos del formulario modal de edición
    document.getElementById("newnombre").value = "";
    console.log('pasa aqui 1'); 
    document.getElementById("newpresentacion").selectedIndex = 0;
    console.log('pasa aqui 1'); 
    document.getElementById("newcantidadInput").value = "";
    console.log('pasa aqui 1'); 
    document.getElementById("newcompania").selectedIndex = 0;
    console.log('pasa aqui 1'); 
    document.getElementById("newcantidadSelect").selectedIndex = 0;
    console.log('pasa aqui 1'); 
    document.getElementById("newprecio").value = "";
    console.log('pasa aqui 1'); 
    // Limpiar los códigos de barras escaneados (si es aplicable)
}

function updateNewQuantityOptions() {
    var newPresentacion = document.getElementById("newpresentacion").value;
    console.log("Selected Presentation:", newPresentacion); // Debugging
    var newCantidadSelect = document.getElementById("newcantidadSelect");
    newCantidadSelect.innerHTML = ""; // Limpiar las opciones existentes

    switch (newPresentacion) {
        case "botella":
            // Opciones específicas para botella
            addOption(newCantidadSelect, "300 ml", "300ml");
            addOption(newCantidadSelect, "1 litro", "1l");
            addOption(newCantidadSelect, "500 ml", "500ml");
            addOption(newCantidadSelect, "175 ml", "175ml");
            break;
        case "empaquetado":
            // Opciones específicas para empaquetado
            addOption(newCantidadSelect, "10 unidades", "10 unidades");
            addOption(newCantidadSelect, "20 unidades", "20 unidades");
            addOption(newCantidadSelect, "50 unidades", "50 unidades");
            addOption(newCantidadSelect, "100 unidades", "100 unidades");
            break;
        case "granel":
            // Opciones específicas para granel
            addOption(newCantidadSelect, "1 kg", "1kg");
            addOption(newCantidadSelect, "500 g", "500g");
            addOption(newCantidadSelect, "250 g", "250g");
            addOption(newCantidadSelect, "100 g", "100g");
            break;
        default:
            // Opciones por defecto
            addOption(newCantidadSelect, "1", "1");
            addOption(newCantidadSelect, "2", "2");
            addOption(newCantidadSelect, "3", "3");
            break;
    }
    newCantidadSelect.selectedIndex = 0;
}

// Función auxiliar para agregar opciones a un elemento select
function addOption(selectElement, text, value) {
    var option = document.createElement("option");
    option.text = text;
    option.value = value;
    selectElement.appendChild(option);
}

// Bloquear números negativos en el campo de precio
document.getElementById('newprecio').addEventListener('input', function () {
    if (this.value < 0) {
        this.value = '';
    }
});

// Bloquear números negativos en el campo de cantidad
document.getElementById('newcantidadInput').addEventListener('input', function () {
    if (this.value < 0) {
        this.value = '';
    }
});
