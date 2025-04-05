// Configura la conexión con el servidor
const socket = io();

// Función para manejar clic en "Editar"
function startEditing(userId, pageId) {
    socket.emit('start_editing', { user_id: userId, page_id: pageId });
}

// Función para manejar clic en "Terminar Edición"
function stopEditing(userId) {
    socket.emit('stop_editing', { user_id: userId });
}

// Bloqueo de la edición para otros usuarios
socket.on('lock_page', (data) => {
    if (data.page_id === 'page1') { // Asegúrate de validar la página actual
        document.getElementById('editor').disabled = true;
        document.getElementById('edit-btn').disabled = true;
        alert('La página está siendo editada por otro usuario.');
    }
});

// Desbloqueo de la edición
socket.on('unlock_page', () => {
    document.getElementById('editor').disabled = false;
    document.getElementById('edit-btn').disabled = false;
    alert('La página está disponible para editar.');
});

// Manejo de errores al editar
socket.on('editing_error', (data) => {
    alert(data.message);
});