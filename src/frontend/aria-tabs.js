/**
 * ARIA-conformant handler for tabs lists.
 */
(function() {
    function init(tablist) {
        var tabs = document.querySelectorAll('*[role="tab"]');
        var panels = [];
        function clickListener(ev) {
            ev.preventDefault();
            for(var idx = 0; idx < tabs.length; idx++) {
                if(tabs[idx] === ev.target) {
                    tabs[idx].setAttribute('aria-selected', 'true');
                } else {
                    tabs[idx].setAttribute('aria-selected', 'false');
                }
            }
            for(var idx = 0; idx < panels.length; idx++) {
                if(panels[idx].getAttribute('id') === ev.target.getAttribute('aria-controls')) {
                    panels[idx].setAttribute('aria-hidden', 'false');
                } else {
                    panels[idx].setAttribute('aria-hidden', 'true');
                }
            }

        }
        for(var idx = 0; idx < tabs.length; idx++) {
            tabs[idx].addEventListener('click', clickListener);
            var panel = document.querySelector('#' + tabs[idx].getAttribute('aria-controls'));
            if(panel) {
                panels.push(panel);
            }
        }
    }

    var tabControls = document.querySelectorAll('*[role="tablist"]');
    for(var idx = 0; idx < tabControls.length; idx++) {
        init(tabControls[idx]);
    }
})();
