/**
 * Plugin that handles closing the flash messages.
 */
(function() {
    let flash = document.querySelector('.flash');
    if (flash) {
        function setup_message(message) {
            message.addEventListener('click', function() {
                message.parentElement.remove();
                if (list.children.length == 0) {
                    flash.remove();
                }
            });
        }

        let list = flash.querySelector('ul');
        let messages = flash.querySelectorAll('[data-action="close-message"]');
        for (let idx = 0; idx < messages.length; idx++) {
            setup_message(messages[idx]);
        }
    }
})();

/**
 * Plugin that posts the URL of a link, instead of the default GET action.
 */
(function() {
    function setup_anchor(anchor) {
        anchor.addEventListener('click', function(ev) {
            ev.preventDefault();
            if(anchor.getAttribute('data-confirm-prompt')) {
                if(confirm(anchor.getAttribute('data-confirm-prompt'))) {
                    let form = document.createElement('form');
                    form.setAttribute('action', anchor.getAttribute('href'));
                    form.setAttribute('method', 'post');
                    anchor.append(form);
                    form.submit();
                }
            } else {
                let form = document.createElement('form');
                form.setAttribute('action', anchor.getAttribute('href'));
                form.setAttribute('method', 'post');
                anchor.append(form);
                form.submit();
            }
        });
    }

    let anchors = document.querySelectorAll('a[data-action="post-link"]');
    for(let idx = 0; idx < anchors.length; idx++) {
        setup_anchor(anchors[idx]);
    }
})();
