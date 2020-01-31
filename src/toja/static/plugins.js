/**
 * Plugin that handles filling parts of the page via ajax.
 */
(function() {
    function fetchData(ajaxFiller) {
        window.fetch(ajaxFiller.getAttribute('data-ajax-fill')).then((response) => {
            response.text().then((data) => {
                ajaxFiller.removeAttribute('data-ajax-fill');
                ajaxFiller.innerHTML = data;
                plugins.imagePopup();
            });
        });
    }

    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.ajaxFill = function() {
        const ajaxFillers = document.querySelectorAll('[data-ajax-fill]');
        if (ajaxFillers) {
            for (let idx = 0; idx < ajaxFillers.length; idx++) {
                const ajaxFill = ajaxFillers[idx];
            }
        }
    };

    plugins.ajaxFill();
})();

/**
 * Plugin that handles closing the flash messages.
 */
(function() {
    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.flash = function() {
        let flash = document.querySelector('.flash');
        if (flash) {
            function setup_message(message) {
                if (!message.getAttribute('data-action-close-message')) {
                    message.addEventListener('click', function() {
                        message.parentElement.remove();
                        if (list.children.length == 0) {
                            flash.remove();
                        }
                    });
                }
                message.setAttribute('data-action-close-message', 'true');
            }

            let list = flash.querySelector('ul');
            let messages = flash.querySelectorAll('[data-action="close-message"]');
            for (let idx = 0; idx < messages.length; idx++) {
                setup_message(messages[idx]);
            }
        }
    };

    plugins.flash();
})();

/**
 * Plugin that sets a hidden action field on a form, based on the data-action of buttons in the form.
 */
(function() {
    function setup_form(form) {
        if (!form.getAttribute('data-action-action-buttons')) {
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
            form.setAttribute('data-action-action-buttons', 'true');
        }
    }

    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.formActionButtons = function() {
        let forms = document.querySelectorAll('form[data-action="action-buttons"]');
        for(let idx = 0; idx < forms.length; idx++) {
            setup_form(forms[idx]);
        }
    };

    plugins.formActionButtons();
})();

/**
 * Plugin that creates a popup when the user clicks on the image in the snippet.
 */
(function() {
    const body = document.querySelector('body');

    function setup_anchor(anchor) {
        if (!anchor.getAttribute('data-action-image-popup')) {
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
            anchor.setAttribute('data-action-image-popup', 'true');
        }
    }

    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.imagePopup = function() {
        let anchors = document.querySelectorAll('a[data-action="image-popup"]');
        for(let idx = 0; idx < anchors.length; idx++) {
            setup_anchor(anchors[idx]);
        }
    };

    plugins.imagePopup();
})();

/**
 * Plugin that posts the URL of a link, instead of the default GET action.
 */
(function() {
    function setup_anchor(anchor) {
        if (!anchor.getAttribute('data-action-post-link')) {
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
            anchor.setAttribute('data-action-post-link', 'true');
        }
    }

    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.postLink = function() {
        let anchors = document.querySelectorAll('a[data-action="post-link"]');
        for(let idx = 0; idx < anchors.length; idx++) {
            setup_anchor(anchors[idx]);
        }
    };

    plugins.postLink();
})();
