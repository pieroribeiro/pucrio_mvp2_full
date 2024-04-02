function showAlert(message, type) {
    $('#alertContainer').prepend(`<div class="alert alert-${type} alert-dismissible fade show" role="alert"><strong>Atenção!</strong> <span class="message">${message}</span><button type="button" style="float: right;" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>`)

    $('.alert button').on('click', () => {
        $(".alert").alert('close')
    })
    


    // alert.close()
    // const alertElement = $('#alert')
    // alertElement.children("#message").addClass(`alert-${type}`).append(message)
    // alertElement.alert()

    // setTimeout(() => {
    //     $("#alert #message").empty().removeClass().addClass("alert")
    //     alertElement.alert("close")
    // }, 5000)
}

showAlert('Testando mensagem', 'warning')
