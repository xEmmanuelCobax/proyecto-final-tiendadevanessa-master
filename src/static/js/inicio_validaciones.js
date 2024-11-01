// Función para reemplazar números por espacios
function replaceNumbersWithSpaces(event) {
    // Reemplaza los números por espacios en el valor del input
    event.target.value = event.target.value.replace(/[0-9]/g, ' ');
}

// Selecciona todos los inputs que deseas modificar
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[type="text"]');

    // Añadir el evento oninput a cada input
    inputs.forEach(input => {
        input.addEventListener('input', replaceNumbersWithSpaces);
    });
});
