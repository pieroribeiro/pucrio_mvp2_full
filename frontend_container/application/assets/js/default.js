(function($) {
    'use strict';

    $(".nav-link").click(e => {
        e.stopPropagation();
        e.preventDefault();
        const url = $(e.target).attr("href")
        window.location.href = url
    })

})(jQuery);

function showAlert(message, type) {
    const alertElement = $('#alert')
    alertElement.children("#message").addClass(`alert-${type}`).append(message)
    alertElement.alert()

    setTimeout(() => {
        $("#alert #message").empty().removeClass().addClass("alert")
        alertElement.alert("close")
    }, 5000)
}
