// --VALIDA LOS ESPACIOS INICIALES Y FINALES QUE EL USUARIO PUEDA LLEGAR A PONER, Y QUE NO PUEDA COPIAR Y PEGARSE ESPACIOS-- >
  document.addEventListener("DOMContentLoaded", function () {
    var trimDelay = 500; // Cambia este valor según el tiempo que desees en milisegundos
    var timeout = null;

    // Función para eliminar espacios en blanco de los valores de los campos de entrada
    function trimInputFields() {
      var inputFields = document.querySelectorAll("input:not([type='number'])");
      inputFields.forEach(function (input) {
        input.value = input.value.trim();
      });
    }

    // Función para reiniciar el temporizador
    function resetTrimTimer() {
      clearTimeout(timeout);
      timeout = setTimeout(trimInputFields, trimDelay);
    }

    // Función para manejar el evento de pegar y eliminar espacios en blanco
    function handlePaste(event) {
      var paste = (event.clipboardData || window.clipboardData).getData("text");
      event.preventDefault();
      var trimmedPaste = paste.trim();
      document.execCommand("insertText", false, trimmedPaste);
      resetTrimTimer();
    }

    // Agregar eventos a todos los campos de entrada que no son de tipo "number"
    var inputFields = document.querySelectorAll("input:not([type='number'])");
    inputFields.forEach(function (input) {
      input.addEventListener("input", resetTrimTimer);
      input.addEventListener("change", resetTrimTimer);
      input.addEventListener("blur", resetTrimTimer);
      input.addEventListener("paste", handlePaste);
    });
  });

//--LIMITA EL NÚMERO DE CARACTERES DE LAS ENTRADAS-- >
  document.addEventListener("DOMContentLoaded", function () {
    var maxCharactersText = 25; // Máximo de caracteres para campos de texto
    var maxCharactersNumber = 10; // Máximo de caracteres para campos de número
    var maxCharactersSerach = 30;

    // Función para manejar el evento de entrada y limitar la longitud de los campos de entrada
    function handleInput(event) {
      if (
        event.target.type === "text" &&
        event.target.value.length > maxCharactersText
      ) {
        event.target.value = event.target.value.substring(0, maxCharactersText); // Limita a maxCharactersText para campos de texto
      } else if (
        event.target.type === "number" &&
        event.target.value.length > maxCharactersNumber
      ) {
        event.target.value = event.target.value.substring(
          0,
          maxCharactersNumber
        ); // Limita a maxCharactersNumber para campos de número
      } else if (
        event.target.type === "search" &&
        event.target.value.length > maxCharactersSerach
      ) {
        event.target.value = event.target.value.substring(0, maxCharactersSerach); // Limita a maxCharactersText para campos de texto
      }
    }

    // Agregar evento de entrada a todos los campos de entrada
    var inputFields = document.querySelectorAll("input");
    inputFields.forEach(function (input) {
      input.addEventListener("input", handleInput);
    });
  });

//--SOLO PERMITE AGREGAR UN UNICO ESPACIO EN TODOS LOS INPUTS-- >
  // Función para mantener solo un espacio entre palabras en los campos de entrada de texto
  function limitarEspacios(event) {
    // Obtener el valor actual del campo
    var valorCampo = event.target.value;
    // Reemplazar múltiples espacios por uno solo
    var valorSinEspaciosRepetidos = valorCampo.replace(/\s+/g, " ");
    // Actualizar el valor del campo con un solo espacio entre palabras
    event.target.value = valorSinEspaciosRepetidos;
  }

  // Seleccionar todos los campos de entrada de texto y textarea
  var inputspace = document.querySelectorAll(
    'input[type="text"], input[type="search"], input[type="password"], input[type="email"], input[type="number"], textarea'
  );

  // Agregar evento de escucha para cada campo de entrada
  inputspace.forEach(function (input) {
    input.addEventListener("input", limitarEspacios);
  });

//--EVITA EL USO DE COMILLAS EN TODOS LOS CAMPOS-- >
      // Función para eliminar comillas simples y dobles de todos los campos de entrada
        document.querySelectorAll("input").forEach(function (input) {
            input.addEventListener("input", function (event) {
                // Obtener el valor actual del campo de entrada
                var inputValue = event.target.value;
                // Eliminar comillas simples y comillas dobles del valor actual
                var cleanedValue = inputValue.replace(/['"]+/g, "");
                // Actualizar el valor del campo de entrada sin comillas simples y comillas dobles
                event.target.value = cleanedValue;
            });
  });
    