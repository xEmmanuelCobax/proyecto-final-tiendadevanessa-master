
// Seccion de modales para que todos las paginas pueden tener modales-- >
//MODALES PARA MOSTRAR FLASH-- >
<div class="modal fade" id="flashModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="flashModalLabel">Mensaje</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="flashModalBody">
            </div>
        </div>
    </div>
</div>


//MOSTRAR EL MODAL CON LOS FLASHES-- >
$(document).ready(function () {
    var flashMessages = $('#flash-messages').html().trim();
    if (flashMessages) {
        $('#flashModalBody').html(flashMessages); //mostrar en el body
        $('#flashModal').modal('show');
    }
});


