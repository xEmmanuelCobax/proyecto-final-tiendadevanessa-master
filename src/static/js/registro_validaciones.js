//  SCRIPT PARA GENERAR CONTRASEÑAS SEGURAS
document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("generatePassword")
        .addEventListener("click", function () {
            var length = 10; // Longitud de la contraseña
            var charset =
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#@"; // Caracteres para la contraseña
            var password = "";
            for (var i = 0; i < length; i++) {
                password += charset.charAt(
                    Math.floor(Math.random() * charset.length)
                );
            }
            var passwordField = document.getElementById("password");
            passwordField.value = password;
            passwordField.type = "text"; // Cambiar temporalmente el tipo de entrada a "text"
            setTimeout(function () {
                passwordField.type = "password"; // Volver a cambiar el tipo de entrada a "password" después de 3 segundos
            }, 5000);
        });
});


// EVITA EL USO DE ESPACIOS, COMILLAS SIMPLES Y DOBLES EN EL EMAIL Y EN EL PASSWORD
document.getElementById("password").addEventListener("input", function (event) {
    var passwordInput = event.target.value;
    var passwordCleaned = passwordInput.replace(/[^\w\s@.]/g, "");
    event.target.value = passwordCleaned;
});

document.getElementById("email").addEventListener("input", function (event) {
    var emailInput = event.target.value;
    var cursorPosition = event.target.selectionStart; // Guarda la posición del cursor
    var emailCleaned = emailInput.replace(/[^\w\s@.]/g, "");

    if (emailInput !== emailCleaned) {
        event.target.value = emailCleaned;
        event.target.setSelectionRange(cursorPosition - 1, cursorPosition - 1); // Restaura la posición del cursor
    }
});



// ELIMINAR LOS ESPACIOS EN BLANCO DEL PRINCIPIO Y FINAL DE LOS INPUTS APELLIDOS Y NOMBRE
document.addEventListener("DOMContentLoaded", function () {
    // Función para eliminar espacios en blanco del inicio y final de campos específicos
    function trimInputFields() {
        var inputFields = document.querySelectorAll("#name, #apellidoPaterno, #apellidoMaterno, #email, #password");
        inputFields.forEach(function (input) {
            input.value = input.value.trim();
        });
    }

    // Agregar solo el evento "blur" a los campos específicos
    var inputFields = document.querySelectorAll("#name, #apellidoPaterno, #apellidoMaterno, #email, #password");
    inputFields.forEach(function (input) {
        input.addEventListener("blur", trimInputFields);
    });
});



// LIMITA EL NÚMERO DE CARACTERES DE LAS ENTRADAS
document.addEventListener("DOMContentLoaded", function () {
    // Definir los máximos de caracteres para cada tipo de campo de entrada
    var maxCharacters = {
        "text": 30,
        "email": 40,
        "password": 15
    };

    // Función para manejar el evento de entrada y limitar la longitud de los campos de entrada
    function handleInput(event) {
        var inputType = event.target.type.toLowerCase();
        if (event.target.value.length > maxCharacters[inputType]) {
            event.target.value = event.target.value.substring(0, maxCharacters[inputType]); // Limita según el tipo de campo de entrada
        }
    }

    // Agregar evento de entrada a todos los campos de entrada
    var inputFields = document.querySelectorAll("input");
    inputFields.forEach(function (input) {
        input.addEventListener("input", handleInput);
    });
});


// Validar la contraseña antes de enviar el formulario