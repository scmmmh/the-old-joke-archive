/**
 * Plugin that sets a hidden action field on a form, based on the data-action of buttons in the form.
 */
(function() {
    function setup_form(form) {
        let action = form.querySelector('input[name="action"]');
        if (action) {
            let buttons = form.querySelectorAll('button[data-action]');
            for(let idx = 0; idx < buttons.length; idx++) {
                let button = buttons[idx];
                button.addEventListener('click', (ev) => {
                    if(button.getAttribute('data-confirm-prompt')) {
                        if(confirm(button.getAttribute('data-confirm-prompt'))) {
                            action.setAttribute('value', button.getAttribute('data-action'));
                        } else {
                            ev.preventDefault();
                        }
                    } else {
                        action.setAttribute('value', button.getAttribute('data-action'));
                    }
                });
            }
        }
    }

    let forms = document.querySelectorAll('form[data-action="action-buttons"]');
    for(let idx = 0; idx < forms.length; idx++) {
        setup_form(forms[idx]);
    }
})();
