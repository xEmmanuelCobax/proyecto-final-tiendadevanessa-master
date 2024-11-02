// SCRIPT PARA VALIDACIÓN Y GENERACIÓN DE CAMPOS
document.addEventListener("DOMContentLoaded", function () {
    const nameInput = document.getElementById("name");
    const paternalLastNameInput = document.getElementById("apellidoPaterno");
    const maternalLastNameInput = document.getElementById("apellidoMaterno");
    const emailField = document.getElementById("email");
    const passwordField = document.getElementById("password");
    const generatePasswordButton = document.getElementById("generatePassword");

    // Generar contraseña segura
    function generatePassword() {
        const length = 10;
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        let password = "";
        for (let i = 0; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        passwordField.value = password;
        passwordField.type = "text";
        setTimeout(() => passwordField.type = "password", 5000); // Volver a "password" en 5 segundos
    }

    // Validar nombre y apellidos (solo letras y espacios)
    function validateTextInput(field) {
        const value = field.value;
        const isValid = /^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{2,20}$/.test(value);
        field.value = value.replace(/[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g, '').substring(0, 20);

        if (!isValid) {
            field.setCustomValidity("Debe tener entre 2 y 20 caracteres y solo contener letras.");
            field.classList.add("is-invalid");
        } else {
            field.setCustomValidity("");
            field.classList.remove("is-invalid");
        }
    }

    // Validar correo electrónico
    function validateEmail() {
        const value = emailField.value;
        const isValid = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value);
        emailField.value = value.substring(0, 40);

        if (!isValid) {
            emailField.setCustomValidity("Por favor, ingresa un correo electrónico válido.");
            emailField.classList.add("is-invalid");
        } else {
            emailField.setCustomValidity("");
            emailField.classList.remove("is-invalid");
        }
    }

    // Validar contraseña (con soporte para autocompletado)
    function validatePassword() {
        const value = passwordField.value;
        passwordField.value = value.substring(0, 20);

        if (value.length < 5) {
            passwordField.setCustomValidity("La contraseña debe tener al menos 5 caracteres.");
            passwordField.classList.add("is-invalid");
        } else if (!/^[a-zA-Z0-9]+$/.test(value)) {
            passwordField.setCustomValidity("La contraseña solo puede contener letras y números.");
            passwordField.classList.add("is-invalid");
        } else {
            passwordField.setCustomValidity("");
            passwordField.classList.remove("is-invalid");
        }
    }

    // Quitar espacios en blanco al principio y al final
    function trimInputFields() {
        [nameInput, paternalLastNameInput, maternalLastNameInput, emailField, passwordField].forEach(input => {
            input.value = input.value.trim();
        });
    }

    // Detectar cambios en el valor de la contraseña (para autocompletado)
    setInterval(validatePassword, 500);

    // Mostrar contraseña al hacer foco y ocultarla al salir
    passwordField.addEventListener("focus", () => passwordField.type = "text");
    passwordField.addEventListener("blur", () => passwordField.type = "password");

    // Asignar eventos
    generatePasswordButton.addEventListener("click", generatePassword);
    nameInput.addEventListener("input", () => validateTextInput(nameInput));
    paternalLastNameInput.addEventListener("input", () => validateTextInput(paternalLastNameInput));
    maternalLastNameInput.addEventListener("input", () => validateTextInput(maternalLastNameInput));
    emailField.addEventListener("input", validateEmail);
    passwordField.addEventListener("input", validatePassword);

    [nameInput, paternalLastNameInput, maternalLastNameInput, emailField, passwordField].forEach(input => {
        input.addEventListener("blur", trimInputFields);
    });
});
