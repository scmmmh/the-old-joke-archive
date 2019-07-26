<template>
    <div>
        <nav>
            <ul role="menu" class="menu">
                <li role="presentation">
                    <a data-action="move" role="menuitem" v-bind:aria-current="modeMove" @click="setMode('move')">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M13,6V11H18V7.75L22.25,12L18,16.25V13H13V18H16.25L12,22.25L7.75,18H11V13H6V16.25L1.75,12L6,7.75V11H11V6H7.75L12,1.75L16.25,6H13Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="add" role="menuitem" v-bind:aria-current="modeAdd" @click="setMode('add')">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="edit" role="menuitem" v-bind:aria-current="modeEdit" @click="setMode('edit')">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                        </svg>
                    </a>
                </li>
                <li role="separator"></li>
                <li role="presentation">
                    <a data-action="zoom-initial" role="menuitem" v-bind:aria-hidden="modeNotMove" @click="zoomInitial">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M9.5,13.09L10.91,14.5L6.41,19H10V21H3V14H5V17.59L9.5,13.09M10.91,9.5L9.5,10.91L5,6.41V10H3V3H10V5H6.41L10.91,9.5M14.5,13.09L19,17.59V14H21V21H14V19H17.59L13.09,14.5L14.5,13.09M13.09,9.5L17.59,5H14V3H21V10H19V6.41L14.5,10.91L13.09,9.5Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="zoom-in" role="menuitem" v-bind:aria-hidden="modeNotMove" @click="zoomIn">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M15.5,14L20.5,19L19,20.5L14,15.5V14.71L13.73,14.43C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.43,13.73L14.71,14H15.5M9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14M12,10H10V12H9V10H7V9H9V7H10V9H12V10Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="zoom-out" role="menuitem" v-bind:aria-hidden="modeNotMove" @click="zoomOut">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M15.5,14H14.71L14.43,13.73C15.41,12.59 16,11.11 16,9.5A6.5,6.5 0 0,0 9.5,3A6.5,6.5 0 0,0 3,9.5A6.5,6.5 0 0,0 9.5,16C11.11,16 12.59,15.41 13.73,14.43L14,14.71V15.5L19,20.5L20.5,19L15.5,14M9.5,14C7,14 5,12 5,9.5C5,7 7,5 9.5,5C12,5 14,7 14,9.5C14,12 12,14 9.5,14M7,9H12V10H7V9Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="confirm" role="menuitem" v-bind:aria-hidden="modeNotEdit" v-bind:disabled="nothingSelected" @click="saveChanges">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                        </svg>
                    </a>
                </li>
                <li role="presentation">
                    <a data-action="cancel" role="menuitem" v-bind:aria-hidden="modeNotEdit" v-bind:disabled="nothingSelected" @click="discardChanges">
                        <svg viewBox="0 0 24 24" class="icon mdi">
                            <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z" />
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>
        <div v-bind:id="guid" style="overflow:hidden;">
            <canvas>
            </canvas>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
// @ts-ignore
import { fabric } from 'fabric-browseronly';
import { Joke } from '@/interfaces';

@Component
export default class JokeSelector extends Vue {
    private guid = 'joke-selector-canvas';
    private viewer = null;
    private canvas = null;

    // Init the canvas state
    private viewerWidth = 0;
    private viewerHeight = 0;
    private zoom = 1;
    private imgBounds = {x: 0, y: 0, width: 0, height: 0};
    private dragging = false;
    private img: fabric.Image = null;
    private mode = 'move';
    private newRect: fabric.Rect = null;
    private jokes: fabric.Rect[] = [];
    private selected: fabric.Rect = null;

    // ****************
    // Lifecycle events
    // ****************

    /**
     * Upon mounting, setup the Fabric Canvas and attach all the listeners.
     */
    public mounted() {
        this.$data.viewer = document.querySelector('#' + this.$data.guid);
        if (this.$data.viewer) {
            this.$data.canvas = new fabric.Canvas(this.$data.viewer.querySelector('canvas'));
            this.$data.canvas.set({
                selection: false,
                uniScaleTransform: true,
            });
            this.$data.canvas.on('mouse:down', (opt: fabric.Event) => { this.mouseDown(opt.e); });
            this.$data.canvas.on('mouse:move', (opt: fabric.Event) => { this.mouseMove(opt.e); });
            this.$data.canvas.on('mouse:up', (opt: fabric.Event) => { this.mouseUp(opt.e); });
            this.$data.canvas.on('mouse:dblclick', () => { this.zoomIn(); });
            this.$data.canvas.on('mouse:wheel', (opt: fabric.Event) => { this.mouseScroll(opt.e); });
            this.$data.canvas.on('selection:created', (opt: fabric.Event) => { this.objectSelected(); });
            this.$data.canvas.on('selection:cleared', (opt: fabric.Event) => { this.objectDeselected(); });
            window.addEventListener('resize', this.resize);
            this.resize();
        }
    }

    /**
     * Before destroying remove the resize listener.
     */
    public beforeDestroy() {
        window.removeEventListener('resize', this.resize);
    }

    // **************
    // Event handlers
    // **************

    /**
     * Handle resizing the window
     */
    public resize() {
        this.$data.viewerWidth = this.$data.viewer.clientWidth;
        this.$data.viewerHeight = this.$data.viewer.clientHeight;
        this.$data.canvas.setWidth(this.$data.viewerWidth);
        this.$data.canvas.setHeight(this.$data.viewerHeight);
        if (this.$data.img) {
            this.$data.zoom = this.$data.viewerHeight / this.$data.imgBounds.height;
            this.$data.maxZoom = this.$data.zoom;
            const transform = this.$data.canvas.viewportTransform;
            transform[5] = 0;
            this.$data.canvas.setViewportTransform(transform);
            this.update();
        }
    }

    /**
     * Switch the joke selection view between "move", "add", and "edit".
     */
    public setMode(mode: string) {
        if (this.$data.mode === 'edit') {
            this.$data.jokes.forEach((joke: fabric.Rect) => {
                joke.set({selectable: false});
            });
            this.$data.canvas.discardActiveObject().renderAll();
            this.$data.canvas.hoverCursor = 'pointer';
        }
        this.$data.mode = mode;
        if (mode === 'move') {
            this.$data.canvas.hoverCursor = 'move';
        } else if (mode === 'add') {
            this.$data.canvas.hoverCursor = 'crosshair';
        } else if (mode === 'edit') {
            this.$data.canvas.hoverCursor = 'pointer';
            this.$data.jokes.forEach((joke: fabric.Rect) => {
                joke.set({selectable: true});
            });
            this.$data.canvas.renderAll();
        }
    }

    /**
     * Zoom to the inital full image zoom.
     */
    public zoomInitial() {
        this.$data.zoom = this.$data.maxZoom;
        const transform = this.$data.canvas.viewportTransform;
        transform[5] = 0;
        this.$data.canvas.setViewportTransform(transform);
        this.update();
    }

    /**
     * Zoom in one step. Zoom is split into 5 steps.
     */
    public zoomIn() {
        this.$data.zoom = Math.min(this.$data.zoom + (1 - this.$data.maxZoom) / 5, 1);
        this.update();
    }

    /**
     * Zoom out one step. Zoom is split into 5 steps.
     */
    public zoomOut() {
        this.$data.zoom = Math.max(this.$data.zoom - (1 - this.$data.maxZoom) / 5, this.$data.maxZoom);
        this.update();
    }

    /**
     * Handle the mouse down event. If the mode is "add", then create a new rectangle to show where the new
     * extract is added.
     */
    public mouseDown(ev: MouseEvent) {
        this.$data.dragging = true;
        this.$data.startMouseX = ev.offsetX;
        this.$data.startMouseY = ev.offsetY;
        if (this.$data.mode === 'add') {
            this.$data.newRect = new fabric.Rect({
                left: ev.offsetX - this.$data.canvas.viewportTransform[4],
                top: ev.offsetY / this.$data.zoom - this.$data.canvas.viewportTransform[5],
                width: 0,
                height: 10,
                fill: 'transparent',
                stroke: '#00aa00',
                hasRotatingPoint: false,
                hasBorders: false,
                hasCorners: false,
            });
            this.$data.canvas.add(this.$data.newRect);
        }
    }

    /**
     * Handle the mouse moving event on the canvas. If the mode is "move", then it pans the viewport. If the mode is
     * "add" it modifies the size of the new rectangle.
     */
    public mouseMove(ev: MouseEvent) {
        if (this.$data.dragging) {
            if (this.$data.mode === 'move') {
                const transform = this.$data.canvas.viewportTransform;
                transform[4] = transform[4] + (ev.offsetX - this.$data.startMouseX);
                transform[5] = transform[5] + (ev.offsetY - this.$data.startMouseY);
                this.$data.canvas.setViewportTransform(transform);
                this.$data.startMouseX = ev.offsetX;
                this.$data.startMouseY = ev.offsetY;
            } else if (this.$data.mode === 'add') {
                this.$data.newRect.set({
                    width: (ev.offsetX - this.$data.startMouseX) / this.$data.zoom
                            - this.$data.canvas.viewportTransform[4],
                    height: (ev.offsetY - this.$data.startMouseY) / this.$data.zoom
                             - this.$data.canvas.viewportTransform[5],
                });
                this.$data.canvas.renderAll();
            }
        }
    }

    /**
     * Handles the mouse up event. If the mode is "add", then a the "addJoke" action is dispatched on the store
     * with the bounding box of the new rectangle.
     */
    public mouseUp(ev: MouseEvent) {
        this.$data.dragging = false;
        if (this.$data.mode === 'add') {
            this.$data.canvas.remove(this.$data.newRect);
            const bbox = this.$data.newRect.getBoundingRect(true, true);
            bbox.left = bbox.left - this.$data.canvas.viewportTransform[4];
            bbox.top = bbox.top - this.$data.canvas.viewportTransform[5];
            this.$store.dispatch('addJoke', bbox);
            this.$data.newRect = null;
            this.setMode('edit');
        }
    }

    /**
     * Handles the mouse scrolling and pans the canvas horizontally and vertically.
     */
    public mouseScroll(ev: WheelEvent) {
        const transform = this.$data.canvas.viewportTransform;
        transform[4] = transform[4] + ev.deltaX * 10;
        transform[5] = transform[5] + ev.deltaY * 10;
        this.$data.canvas.setViewportTransform(transform);
    }

    /**
     * Handles selecting an object.
     */
    public objectSelected() {
        this.$data.selected = this.$data.canvas.getActiveObject();
    }

    /**
     * Handles deselecting an object, which means resetting its bounding box.
     */
    public objectDeselected() {
        this.$data.selected.set({
            left: this.$data.selected.sourceData.attributes.bbox.left,
            top: this.$data.selected.sourceData.attributes.bbox.top,
            width: this.$data.selected.sourceData.attributes.bbox.width,
            height: this.$data.selected.sourceData.attributes.bbox.height,
        });
        this.$data.selected = null;
        this.$data.canvas.renderAll();
    }

    /**
     * Discards any changes to the current selection.
     */
    public discardChanges() {
        this.$data.canvas.discardActiveObject().renderAll();
    }

    /**
     * Saves changes to the current selection, updating the bounding box.
     */
    public saveChanges() {
        this.$store.dispatch('updateJoke', {
            jid: this.$data.selected.sourceData.id,
            attrs: {
                bbox: this.$data.selected.getBoundingRect(true, true),
            },
        });
        this.$data.canvas.discardActiveObject().renderAll();
    }

    // ************
    // Dynamic data
    // ************

    /**
     * Is the mode set to "move".
     */
    public get modeMove() {
        return this.$data.mode === 'move' ? 'true' : 'false';
    }

    /**
     * Is the mode not set to "move".
     */
    public get modeNotMove() {
        return this.$data.mode !== 'move' ? 'true' : 'false';
    }

    /**
     * Is the mode set to "add".
     */
    public get modeAdd() {
        return this.$data.mode === 'add' ? 'true' : 'false';
    }

    /**
     * Is the mode set to "edit".
     */
    public get modeEdit() {
        return this.$data.mode === 'edit' ? 'true' : 'false';
    }

    /**
     * Is the mode not set to "edit".
     */
    public get modeNotEdit() {
        return this.$data.mode !== 'edit' ? 'true' : 'false';
    }

    /**
     * Is anything selected.
     */
    public get nothingSelected() {
        return this.$data.selected !== null ? null : 'disabled';
    }

    /**
     * React to updates to the list of jokes, drawing their bounding boxes.
     */
    @Watch('$store.state.jokes')
    public watchJokesList(newValue: object[], oldValue: object[]) {
        this.$data.jokes.forEach((rect: fabric.Rect) => {
            this.$data.canvas.remove(rect);
        });
        if (newValue) {
            const jokes: fabric.Rect[] = [];
            newValue.forEach((joke: fabric.Rect) => {
                const rect = new fabric.Rect({
                    left: joke.attributes.bbox.left,
                    top: joke.attributes.bbox.top,
                    width: joke.attributes.bbox.width,
                    height: joke.attributes.bbox.height,
                    fill: 'transparent',
                    stroke: '#00aa00',
                    hasRotatingPoint: false,
                    hasBorders: false,
                    transparentCorners: false,
                    selectable: false,
                    cornerColor: '#000000',
                    sourceData: joke,
                });
                jokes.push(rect);
                this.$data.canvas.add(rect);
            });
            this.$data.jokes = jokes;
        }
    }

    /**
     * React to updates to the source URL, loading the image source data.
     */
    @Watch('$store.state.source.attributes.raw')
    public watchSourceUrl(newValue: string, oldValue: string) {
        if (newValue !== '') {
            fabric.Image.fromURL(newValue, (img: fabric.Image) => {
                this.$data.img = img;
                this.$data.canvas.add(img);
                img.set({
                    selectable: false,
                });
                this.$data.canvas.sendToBack(img);
                this.$data.imgBounds = this.$data.img.getBoundingRect();
                this.$data.zoom = this.$data.viewerHeight / this.$data.imgBounds.height;
                this.$data.maxZoom = this.$data.zoom;
                this.update();
            });
        }
    }

    // ***************
    // Private methods
    // ***************

    /**
     * Update the canvas zoom.
     */
    private update() {
        this.$data.canvas.setZoom(this.$data.zoom);
    }
}
</script>
