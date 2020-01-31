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
