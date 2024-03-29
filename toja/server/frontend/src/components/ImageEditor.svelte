<script lang="ts">
    import { onMount, onDestroy, createEventDispatcher, tick } from 'svelte';
    import { Application, Sprite, Graphics, Point } from 'pixi.js';
    import deepcopy from 'deepcopy';

    import IconButton from './IconButton.svelte';
    import { getJsonApiObjects, saveJsonApiObject, deleteJsonApiObject } from '../stores';

    type Element = {
        joke: JokeDocument,
        graphics: Graphics,
        editable: boolean,
        selected: boolean
    };

    export let source: SourceDocument;

    const MODE_SELECT = 1;
    const MODE_EDIT = 2;
    const MODE_NEW = 3;
    const DRAG_MODE_NONE = 0;
    const DRAG_MODE_LEFT_EDGE = 1;
    const DRAG_MODE_TOP_EDGE = 2;
    const DRAG_MODE_RIGHT_EDGE = 3;
    const DRAG_MODE_BOTTOM_EDGE = 4;
    const DRAG_MODE_LEFT_TOP_CORNER = 5;
    const DRAG_MODE_RIGHT_TOP_CORNER = 6;
    const DRAG_MODE_RIGHT_BOTTOM_CORNER = 7;
    const DRAG_MODE_LEFT_BOTTOM_CORNER = 8;
    const DRAG_MODE_WHOLE = 9;
    const DRAG_MODE_OTHER = 10;

    let oldSourceId  = null;
    let containerElement = null as HTMLElement;
    let editMenuElement = null as HTMLElement;
    let app = null as Application;
    let mode = MODE_SELECT;
    let dragMode = DRAG_MODE_NONE;
    let busyAction = '';

    let image = null as Sprite;
    let elements = [] as Element[];
    let scale = 1;
    let selectedElement = null as Element;
    let offsetX = 0;
    let offsetY = 0;
    let mouseDown = false;
    let mouseDownX = 0;
    let mouseDownY = 0;
    let dragging = false;
    let originalElement = null as Element;

    let dispatch = createEventDispatcher();

    function resizeWindow() {
        app.resize();
    }

    function render() {
        image.x = offsetX;
        image.y = offsetY;
        image.scale.set(scale);
        for (let element of elements) {
            if  ((element.joke.attributes as JokeDocumentAttributes).coordinates[0] !== null &&  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[1] !== null) {
                element.graphics.x =  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[0] * scale + offsetX;
                element.graphics.y =  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[1] * scale + offsetY;
                element.graphics.clear();
                if (element.editable) {
                    if (element.selected) {
                        element.graphics.lineStyle(3, 0xDF95B6).beginFill(0xffffff, 0.1);
                        element.graphics.zIndex = 20;
                        editMenuElement.style.left = Math.min(containerElement.clientWidth - editMenuElement.offsetWidth,  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[2] * scale + offsetX - editMenuElement.offsetWidth + 2) + 'px';
                        editMenuElement.style.top =  ((element.joke.attributes as JokeDocumentAttributes).coordinates[3] * scale + offsetY + 2) + 'px';
                    } else {
                        element.graphics.lineStyle(3, 0x2D8095).beginFill(0xffffff, 0.1);
                        element.graphics.zIndex = 10;
                    }
                } else {
                    element.graphics.lineStyle(3, 0x222222, 0.4).beginFill(0x222222, 0.2);
                    element.graphics.zIndex = 0;
                }
                element.graphics.drawRect(0, 0,  ((element.joke.attributes as JokeDocumentAttributes).coordinates[2] -  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[0]) * scale,  ((element.joke.attributes as JokeDocumentAttributes).coordinates[3] -  ((element.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates[1]) * scale);
            }
        }
    }

    function canvasMouseDown(ev: MouseEvent) {
        mouseDown = true;
        mouseDownX = ev.clientX;
        mouseDownY = ev.clientY;
        dragging = false;
        if (mode === MODE_NEW) {
            const point = new Point(0, 0);
            app.renderer.plugins.interaction.mapPositionToPoint(point, ev.clientX, ev.clientY);
             (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates = [(point.x - offsetX) / scale, (point.y - offsetY) / scale, (point.x - offsetX) / scale, (point.y - offsetY) / scale];
            dragging = true;
            app.view.style.cursor = 'nwse-resize';
            mode = MODE_EDIT;
            dragMode = DRAG_MODE_RIGHT_BOTTOM_CORNER;
        }
    }

    function canvasMouseMove(ev: MouseEvent) {
        if (mouseDown) {
            let deltaX = ev.clientX - mouseDownX;
            let deltaY = ev.clientY - mouseDownY;
            if (!dragging && Math.abs(deltaX) >= 5 || Math.abs(deltaY) >= 5) {
                dragging = true;
                editMenuElement.classList.add('hidden');
            }
            if (dragging) {
                if (selectedElement && dragMode !== DRAG_MODE_OTHER) {
                    deltaX = deltaX / scale;
                    deltaY = deltaY / scale;
                    if (dragMode === DRAG_MODE_WHOLE) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] + deltaY;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] + deltaY;
                    } else if (dragMode == DRAG_MODE_LEFT_EDGE) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] + deltaX;
                    } else if (dragMode == DRAG_MODE_TOP_EDGE) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] + deltaY;
                    } else if (dragMode == DRAG_MODE_RIGHT_EDGE) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] + deltaX;
                    } else if (dragMode == DRAG_MODE_BOTTOM_EDGE) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] + deltaY;
                    } else if (dragMode == DRAG_MODE_LEFT_TOP_CORNER) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] + deltaY;
                    } else if (dragMode == DRAG_MODE_RIGHT_TOP_CORNER) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[1] + deltaY;
                    } else if (dragMode == DRAG_MODE_RIGHT_BOTTOM_CORNER) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[2] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] + deltaY;
                    } else if (dragMode == DRAG_MODE_LEFT_BOTTOM_CORNER) {
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[0] + deltaX;
                         (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] =  (selectedElement.joke.attributes as JokeDocumentAttributes).coordinates[3] + deltaY;
                    }
                } else {
                    offsetX = offsetX + deltaX;
                    offsetY = offsetY + deltaY;
                }
                mouseDownX = ev.clientX;
                mouseDownY = ev.clientY;
                render();
            }
        } else {
            const point = new Point(0, 0);
            app.renderer.plugins.interaction.mapPositionToPoint(point, ev.clientX, ev.clientY);
            const target = app.renderer.plugins.interaction.hitTest(point);
            if (target) {
                if (mode === MODE_SELECT) {
                    app.view.style.cursor = 'pointer';
                } else if (mode === MODE_EDIT && selectedElement && target === selectedElement.graphics) {
                    const leftDelta = Math.abs(target.x - point.x);
                    const rightDelta = Math.abs(target.x + target.width - point.x);
                    const topDelta = Math.abs(target.y - point.y);
                    const bottomDelta = Math.abs(target.y + target.height - point.y);
                    if (leftDelta < 8 && topDelta < 8) {
                        app.view.style.cursor = 'nwse-resize';
                        dragMode = DRAG_MODE_LEFT_TOP_CORNER;
                    } else if (rightDelta < 8 && topDelta < 8) {
                        app.view.style.cursor = 'nesw-resize';
                        dragMode = DRAG_MODE_RIGHT_TOP_CORNER;
                    } else if (rightDelta < 8 && bottomDelta < 8) {
                        app.view.style.cursor = 'nwse-resize';
                        dragMode = DRAG_MODE_RIGHT_BOTTOM_CORNER;
                    } else if (leftDelta < 8 && bottomDelta < 8) {
                        app.view.style.cursor = 'nesw-resize';
                        dragMode = DRAG_MODE_LEFT_BOTTOM_CORNER;
                    } else if (leftDelta < 8) {
                        app.view.style.cursor = 'ew-resize';
                        dragMode = DRAG_MODE_LEFT_EDGE;
                    } else if (topDelta < 8) {
                        app.view.style.cursor = 'ns-resize';
                        dragMode = DRAG_MODE_TOP_EDGE;
                    } else if (rightDelta < 8) {
                        dragMode = DRAG_MODE_RIGHT_EDGE;
                        app.view.style.cursor = 'ew-resize';
                    } else if (bottomDelta < 8) {
                        app.view.style.cursor = 'ns-resize';
                        dragMode = DRAG_MODE_BOTTOM_EDGE;
                    } else {
                        app.view.style.cursor = 'move';
                        dragMode = DRAG_MODE_WHOLE;
                    }
                } else {
                    dragMode = DRAG_MODE_OTHER;
                }
            } else if (mode === MODE_NEW) {
                app.view.style.cursor = 'copy';
            } else {
                app.view.style.cursor = 'move';
                dragMode = DRAG_MODE_OTHER;
            }
        }
    }

    function canvasMouseUp(ev: MouseEvent) {
        mouseDown = false;
        if (!dragging) {
            if (mode === MODE_SELECT) {
                const point = new Point(0, 0);
                app.renderer.plugins.interaction.mapPositionToPoint(point, ev.clientX, ev.clientY);
                const target = app.renderer.plugins.interaction.hitTest(point);
                if (target) {
                    selectedElement = null;
                    editMenuElement.classList.add('hidden');
                    mode = MODE_EDIT;
                    for (let element of elements) {
                        if (element.graphics === target) {
                            element.selected = true;
                            selectedElement = element;
                            originalElement = deepcopy(selectedElement);
                            editMenuElement.classList.remove('hidden');
                            tick().then(() => {
                                (editMenuElement.querySelector('[aria-label="Save changes"]') as HTMLElement).focus();
                                render();
                            });
                        } else {
                            element.selected = false;
                        }
                    }
                    render();
                }
            }
        }
        if (mode === MODE_EDIT) {
            editMenuElement.classList.remove('hidden');
            tick().then(() => {
                (editMenuElement.querySelector('[aria-label="Save changes"]') as HTMLElement).focus();
                render();
            });
        }
    }

    function canvasScroll(ev: WheelEvent) {
        ev.preventDefault();
        if (ev.deltaY > 0) {
            scale = scale + 0.02;
        } else if (ev.deltaY < 0) {
            scale = scale - 0.02;
        }
        render();
    }

    async function loadData(source: SourceDocument) {
        if (app && source && source.id !== oldSourceId) {
            oldSourceId = source.id;
            app.stage.removeChildren();
            image = Sprite.from(source.attributes.data as string);
            app.stage.addChild(image);
            setTimeout(() => {
                if (image.width > 1) {
                    scale = containerElement.clientWidth / image.width;
                    render();
                }
            }, 50);
            if (image.width > 1) {
                scale = containerElement.clientWidth / image.width;
            } else {
                scale = 1;
            }
            const jokeIds = source.relationships.jokes.data.map((rel) => {
                return rel.id;
            })
            for (let joke of await getJsonApiObjects('jokes', 'filter[id]=' + jokeIds.join(',')) as JokeDocument[]) {
                let found = false;
                for (let element of elements) {
                    if (element.joke.id === joke.id) {
                        element.joke = joke;
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    const element = {
                        joke: joke,
                        graphics: new Graphics(),
                        editable: true,
                        selected: false,
                    };
                    if (element.editable) {
                        element.graphics.interactive = true;
                    }
                    app.stage.addChild(element.graphics);
                    elements.push(element);
                }
                render();
            }
            render();
        }
    }

    onMount(() => {
        app = new Application({
            resizeTo: containerElement,
            backgroundColor: 0xd1d5db,
        });
        containerElement.appendChild(app.view);
        app.resize();
        app.stage.sortableChildren = true;
        app.view.addEventListener('wheel', canvasScroll);
        app.view.addEventListener('mousedown', canvasMouseDown);
        app.view.addEventListener('mousemove', canvasMouseMove);
        app.view.addEventListener('mouseup', canvasMouseUp);
        window.addEventListener('resize', resizeWindow);
        loadData(source);
    });

    $: loadData(source);

    onDestroy(() => {
        window.removeEventListener('resize', resizeWindow);
    });

    function addNew() {
        selectedElement = {
            joke: {
                type: 'jokes',
                attributes: {
                    title: '[Untitled]',
                    coordinates: [null, null, null, null],
                    transcriptions: {}
                },
                relationships: {
                    source: {
                        data: {
                            type: 'sources',
                            id: source.id,
                        },
                    },
                },
            },
            graphics: new Graphics(),
            editable: true,
            selected: true,
        };
        selectedElement.graphics.interactive = true;
        app.stage.addChild(selectedElement.graphics);
        elements.push(selectedElement);
        mode = MODE_NEW;
        dragMode = DRAG_MODE_RIGHT_BOTTOM_CORNER;
        originalElement = null;
        render();
    }

    function cancelEdit() {
        if (originalElement) {
            ( (selectedElement.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates = (originalElement.joke.attributes as JokeDocumentAttributes).coordinates;
        } else {
            elements = elements.filter((element) => { return element === selectedElement});
            app.stage.removeChild(selectedElement.graphics);
        }
        mode = MODE_SELECT;
        editMenuElement.classList.add('hidden');
        selectedElement = null;
        for (let element of elements) {
            element.selected = false;
        }
        render();
    }

    async function saveEdit() {
        busyAction = 'edit';
        try {
            const updateJoke = {
                type: 'jokes',
                attributes: {
                    actions: [
                        {
                            coordinates: ( (selectedElement.joke.attributes as JokeDocumentAttributes) as JokeDocumentAttributes).coordinates,
                        }
                    ],
                },
                relationships: selectedElement.joke.relationships,
            } as JokeDocument;
            if (selectedElement.joke.id) {
                updateJoke.id = selectedElement.joke.id;
            }
            selectedElement.joke = await saveJsonApiObject(updateJoke) as JokeDocument;
            dispatch('changed', selectedElement.joke);
            mode = MODE_SELECT;
            editMenuElement.classList.add('hidden');
            selectedElement = null;
            for (let element of elements) {
                element.selected = false;
            }
            render();
        } finally {
            busyAction = '';
        }
    }

    async function deleteElement() {
        busyAction = 'delete';
        try {
            await deleteJsonApiObject('jokes', selectedElement.joke.id);
            dispatch('deleted', selectedElement.joke);
            elements = elements.filter((element) => { return element !== selectedElement});
            app.stage.removeChild(selectedElement.graphics);
            mode = MODE_SELECT;
            editMenuElement.classList.add('hidden');
            selectedElement = null;
            render();
        } finally {
            busyAction = '';
        }
    }
</script>

<div class="w-full h-full flex flex-col">
    <nav class="flex-none">
        <ul class="flex flex-row gap-1 pb-1">
            <li role="presentation">
                <IconButton on:action={addNew} disabled={mode === MODE_EDIT} active={mode === MODE_NEW} label="Mark up a new joke"><path fill="currentColor" d="M14.1,9L15,9.9L5.9,19H5V18.1L14.1,9M17.7,3C17.5,3 17.2,3.1 17,3.3L15.2,5.1L18.9,8.9L20.7,7C21.1,6.6 21.1,6 20.7,5.6L18.4,3.3C18.2,3.1 17.9,3 17.7,3M14.1,6.2L3,17.2V21H6.8L17.8,9.9L14.1,6.2M7,2V5H10V7H7V10H5V7H2V5H5V2H7Z" /></IconButton>
            </li>
        </ul>
    </nav>
    <div bind:this={containerElement} class="relative flex-auto border">
        <nav bind:this={editMenuElement} class="hidden absolute z-10 w-min bg-white/95 border border-primary shadow-lg">
            <ul class="flex flex-row p-1 gap-1">
                {#if selectedElement && selectedElement.joke.id}
                    <li role="presentation">
                        <IconButton on:action={deleteElement} disabled={busyAction !== '' && busyAction !== 'delete'} busy={busyAction === 'delete'} label="Delete this joke"><path fill="currentColor" d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z" /></IconButton>
                    </li>
                {/if}
                <li role="presentation">
                    <IconButton on:action={cancelEdit} disabled={busyAction !== ''} label="Discard any changes"><path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></IconButton>
                </li>
                <li role="presentation">
                    <IconButton on:action={saveEdit} disabled={busyAction !== '' && busyAction !== 'edit'} busy={busyAction === 'edit'} label="Save changes"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></IconButton>
                </li>
            </ul>
        </nav>
    </div>
</div>
