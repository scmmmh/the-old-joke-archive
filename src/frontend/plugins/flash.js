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
