
// ontener los id
function setIntermediaryId(IntermediaryId) {
    document.getElementById("ValueIntermediaryId").value = IntermediaryId;

    console.log("IntermediaryId BORRAR>" + IntermediaryId);
}

function setEditProductId(IntermediaryId, accountname, PAT, MAT, CORREO) {
    document.getElementById("EditValueIntermediary_id").value = IntermediaryId;
    document.getElementById("editIntermediaryName").value = accountname;
    document.getElementById("NEW-AP_PAT").value = PAT;
    document.getElementById("NEW-AP_MAT").value = MAT;
    document.getElementById("NEW-Correo").value = CORREO;
    console.log("EditIntermediary_id EDITAR>" + IntermediaryId);

    // Encuentra la fila con el data-relation-id correspondiente
    var table = document.getElementById("intermedaries-table");
    var rows = table.getElementsByTagName("tr");
    var foundRow = null;
    for (var i = 0; i < rows.length; i++) {
        var rowRelationId = rows[i].getAttribute("data-relation-id");
        if (rowRelationId === IntermediaryId) {
            foundRow = rows[i];
            break;
        }
    }

    if (foundRow) {
        console.log("Se encontró la fila con data-relation-id =", IntermediaryId);
        // Obtiene todos los datos de las celdas en la fila
        var rowData = Array.from(foundRow.children).map((cell) =>
            cell.textContent.trim()
        );

        //var idIntermedary = rowData[0];}

        //SELECCIONA LA COMPAÑIA PARA CARGARLA
        var companyName = rowData[1];
        // Obtener el elemento select
        var selectElement = document.getElementById("company-select2");

        // Iterar sobre las opciones del elemento select
        for (var i = 0; i < selectElement.options.length; i++) {
            var option = selectElement.options[i];
            console.log("Opción", i, "Valor:", option.value, "Texto:", option.text);
            // Verificar si el texto de la opción coincide con el nombre de la empresa
            if (option.text === companyName) {
                // Establecer el valor del elemento select a la opción correspondiente
                selectElement.selectedIndex = i;
                console.log("Opción seleccionada de compañia:", option.text);
                // Opcionalmente, puedes salir del bucle si solo quieres seleccionar la primera coincidencia
                // break;
            }
        }
        //FIN

        var intermedaryName = rowData[2].replace(/\s+/g, " ").trim();
        console.log(intermedaryName);
        document.getElementById("editIntermediaryName").value = intermedaryName;

        var telPhone = rowData[3];
        document.getElementById("editIntermediaryPhone").value = telPhone;

        var tostada = new bootstrap.Toast(document.getElementById("toast"));
        tostada.show();
    } else {
        console.log("No se encontro la fila.");
    }
}

