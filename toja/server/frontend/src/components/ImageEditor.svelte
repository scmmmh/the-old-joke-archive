<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Application, Sprite, Graphics } from 'pixi.js';

    import { getJsonApiObject } from '../stores';

    let containerElement = null as HTMLElement;
    let app = null as Application;
    let sprite = null as Sprite;

    function resizeWindow() {
        app.resize();
    }

    onMount(() => {
        app = new Application({
            resizeTo: containerElement,
            backgroundColor: 0xffffff,
        });
        containerElement.appendChild(app.view);
        app.resize();
        window.addEventListener('resize', resizeWindow);
        getJsonApiObject('sources', '8344cd50-892a-11ec-af11-c9a7094645a3').then((data) => {
            sprite = Sprite.from(data.attributes.data as string);
            app.stage.addChild(sprite);
            const graphics = new Graphics();
            graphics.x = 0;
            graphics.y = 0;
            graphics.lineStyle(3, 0xDF95B6);
            graphics.drawRect(0, 0, 300, 300);
            graphics.zIndex = 1;
            app.stage.addChild(graphics);
            const graphics2 = new Graphics();
            graphics2.x = 5;
            graphics2.y = 195;
            graphics2.lineStyle(3, 0x222222, 0.4);
            graphics2.beginFill(0x222222, 0.2);
            graphics2.drawRect(0, 0, 505, 190);
            graphics2.zIndex = 0;
            app.stage.addChild(graphics2);
            app.view.addEventListener('wheel', (ev: Event) => {
                ev.preventDefault();
                if (ev.deltaY > 0) {
                    sprite.scale.set(sprite.scale.x + 0.02);
                    graphics.scale.set(graphics.scale.x + 0.02);
                } else if (ev.deltaY < 0) {
                    sprite.scale.set(sprite.scale.x - 0.02);
                    graphics.scale.set(graphics.scale.x - 0.02);
                }
            });
        });
    });

    onDestroy(() => {
        window.removeEventListener('resize', resizeWindow);
    });

</script>

<div bind:this={containerElement} class="w-full h-full"></div>