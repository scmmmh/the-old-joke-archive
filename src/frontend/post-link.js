function postLink() {
    function init(anchor) {
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
        init(anchors[idx]);
    }
}
postLink();
