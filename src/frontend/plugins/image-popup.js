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
