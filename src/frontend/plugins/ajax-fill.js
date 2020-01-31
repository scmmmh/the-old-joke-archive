/**
 * Plugin that handles filling parts of the page via ajax.
 */
(function() {
    const ajaxFillers = document.querySelectorAll('[data-ajax-fill]');
    if (ajaxFillers) {
        for (let idx = 0; idx < ajaxFillers.length; idx++) {
            const ajaxFill = ajaxFillers[idx];
            window.fetch(ajaxFill.getAttribute('data-ajax-fill')).then((response) => {
                response.text().then((data) => {
                    ajaxFill.innerHTML = data;
                });
            });
        }
    }
})();
