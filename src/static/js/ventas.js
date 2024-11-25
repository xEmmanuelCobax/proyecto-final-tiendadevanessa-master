
function sumTableNumbers() {
    let table = document.getElementById("saleTable");
    let rows = table.getElementsByTagName("tr");
    let total = 0.0;

    // Crear un array para almacenar los subtotales de cada producto
    let subtotals = [];

    // Iterar sobre las filas y calcular los subtotales de cada producto
    for (let i = 1; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName("td");
        if (cells.length > 0) {
            let price = parseFloat(cells[3].innerText);
            let quantity = parseFloat(cells[2].querySelector("input").value);
            let subtotal = price * quantity;
            subtotals.push(subtotal);
        }
    }

    const inputElement = document.getElementById('paymentInput');
    const inputValue = inputElement.value;
    // console.log(inputValue);

    // Sumar todos los subtotales para obtener el subtotal total
    let subtotal = subtotals.reduce((acc, val) => acc + val, 0);

    // Calcular el total con IVA
    let totalWithIVA = (subtotal * 1.16).toFixed(2);

    // Calcular el total de la compra
    let totalTotalWithIVA = (subtotal * 1.16).toFixed(2);



    if (inputValue === "") {
        var cambiocliente = 0.0;
    } else {
        var cambiocliente = (inputValue - totalTotalWithIVA);
    }

    cambiocliente = cambiocliente.toFixed(2);

    // Actualizar los elementos HTML con los resultados
    document.getElementById("totalSum").innerText =
        "Subtotal: " + subtotal.toFixed(2) + "$";
    document.getElementById("totalSumIVA").innerText =
        "Total de la compra con IVA: " + totalWithIVA + "$";
    document.getElementById("totalSumALL").innerText =
        "Total de la compra: " + totalTotalWithIVA + "$";
    document.getElementById("cambiocliente").innerText =
        "Cambio a entregar: " + cambiocliente + "$";

}



// Crear un MutationObserver para observar cambios en el tbody de la tabla
const targetNode = document.querySelector("#saleTable tbody");
const config = {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
};


const callback = function (mutationsList, observer) {
    for (const mutation of mutationsList) {
        if (
            mutation.type === "childList" ||
            mutation.type === "characterData" ||
            mutation.type === "attributes"
        ) {
            sumTableNumbers(); // Llamar a sumTableNumbers en cada mutación observada
        }
    }
};

const observer = new MutationObserver(callback);
observer.observe(targetNode, config);

// Observar cambios en los inputs de cantidad específicamente
const inputElements = document.querySelectorAll(
    "#saleTable tbody tr td:nth-child(3) input"
);
inputElements.forEach((input) => {
    input.addEventListener("input", sumTableNumbers);
});

function updateTotal() {
    // Mostrar el spinner
    document.getElementById("spinner-total").classList.remove("d-none");

    // Llamar a la función sumTableNumbers después de un pequeño retraso para simular el tiempo de procesamiento
    setTimeout(function () {
        sumTableNumbers();

        // Ocultar el spinner después de que se completen los cálculos
        document.getElementById("spinner-total").classList.add("d-none");
    }, 500); // Puedes ajustar este valor según sea necesario
}

// Ejecutar la función al hacer clic en el botón
document
    .getElementById("updateTotalButton")
    .addEventListener("click", function () {
        updateTotal();
    });

// Ejecutar la función automáticamente cada 1 segundo
setInterval(updateTotal, 500);

// Llamar a la función para calcular la suma cuando se carga la página
window.onload = sumTableNumbers;

function validateInput() {
    let table = document.getElementById("saleTable");
    let rows = table.getElementsByTagName("tr");
    let total = 0.0;

    // Crear un array para almacenar los subtotales de cada producto
    let subtotals1 = [];

    // Iterar sobre las filas y calcular los subtotales de cada producto
    for (let i = 1; i < rows.length; i++) {
        let cells = rows[i].getElementsByTagName("td");
        if (cells.length > 0) {
            let price = parseFloat(cells[3].innerText);
            let quantity = parseFloat(cells[2].querySelector("input").value);
            let subtotal = price * quantity;
            subtotals1.push(subtotal);
        }
    }

    // Sumar todos los subtotales para obtener el subtotal total
    let subtotal = subtotals1.reduce((acc, val) => acc + val, 0);

    // Calcular el total con IVA
    let totalWithIVA = (subtotal * 1.16).toFixed(2);

    // Calcular el total de la compra
    let totalTotalWithIVA = (subtotal * 1.16).toFixed(2);

    const addSaleButton = document.getElementById('addSale');
    const inputElement = document.getElementById('paymentInput');
    const inputValue = parseFloat(inputElement.value);
    console.log("Botón addSale:", addSaleButton);
    console.log("Valor ingresado:", inputValue);
    console.log("Valor ingresado2:", totalTotalWithIVA);
    if (inputValue < totalTotalWithIVA) {
        // Muestra el mensaje de advertencia
        // showToast("Por favor, ingrese un valor mayor al de la venta.", "warning");

        // Deshabilita el botón si la condición no se cumple
        addSaleButton.disabled = true;
        console.log("Botón deshabilitado");

    } else if (inputValue > totalTotalWithIVA && totalTotalWithIVA > 0) {
        // Habilita el botón si la condición se cumple
        addSaleButton.disabled = false;
        console.log("Botón habilitado");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const tooltipTriggerList = document.querySelectorAll(
        '[data-bs-toggle="tooltip"]'
    );
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        const tooltip = new bootstrap.Tooltip(tooltipTriggerEl);
        tooltipTriggerEl.addEventListener("click", function () {
            // Cerrar el tooltip al hacer clic en el elemento
            tooltip.hide();
        });
        tooltipTriggerEl.addEventListener("mouseleave", function () {
            // Cerrar el tooltip cuando el mouse sale del elemento
            tooltip.hide();
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var maxCharactersText = 35; // Máximo de caracteres para campos de texto
    var maxCharactersNumber = 6; // Máximo de caracteres para campos de número

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
        }
    }

    // Agregar evento de entrada a todos los campos de entrada
    var inputFields = document.querySelectorAll("input");
    inputFields.forEach(function (input) {
        input.addEventListener("input", handleInput);
    });
});

// VALIDA EL NULO INGRESO DE OPERADORES EN LOS INPUTS DE TIPO NUMERO-->
document.addEventListener("DOMContentLoaded", function () {
    // Función para prevenir caracteres no numéricos y operadores en inputs de tipo number
    function preventInvalidChars(event) {
        if (
            event.target.type === "number" &&
            (event.key === "e" ||
                event.key === "E" ||
                event.key === "-" ||
                event.key === "+"
            )
        ) {
            event.preventDefault();
        }
    }

    // Agregar evento solo a los campos de entrada de tipo number
    var numberFields = document.querySelectorAll("input[type='number']");
    numberFields.forEach(function (input) {
        input.addEventListener("keydown", preventInvalidChars);
    });
});

// SCRIPT PARA MOSTRAR CORRECTAMENTE LOS NOMBRES -->
// Reemplazar guiones bajos "_" por espacios en blanco en los nombres de productos
document.querySelectorAll(".product-name").forEach(function (element) {
    element.innerText = element.innerText.replace(/_/g, " ");
});

//EVITA EL USO DE COMILLAS EN TODOS LOS CAMPOS-->
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

// MUESTA MENSAJE DE BOTONES Y LISTA VACIOS (AS)-->
document.addEventListener("DOMContentLoaded", function () {
    // Verificar si el contenedor de botones está vacío
    const buttonsContainer = document.querySelector(".buttons");
    if (!buttonsContainer || buttonsContainer.children.length === 0) {
        const emptyButtonsMessage = document.createElement("p");
        emptyButtonsMessage.textContent = "Lista de elementos vacía.";
        buttonsContainer.appendChild(emptyButtonsMessage);
    }
});

// SCRIPT PARA AGREGAR PRODUCTOS A LA TABLA MEDIANTE LA BARRA DE BUSQUEDA O LOS BOTONES -->
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".product-btn");
    const tableBody = document.querySelector(".table-group-divider");
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");
    const addButton = document.getElementById("addButton");
    let selectedProduct = null;

    // Función para agregar un producto a la tabla
    function addProductToTable(productInfo) {
        const existingProduct = Array.from(tableBody.querySelectorAll("tr")).find(
            (row) => row.dataset.id === productInfo[0]
        );

        if (existingProduct) {
            showToast("El producto ya está en la tabla.", "error");
            return;
        }

        if (parseInt(productInfo[2]) <= 0) {
            showToast(
                "No hay suficientes existencias para agregar este producto.",
                "error"
            );
            return;
        }

        const newRow = document.createElement("tr");
        newRow.dataset.id = productInfo[0];
        newRow.innerHTML = `
        <th scope="row" style="text-align: center; margin: auto;">${tableBody.querySelectorAll("tr").length + 1
            }</th>
        <td style="text-align: center; margin: auto;">${productInfo[0]}</td>
        <td>${productInfo[1]}</td>
        <td style="text-align: center;">
          <input type="number" class="form-control" value="1" min="1" max="${productInfo[2]
            }" onkeydown="return false" onpaste="return false" onfocus="this.blur();" style="background: transparent; border: none; padding: 0; width: 80px; font-size: 17px; text-align: center; margin: auto;" />
        </td>
        <td style="text-align: center; margin: auto;">${productInfo[3]}$</td>
        <td class="text-center d-flex justify-content-center align-items-center">
          <button id="deletebotton" type="button" class="btn btn-danger mx-2" onclick="confirmDelete(this)">
      <span class="material-symbols-outlined"> delete_forever </span>
    </button>
        </td>
      `;

        tableBody.appendChild(newRow);
    }

    // Event listener para los botones de productos
    buttons.forEach((button, index) => {
        button.addEventListener("click", function () {
            const productInfo = [
                this.dataset.id,
                this.dataset.name,
                this.dataset.amount,
                this.dataset.price,
            ];
            addProductToTable(productInfo);
        });
    });

    // Event listener para el campo de búsqueda
    searchInput.addEventListener("input", function () {
        const searchTerm = this.value.toLowerCase();
        const matchingProducts = Array.from(buttons).filter((button) =>
            button.dataset.name.toLowerCase().includes(searchTerm)
        );

        searchResults.innerHTML = "";

        matchingProducts.forEach((product) => {
            const listItem = document.createElement("div");
            listItem.classList.add("dropdown-item");
            listItem.innerHTML = `
          <div class="product-info border-bottom border-2 border-gray desc-inventario">
            
            <div>Nombre: ${product.dataset.name}</div>
            <div>Precio: $${product.dataset.price}</div>
            <div>Stock: ${product.dataset.amount}</div>
          </div>
        `;
            listItem.addEventListener("click", function () {
                searchResults.querySelectorAll(".dropdown-item").forEach((item) => {
                    item.classList.remove("selected");
                });
                listItem.classList.add("selected");
                selectedProduct = product;
            });
            searchResults.appendChild(listItem);
        });

        searchResults.style.display =
            matchingProducts.length > 0 ? "block" : "none";
    });

    // Cerrar el menú de búsqueda y limpiar el campo de búsqueda cuando se hace clic fuera de él
    document.addEventListener("click", function (event) {
        if (
            !searchResults.contains(event.target) &&
            event.target !== searchInput
        ) {
            searchResults.style.display = "none";
            selectedProduct = null;
            searchInput.value = ""; // Limpiar el contenido del campo de búsqueda
        }
    });

    // Event listener para el botón de agregar
    addButton.addEventListener("click", function () {
        if (!selectedProduct) {
            showToast("No hay ningún producto seleccionado.", "warning");
            return;
        }
        addProductToTable([
            selectedProduct.dataset.id,
            selectedProduct.dataset.name,
            selectedProduct.dataset.amount,
            selectedProduct.dataset.price,
        ]);
    });
});

// Variable para almacenar el botón que fue presionado
let buttonToDelete;

function confirmDelete(button) {
    // Almacenar el botón que fue presionado
    buttonToDelete = button;
    // Mostrar el modal de confirmación
    $('#deleteConfirmationModal').modal('show');
}

document.getElementById('confirmDelete').addEventListener('click', function () {
    // Si se confirma, eliminar el producto
    deleteProduct(buttonToDelete);
    // Cerrar el modal
    $('#deleteConfirmationModal').modal('hide');
});

function deleteProduct(button) {
    const row = button.closest("tr");
    row.remove();
}

// Función para mostrar toasts personalizados
function showToast(message, type) {
    const toastContainer = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.classList.add("show");
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");
    toast.setAttribute("data-bs-autohide", "true");

    // Obtener la hora actual
    const currentTime = new Date().toLocaleTimeString();

    toast.innerHTML = `
      <div class="toast-header">
        <i class="fas fa-exclamation-circle"></i>
        <strong class="me-auto mx-2">Warning!</strong>
        <small>${currentTime}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body mt-1">
        ${message}
      </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", function () {
        toast.remove();
    });
}

//SCRIPT PARA ENVIAR LOS DATOS AL SERVIDOR -->
document.getElementById("addSale").addEventListener("click", function () {
    const salesData = obtenerDatosTabla(); // Función para obtener los datos de la tabla

    // Verificar si la tabla está vacía
    if (salesData.length === 0) {
        showToast(
            "La tabla está vacía. Por favor, agregue productos antes de realizar una venta.",
            "warning"
        );
        return;
    }


    // Mostrar el spinner de carga
    document.getElementById("spinner-container").style.display = "flex";

    const xhr = new XMLHttpRequest();
    const url = "/sales/addsalesworker";
    const method = "POST";

    xhr.open(method, url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
        // Ocultar el spinner de carga después de la respuesta
        document.getElementById("spinner-container").style.display = "none";

        if (xhr.status === 200) {
            console.log("Success:", xhr.responseText);
            showToastSuccess("Venta realizada con éxito.");
            setTimeout(() => {
                location.reload(); // Recargar la página después de 1 segundo
            }, 1000); // 1000 milisegundos = 1 segundo
        } else {
            console.error("Error:", xhr.statusText);
            let errorMessage = "Ha ocurrido un error.";

            // Si el servidor responde con un mensaje de error más específico
            if (xhr.responseText) {
                try {
                    const responseJson = JSON.parse(xhr.responseText);
                    errorMessage = responseJson.message || errorMessage;
                } catch (e) {
                    errorMessage = "Error inesperado al procesar la venta.";

                }
                setTimeout(() => {
                    location.reload(); // Recargar la página después de 1 segundo
                }, 1000);

            }

            showToast(errorMessage, "danger");
        }
    };
    xhr.onerror = function () {
        console.error("Error:", xhr.statusText);
        showToast("Error de conexión. Intente nuevamente.", "danger");
    };
    xhr.send(JSON.stringify(salesData));
});

function obtenerDatosTabla() {
    const rows = document.querySelectorAll("#saleTable tbody tr");
    const salesData = [];

    rows.forEach((row) => {
        const dataId = row.getAttribute("data-id");
        const cells = row.querySelectorAll("td");
        const rowData = { id: dataId };

        cells.forEach((cell, index) => {
            let cellValue;
            if (cell.querySelector("input")) {
                cellValue = cell.querySelector("input").value;
            } else {
                cellValue = cell.textContent.trim();
            }

            switch (index) {
                case 2: // Quantity is in the 3rd column (index 2)
                    rowData.quantity = cellValue;
                    break;
                case 3: // Name is in the 4th column (index 3)
                    rowData.productName = cellValue;
                    break;
                case 4: // Price is in the 5th column (index 4)
                    rowData.price = cellValue;
                    break;
            }
        });

        salesData.push(rowData);
    });
    return salesData;
}

// Función para mostrar toasts personalizados
function showToast(message, type) {
    const toastContainer = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.classList.add("show");
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");
    toast.setAttribute("data-bs-autohide", "true");

    // Obtener la hora actual
    const currentTime = new Date().toLocaleTimeString();

    toast.innerHTML = `
      <div class="toast-header">
        <i class="fas fa-exclamation-circle"></i>
        <strong class="me-auto mx-2">Warning!</strong>
        <small>${currentTime}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body mt-1">
        ${message}
      </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", function () {
        toast.remove();
    });
}

// Función para mostrar toasts de éxito
function showToastSuccess(message) {
    const toastContainer = document.getElementById("toastContainerSuccess");
    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.classList.add("show");
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");
    toast.setAttribute("data-bs-autohide", "true");

    // Obtener la hora actual
    const currentTime = new Date().toLocaleTimeString();

    toast.innerHTML = `
      <div class="toast-header">
        <i class="fas fa-check-circle"></i>
        <strong class="me-auto mx-2">Success!</strong>
        <small>${currentTime}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body mt-1">
        ${message}
      </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", function () {
        toast.remove();
    });
}




//MOSTRAR EL MODAL PARA MOSTRAR ERRORES Y MENSAJES  -->
$(document).ready(function () {
    var flashMessages = $('#flash-messages').html().trim();
    if (flashMessages) {
        $('#flashModalBody').html(flashMessages);
        $('#flashModal').modal('show');
    }
});