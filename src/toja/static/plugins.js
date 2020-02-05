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
 * Plugin that handles the joke ratings, both submission and tracking of changes.
 */
(function() {
    function setup_anchor(anchor) {
        if (!anchor.getAttribute('data-action-joke-ratings')) {
            anchor.setAttribute('data-action-joke-ratings', 'true');
        }
    }

    function setup_tracking(rating) {
        if (!rating.getAttribute('data-action-joke-ratings')) {
            let categories = rating.querySelectorAll('span[data-joke-ratings-category]');
            let timeout = 1000;
            let timeoutId = null;
            function update() {
                clearTimeout(timeoutId);
                let request = fetch(rating.getAttribute('data-joke-rating-url'));
                request.then((response) => {
                    timeoutId = setTimeout(update, timeout);
                    response.json().then((data) => {
                        for(let idx = 0; idx < categories.length; idx++) {
                            let category = categories[idx].getAttribute('data-joke-ratings-category');
                            if (data[category]) {
                                categories[idx].innerHTML = data[category];
                            } else {
                                categories[idx].innerHTML = 0;
                            }
                        }
                        timeout = Math.min(timeout * 6, 60000);
                    });
                });
            }
            timeoutId = setTimeout(update, timeout);
            let anchors = rating.querySelectorAll('a[data-action="joke-ratings"]');
            for(let idx = 0; idx < anchors.length; idx++) {
                (function (anchor) {
                    anchor.addEventListener('click', function(ev) {
                        ev.preventDefault();
                        let request = fetch(anchor.getAttribute('href'), {
                            method: 'POST',
                        });
                        request.then((response) => {
                            let countElement = anchor.querySelector('span');
                            let count = Number.parseInt(countElement.innerHTML);
                            countElement.innerHTML = count + 1;
                            clearTimeout(timeoutId);
                            timeoutId = setTimeout(update, 1000);
                        });
                    });
                })(anchors[idx]);
            }
            rating.setAttribute('data-action-joke-ratings', 'true');
        }
    }

    window.TOJA_PLUGINS = window.TOJA_PLUGINS || {};
    let plugins = window.TOJA_PLUGINS;
    plugins.jokeRatings = function() {
        let ratings = document.querySelectorAll('div[data-action="update-ratings"]');
        for(let idx = 0; idx < ratings.length; idx++) {
            setup_tracking(ratings[idx]);
        }
    };

    plugins.jokeRatings();
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
