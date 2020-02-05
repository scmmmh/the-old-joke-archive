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
