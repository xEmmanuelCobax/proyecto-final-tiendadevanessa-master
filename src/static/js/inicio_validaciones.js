// Función para reemplazar números por espacios (Compartido)
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


// ELIMINAR LOS ESPACIOS EN BLANCO DEL PRINCIPIO Y FINAL DE LOS INPUTS APELLIDOS Y NOMBRE (COMPARTIDO)
document.addEventListener("DOMContentLoaded", function () {
    // Función para eliminar espacios en blanco del inicio y final de campos específicos
    function trimInputFields() {
        var inputFields = document.querySelectorAll("#email, #password");
        inputFields.forEach(function (input) {
            input.value = input.value.trim();
        });
    }

    // Agregar solo el evento "blur" a los campos específicos
    var inputFields = document.querySelectorAll("#email, #password");
    inputFields.forEach(function (input) {
        input.addEventListener("blur", trimInputFields);
    });
});


// VALIDAR CONTRASEÑa
document.addEventListener("DOMContentLoaded", function () {
    var passwordField = document.getElementById("password");

    // Función de validación
    function validatePassword() {
        var value = passwordField.value;
        console.log("Contraseña ingresada:", value);

        // Validar el patrón: solo letras y números, longitud de 5 a 15 caracteres
        var isValid = /^[A-Za-z0-9]{5,15}$/.test(value);
        console.log("isValid:", isValid);

        // Muestra un mensaje si la contraseña es inválida
        if (!isValid) {
            passwordField.setCustomValidity("La contraseña debe contener solo letras y números, y tener entre 5 y 15 caracteres.");
        } else {
            passwordField.setCustomValidity(""); // Resetea el mensaje de error
        }

        // Opción para mostrar un mensaje visual si es inválido
        if (passwordField.checkValidity()) {
            passwordField.classList.remove('is-invalid'); // Remueve la clase de error si es válido
        } else {
            passwordField.classList.add('is-invalid'); // Agrega la clase de error si es inválido
        }
    }

    // Validar al escribir
    passwordField.addEventListener("input", validatePassword);

    // Validar al cambiar (incluye autocompletado)
    passwordField.addEventListener("blur", validatePassword);
});

// Función para alternar la visibilidad de la contraseña
function togglePassword() {
    var passwordField = document.getElementById("password");
    var eyeIcon = document.getElementById("eye-icon");
    if (passwordField.type === "password") {
        passwordField.type = "text"; // Cambia a texto
        eyeIcon.classList.remove("bi-eye-slash");
        eyeIcon.classList.add("bi-eye");
    } else {
        passwordField.type = "password"; // Cambia a contraseña
        eyeIcon.classList.remove("bi-eye");
        eyeIcon.classList.add("bi-eye-slash");
    }
}
