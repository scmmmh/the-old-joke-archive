/**
 * JavaScript functionality to handle the inline field editor.
 */
function inlineEditor() {
    function init(field) {
        let display = field.querySelector('div');
        let form = field.querySelector('form');
        form.classList.add('hidden');
        display.querySelector('*[data-action="edit"]').addEventListener('click', function(ev) {
            ev.preventDefault();
            display.classList.add('hidden');
            form.classList.remove('hidden')
        });
        form.querySelector('*[data-action="cancel"]').addEventListener('click', function(ev) {
            ev.preventDefault();
            display.classList.remove('hidden');
            form.classList.add('hidden')
        });
    }

    let fields = document.querySelectorAll('*[data-action="inline-edit"]');
    for(let idx = 0; idx < fields.length; idx++) {
        init(fields[idx]);
    }
};
inlineEditor();

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
