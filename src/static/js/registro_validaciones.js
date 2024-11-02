// SCRIPT PARA GENERAR CONTRASEÑAS SEGURAS
document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("generatePassword")
        .addEventListener("click", function () {
            var length = 10; // Longitud de la contraseña
            var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; // Solo letras y números
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
                passwordField.type = "password"; // Volver a cambiar el tipo de entrada a "password" después de 5 segundos
            }, 5000);
        });
});


//IMPEDIR CUALQUIER COSA QUE NO SE LETRA EN TIPOS TEXT
document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar los campos de entrada
    var nameInput = document.getElementById("name");
    var paternalLastNameInput = document.getElementById("apellidoPaterno");
    var maternalLastNameInput = document.getElementById("apellidoMaterno");

    // Función para limpiar el valor del campo
    function cleanInput(event) {
        this.value = this.value.replace(/[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g, ''); // Permite solo letras y espacios
    }

    // Asociar la función de limpieza a los eventos de entrada
    nameInput.addEventListener("input", cleanInput);
    paternalLastNameInput.addEventListener("input", cleanInput);
    maternalLastNameInput.addEventListener("input", cleanInput);
});


//CAMBIO AUTOMATICO PARA VER CONTRASEÑA EN PASSWORD
// document.addEventListener("DOMContentLoaded", function () {
//     var passwordField = document.getElementById("password");

//     // Cambia el tipo de campo a "text" al recibir el foco
//     passwordField.addEventListener("focus", function () {
//         passwordField.type = "text";
//     });

//     // Cambia el tipo de campo a "password" al perder el foco
//     passwordField.addEventListener("blur", function () {
//         passwordField.type = "password";
//     });

//     // Generar una contraseña al hacer clic en el botón de generación
//     document.getElementById("generatePassword").addEventListener("click", function () {
//         var length = 10; // Longitud de la contraseña
//         var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
//         var password = "";
//         for (var i = 0; i < length; i++) {
//             password += charset.charAt(Math.floor(Math.random() * charset.length));
//         }
//         passwordField.value = password;
//     });
// });


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



// MINIMO Y MAXIMO DE CARACTERES Y PATRON DE VALIDACION
document.addEventListener("DOMContentLoaded", function () {
    // Definir los máximos, mínimos de caracteres y el patrón para cada tipo de campo de entrada
    var charLimits = {
        "text": { min: 2, max: 20, pattern: /^[A-Za-z]{2,21}$/ },
        "email": { min: 2, max: 40, pattern: /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/ },
        "password": { min: 5, max: 15, pattern: /^[A-Za-z0-9]{6,16}$/ }
    };

    // Función para manejar el evento de entrada, limitar la longitud y validar el patrón
    function handleInput(event) {
        var inputType = event.target.type.toLowerCase();
        var value = event.target.value;

        // Limitar el número máximo de caracteres
        if (value.length > charLimits[inputType].max) {
            event.target.value = value.substring(0, charLimits[inputType].max);
        }

        // Validar el patrón y la longitud mínima
        if (!charLimits[inputType].pattern.test(value)) {
            event.target.setCustomValidity("El campo solo debe contener letras o numeros y tener entre " + charLimits[inputType].min + " y " + charLimits[inputType].max + " caracteres.");
        } else {
            event.target.setCustomValidity("");
        }
    }

    // Agregar evento de entrada a todos los campos de entrada
    var inputFields = document.querySelectorAll("input[type='text'], input[type='password']");
    inputFields.forEach(function (input) {
        input.addEventListener("input", handleInput);
    });
});

// EVITA EL USO DE ESPACIOS, COMILLAS SIMPLES Y DOBLES EN EL EMAIL Y EN EL PASSWORD 
document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los campos de entrada de tipo "text", "password" y "email"
    var inputFields = document.querySelectorAll("input[type='text'], input[type='password'], input[type='email']");

    // Función para limpiar el valor del campo según su tipo
    function cleanInput(event) {
        var inputType = event.target.type.toLowerCase();
        var inputValue = event.target.value;
        var cursorPosition = event.target.selectionStart; // Guarda la posición del cursor
        var cleanedValue;

        // Aplica el patrón de limpieza según el tipo de campo
        if (inputType === "password") {
            cleanedValue = inputValue.replace(/[^a-zA-Z0-9]/g, ""); // Letras y números para "password"
        } else { // Esta línea ha sido corregida
            cleanedValue = inputValue.replace(/[^\w\s@.]/g, ""); // Letras, números, "@", ".", y "_" para "email"
        }

        // Si el valor cambió, actualiza el campo y restaura el cursor
        if (inputValue !== cleanedValue) {
            event.target.value = cleanedValue;
            event.target.setSelectionRange(cursorPosition - 1, cursorPosition - 1); // Restaura la posición del cursor
        }
    }

    // Asocia la función de limpieza a todos los campos seleccionados
    inputFields.forEach(function (input) {
        input.addEventListener("input", cleanInput);
    });
});




// Validar la contraseña antes de enviar el formulario