(function() {
    var JokeExtractor = function(attachmentPoint, options) {
        var self = this;

        this._options = options;

        this._attachmentPoint = attachmentPoint;
        this._viewer = document.querySelector('#viewer');
        this._canvas = new fabric.Canvas(attachmentPoint.querySelector('#viewer canvas'));
        this._canvas.set({
            selection: false,
            uniScaleTransform: true
        });

        // Init state
        this._zoom = 1;
        this._imgBounds = {x: 0, y: 0, width: 0, height: 0};
        this._dragging = false;
        this._img = null;
        this.setMode('move');

        // Attach canvas events
        this._canvas.on('mouse:down', function(opt) { self.mouseDown(opt.e); });
        this._canvas.on('mouse:move', function(opt) { self.mouseMove(opt.e); });
        this._canvas.on('mouse:up', function(opt) { self.mouseUp(opt.e); });
        this._canvas.on('mouse:dblclick', function(opt) { self.zoomIn(); });
        this._canvas.on('object:selected', function(opt) { self.select(); })
        this._canvas.on('selection:cleared', function(opt) { self.deSelect(); })

        // Attach menu events
        this._attachmentPoint.querySelector('#zoom-initial').addEventListener('click', function() { self.zoomInitial(); });
        this._attachmentPoint.querySelector('#zoom-in').addEventListener('click', function() { self.zoomIn(); });
        this._attachmentPoint.querySelector('#zoom-out').addEventListener('click', function() { self.zoomOut(); });
        this._attachmentPoint.querySelector('#mode-move').addEventListener('click', function() { self.setMode('move'); });
        this._attachmentPoint.querySelector('#mode-add').addEventListener('click', function() { self.setMode('add'); });
        this._attachmentPoint.querySelector('#mode-edit').addEventListener('click', function() { self.setMode('edit'); });
        this._attachmentPoint.querySelector('#edit-remove').addEventListener('click', function() { self.removeSelected(); });
        this._attachmentPoint.querySelector('#edit-cancel').addEventListener('click', function() { self.cancelEdit(); });
        this._attachmentPoint.querySelector('#edit-save').addEventListener('click', function() { self.saveEdit(); });

        // Attach window events
        window.addEventListener('resize', function() { self.resize(); });
        this.resize();

        // Load existing data
        var jokes = options.jokes;
        this._jokes = [];
        for(var idx = 0; idx < jokes.length; idx++) {
            var rect = new fabric.Rect({
                left: jokes[idx].attributes.bbox.left + this._canvas.viewportTransform[4],
                top: jokes[idx].attributes.bbox.top,
                width: jokes[idx].attributes.bbox.width,
                height: jokes[idx].attributes.bbox.height,
                fill: 'transparent',
                stroke: jokes[idx].attributes.editable ? '#00aa00' : '#0000aa',
                hasRotatingPoint: false,
                hasBorders: false,
                selectable: false,
                cornerColor: '#000000',
                transparentCorners: false,
                sourceData: jokes[idx]
            });
            this._canvas.add(rect);
            this._jokes.push(rect);
        }
    };

    JokeExtractor.prototype = {
        resize: function() {
            this._clientWidth = this._viewer.clientWidth;
            this._clientHeight = this._viewer.clientHeight;
            this._canvas.setWidth(this._clientWidth);
            this._canvas.setHeight(this._clientHeight);

            if(this._img) {
                this._zoom = this._clientHeight / this._imgBounds.height;
                this._maxZoom = this._zoom;
                var transform = this._canvas.viewportTransform;
                transform[5] = 0;
                this._canvas.setViewportTransform(transform);
                this.update();
            }
        },
        load: function(url) {
            var self = this;

            fabric.Image.fromURL(url, function(img) {
                self._img = img;
                self._img.set({
                    selectable: false
                });
                self._canvas.add(self._img);
                self._imgBounds = self._img.getBoundingRect();
                self._zoom = self._clientHeight / self._imgBounds.height;
                self._maxZoom = self._zoom;
                self.update();
                for(var idx = 0; idx < self._jokes.length; idx++) {
                    self._canvas.bringToFront(self._jokes[idx]);
                }
            });
        },
        update: function() {
            this._canvas.setZoom(this._zoom);
            var transform = this._canvas.viewportTransform;
            transform[4] = this._clientWidth / 2 - (this._imgBounds.width * this._zoom) / 2;
            this._canvas.setViewportTransform(transform);
        },
        mouseDown: function(ev) {
            this._dragging = true;
            this._startMouseX = ev.offsetX;
            this._startMouseY = ev.offsetY;
        },
        mouseMove: function(ev) {
            if(this._dragging) {
                if(this._mode === 'move') {
                    var transform = this._canvas.viewportTransform;
                    transform[5] = transform[5] + (ev.offsetY - this._startMouseY);
                    this._canvas.setViewportTransform(transform);
                    this._startMouseY = ev.offsetY;
                }
            }
        },
        mouseUp: function(ev) {
            this._dragging = false;
            if(this._mode === 'add') {
                var rect = new fabric.Rect({
                    left: ev.offsetX - this._canvas.viewportTransform[4],
                    top: ev.offsetY / this._zoom - this._canvas.viewportTransform[5],
                    width: this._imgBounds.width,
                    height: 100,
                    fill: 'transparent',
                    stroke: '#00aa00',
                    hasRotatingPoint: false,
                    hasBorders: false,
                    cornerColor: '#000000',
                    transparentCorners: false
                });
                this._canvas.add(rect);
                this._jokes.push(rect);
                this.setMode('edit');
                this._canvas.setActiveObject(rect);
            }
        },
        select: function() {
            this._attachmentPoint.querySelector('#edit-remove').setAttribute('aria-disabled', 'false');
            this._attachmentPoint.querySelector('#edit-cancel').setAttribute('aria-disabled', 'false');
            this._attachmentPoint.querySelector('#edit-save').setAttribute('aria-disabled', 'false');
            for(var idx = 0; idx < this._jokes.length; idx++) {
                if(this._jokes[idx] !== this._canvas.getActiveObject()) {
                    if(this._jokes[idx].sourceData.attributes.editable) {
                        this._jokes[idx].set({stroke: '#00aa00'});
                    } else {
                        this._jokes[idx].set({stroke: '#0000aa'});
                    }
                } else {
                    this._jokes[idx].set({stroke: '#ff0000'});
                }
            }
        },
        deSelect: function() {
            this._attachmentPoint.querySelector('#edit-remove').setAttribute('aria-disabled', 'true');
            this._attachmentPoint.querySelector('#edit-cancel').setAttribute('aria-disabled', 'true');
            this._attachmentPoint.querySelector('#edit-save').setAttribute('aria-disabled', 'true');
            for(var idx = 0; idx < this._jokes.length; idx++) {
                if(this._jokes[idx].sourceData.attributes.editable) {
                    this._jokes[idx].set({stroke: '#00aa00'});
                } else {
                    this._jokes[idx].set({stroke: '#0000aa'});
                }
            }
        },
        zoomInitial: function() {
            this._zoom = this._maxZoom;
            var transform = this._canvas.viewportTransform;
            transform[5] = 0;
            this._canvas.setViewportTransform(transform);
            this.update();
        },
        zoomIn: function() {
            this._zoom = Math.min(this._zoom + (1 - this._maxZoom) / 5, 1);
            this.update();
        },
        zoomOut: function() {
            this._zoom = Math.max(this._zoom - (1 - this._maxZoom) / 5, this._maxZoom);
            this.update();
        },
        setMode: function(mode) {
            if(this._mode === 'move') {
                this._attachmentPoint.querySelector('#zoom-initial').parentElement.classList.add('hidden');
                this._attachmentPoint.querySelector('#zoom-in').parentElement.classList.add('hidden');
                this._attachmentPoint.querySelector('#zoom-out').parentElement.classList.add('hidden');
            } else if(this._mode === 'edit') {
                this._attachmentPoint.querySelector('#edit-remove').parentElement.classList.add('hidden');
                this._attachmentPoint.querySelector('#edit-cancel').parentElement.classList.add('hidden');
                this._attachmentPoint.querySelector('#edit-save').parentElement.classList.add('hidden');
                for(var idx = 0; idx < this._jokes.length; idx++) {
                    this._jokes[idx].set({selectable: false});
                }
                this._canvas.deactivateAllWithDispatch().renderAll();
            }
            if(this._mode) {
                this._attachmentPoint.querySelector('#mode-' + this._mode).setAttribute('aria-current', 'false');
            }
            this._mode = mode;
            this._attachmentPoint.querySelector('#mode-' + this._mode).setAttribute('aria-current', 'true');
            if(this._mode === 'move') {
                this._attachmentPoint.querySelector('#zoom-initial').parentElement.classList.remove('hidden');
                this._attachmentPoint.querySelector('#zoom-in').parentElement.classList.remove('hidden');
                this._attachmentPoint.querySelector('#zoom-out').parentElement.classList.remove('hidden');
            } else if(this._mode === 'edit') {
                this._attachmentPoint.querySelector('#edit-remove').parentElement.classList.remove('hidden');
                this._attachmentPoint.querySelector('#edit-cancel').parentElement.classList.remove('hidden');
                this._attachmentPoint.querySelector('#edit-save').parentElement.classList.remove('hidden');
                for(var idx = 0; idx < this._jokes.length; idx++) {
                    this._jokes[idx].set({selectable: !this._jokes[idx].sourceData || this._jokes[idx].sourceData.attributes.editable});
                }
            }
        },
        removeSelected: function() {
            this._canvas.remove(this._canvas.getActiveObject());
        },
        cancelEdit: function() {

        },
        saveEdit: function() {
            var self = this;
            this._attachmentPoint.querySelector('#edit-remove').setAttribute('aria-disabled', 'true');
            this._attachmentPoint.querySelector('#edit-cancel').setAttribute('aria-disabled', 'true');
            this._attachmentPoint.querySelector('#edit-save').setAttribute('aria-disabled', 'true');
            this._attachmentPoint.querySelector('#busy-spinner').classList.remove('hidden');
            var activeObject = this._canvas.getActiveObject();
            var bbox = activeObject.getBoundingRect();
            bbox.left = bbox.left - this._canvas.viewportTransform[4];
            bbox.top = bbox.top - this._canvas.viewportTransform[5];
            if(activeObject.sourceData !== undefined) {
                var promise = fetch(this._options.urls.update.replace('$jid', activeObject.sourceData.id), {
                    method: 'PATCH',
                    body: JSON.stringify({
                        data: {
                            type: 'images',
                            attributes: {
                                bbox: bbox
                            }
                        }
                    })
                });
            } else {
                var promise = fetch(this._options.urls.create, {
                    method: 'POST',
                    body: JSON.stringify({
                        data: {
                            type: 'images',
                            attributes: {
                                bbox: bbox
                            }
                        }
                    })
                });
            }
            promise.then(function(data) {
                data.json().then(function(body) {
                    activeObject.set({
                        sourceData: body.data
                    });
                    body.data.attributes.editable = true;
                    self._attachmentPoint.querySelector('#edit-cancel').setAttribute('aria-disabled', 'false');
                    self._attachmentPoint.querySelector('#edit-remove').setAttribute('aria-disabled', 'false');
                    self._attachmentPoint.querySelector('#edit-save').setAttribute('aria-disabled', 'false');
                    self._attachmentPoint.querySelector('#busy-spinner').classList.add('hidden');

                    var joke = self._attachmentPoint.querySelector('#joke-' + body.data.id);
                    if(joke === null) {
                        console.log('hm')
                        var joke = document.createElement('li');
                        joke.setAttribute('id', 'joke-' + body.data.id);
                        var img = document.createElement('img');
                        img.setAttribute('src', self._options.urls.image.replace('$jid', body.data.id))
                        joke.appendChild(img);
                        self._attachmentPoint.querySelector('#extract-list').appendChild(joke);
                    } else {
                        var img = joke.querySelector('img');
                        if(img.getAttribute('src').indexOf('#') < 0) {
                            img.setAttribute('src', img.getAttribute('src') + '#');
                        }
                        img.setAttribute('src', img.getAttribute('src') + '1');
                    }
                    joke.scrollIntoView();
                });
            }).catch(function(err) {
                self._attachmentPoint.querySelector('#edit-cancel').setAttribute('aria-disabled', 'false');
                self._attachmentPoint.querySelector('#edit-remove').setAttribute('aria-disabled', 'false');
                self._attachmentPoint.querySelector('#edit-save').setAttribute('aria-disabled', 'false');
                self._attachmentPoint.querySelector('#busy-spinner').classList.add('hidden');
            });
        }
    };

    if(!window.toja) {
        window.toja = {};
    }
    window.toja.JokeExtractor = JokeExtractor;
})();
