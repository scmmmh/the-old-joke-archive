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
 * Plugin that creates a popup when the user clicks on the image in the snippet.
 */
(function() {
    let body = document.querySelector('body');

    function setup_anchor(anchor) {
        anchor.addEventListener('click', function(ev) {
            ev.preventDefault();
            let wrapper = document.createElement('div');
            wrapper.classList.add('image-popup');
            let popup = document.createElement('div');
            popup.classList.add('content');
            wrapper.appendChild(popup);
            let link = document.createElement('a');
            link.setAttribute('href', anchor.getAttribute('href'));
            popup.appendChild(link);
            let srcImg = anchor.querySelector('img');
            if(srcImg) {
                let image = document.createElement('img');
                image.setAttribute('src', srcImg.getAttribute('src'));
                link.appendChild(image);
            }
            body.appendChild(wrapper);
            wrapper.addEventListener('click', function(ev) {
                wrapper.remove();
            });
        });
    }

    let anchors = document.querySelectorAll('a[data-action="image-popup"]');
    for(let idx = 0; idx < anchors.length; idx++) {
        setup_anchor(anchors[idx]);
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
