/**
 * Plugin that posts the URL of a link, instead of the default GET action.
 */
(function() {
    function setup_anchor(anchor) {
        anchor.addEventListener('click', function(ev) {
            ev.preventDefault();
            let form = document.createElement('form');
            form.setAttribute('action', anchor.getAttribute('href'));
            form.setAttribute('method', 'post');
            anchor.append(form);
            form.submit();
        });
    }

    let anchors = document.querySelectorAll('a[data-action="post-link"]');
    for(let idx = 0; idx < anchors.length; idx++) {
        setup_anchor(anchors[idx]);
    }
})();
