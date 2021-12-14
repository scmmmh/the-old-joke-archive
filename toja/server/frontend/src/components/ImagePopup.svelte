<script lang="ts">
    import { createEventDispatcher, onMount } from 'svelte';

    export let imageUrl;
    let imageElement = null;
    const dispatch = createEventDispatcher();

    function close() {
        dispatch('close');
    }

    function handleKeyDown(ev: KeyboardEvent) {
        console.log(ev.key);
        if (ev.key === 'Escape') {
            close();
        }
    }

    onMount(() => {
        if (imageElement) {
            imageElement.focus();
        }
    });
</script>

<div on:click={close} on:keydown={handleKeyDown} class="fixed left-0 top-0 w-screen h-screen bg-black bg-opacity-75 z-50" style="margin-left:0;margin-right:0;">
    <div on:click={(ev) => { ev.stopPropagation(); }} class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-9/10 max-h-9/10 bg-white px-4 py-2 rounded-lg overflow-auto overscroll-none">
        <img bind:this={imageElement} src={imageUrl} alt="" class="max-w-none" tabindex="-1"/>
    </div>
</div>
