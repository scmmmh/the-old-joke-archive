<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let type = 'primary';
    export let disabled = false;
    let cls = '';
    export { cls as class};

    const dispatch = createEventDispatcher();

    function handleClick(ev: Event) {
        dispatch('action', ev);
    }
</script>

<button on:click={handleClick} class="inline-block {disabled ? 'bg-gray-200 text-black cursor-not-allowed' : (type === 'primary' ? 'bg-primary text-white italic hover:bg-accent focus:bg-accent' : 'text-primary hover:text-accent focus:text-accent')} border border-primary text-black italic hover:border-accent focus:border-accent transition-colors text-sm font-bold rounded-full px-6 py-3 {cls}" disabled={disabled}><slot></slot></button>
