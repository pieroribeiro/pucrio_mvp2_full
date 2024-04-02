function showAlert(message, type) {
    $('#alertContainer').prepend(`<div class="alert alert-${type} fade show" role="alert"><strong>Atenção!</strong> <span class="message">${message}</span></div>`)

    setTimeout(() => {
        $(".alert").alert('close')
    }, 5000)
}
