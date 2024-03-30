(function($) {
    'use strict';
    //nav-link active

    $(".nav-link").click(e => {
        e.stopPropagation();
        e.preventDefault();
        const url = $(e.target).attr("href")
        window.location.href = url
    })




})(jQuery);