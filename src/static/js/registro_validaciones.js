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


//IMPEDIR CUALQUIER COSA QUE NO SE LETRA EN TIPOS TEXT (numeros)
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
document.addEventListener("DOMContentLoaded", function () {
    var passwordField = document.getElementById("password");

    // Cambia el tipo de campo a "text" al recibir el foco
    passwordField.addEventListener("focus", function () {
        passwordField.type = "text";
    });

    // Cambia el tipo de campo a "password" al perder el foco
    passwordField.addEventListener("blur", function () {
        passwordField.type = "password";
    });

    // Generar una contraseña al hacer clic en el botón de generación
    document.getElementById("generatePassword").addEventListener("click", function () {
        var length = 10; // Longitud de la contraseña
        var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        var password = "";
        for (var i = 0; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        passwordField.value = password;
    });
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




// LIMITAR NOMBRES Y VALIDAR
document.addEventListener("DOMContentLoaded", function () {
    // Selecciona los campos a validar
    const fields = [
        document.getElementById("name"),
        document.getElementById("apellidoPaterno"),
        document.getElementById("apellidoMaterno")
    ];

    // Función de validación y limitación de caracteres
    function validateField(field) {
        const value = field.value;
        const isValid = /^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{2,20}$/.test(value);

        // Limitar la longitud del input
        if (value.length > 20) {
            field.value = value.substring(0, 20); // Limita a 20 caracteres
        }

        // Validar el patrón
        if (!isValid) {
            field.setCustomValidity("Debe tener entre 2 y 20 caracteres y solo contener letras.");
            field.classList.add("is-invalid");
        } else {
            field.setCustomValidity("");
            field.classList.remove("is-invalid");
        }
    }

    // Agregar el evento "input" a cada campo
    fields.forEach(function (field) {
        field.addEventListener("input", function () {
            validateField(field);
        });
    });
});


//LIMITAR CORREO Y CONTRASEÑA Y VALIDARLOS
document.addEventListener("DOMContentLoaded", function () {
    // Selecciona los campos a validar
    const emailField = document.getElementById("email");
    const passwordField = document.getElementById("password");

    // Función de validación y limitación de caracteres
    function validateEmail() {
        const value = emailField.value;
        // Limitar la longitud del input
        if (value.length > 40) {
            emailField.value = value.substring(0, 40); // Limita a 40 caracteres
        }

        // Validar el formato del email
        const isValid = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value);
        if (!isValid) {
            emailField.setCustomValidity("Por favor, ingresa un correo electrónico válido.");
            emailField.classList.add("is-invalid");
        } else {
            emailField.setCustomValidity("");
            emailField.classList.remove("is-invalid");
        }
    }

    function validatePassword() {
        const value = passwordField.value;

        // Limitar la longitud del input
        if (value.length > 20) {
            passwordField.value = value.substring(0, 20); // Limita a 20 caracteres
        }

        // Validar que la contraseña no esté vacía y cumpla con los requisitos de longitud
        if (value.length < 5) {
            passwordField.setCustomValidity("La contraseña debe tener al menos 5 caracteres.");
            passwordField.classList.add("is-invalid");
        }
        // Validar que solo contenga letras y números
        else if (!/^[a-zA-Z0-9]+$/.test(value)) {
            passwordField.setCustomValidity("La contraseña solo puede contener letras y números.");
            passwordField.classList.add("is-invalid");
        }
        // Si cumple con todos los requisitos, se considera válida
        else {
            passwordField.setCustomValidity("");
            passwordField.classList.remove("is-invalid");
        }
    }


    // Agregar el evento "input" a cada campo
    emailField.addEventListener("input", validateEmail);
    passwordField.addEventListener("input", validatePassword);
});


