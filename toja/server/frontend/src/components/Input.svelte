<script lang="ts">
    export let type = 'text';
    export let value: string | boolean;
    export let values = [] as string[][];
    export let keyPropagation = false;
    export let error = '';
    export let disabled = false;

    function changeValue(ev: Event) {
        if (type === 'checkbox' || type === 'radio') {
            value = (ev.target as HTMLInputElement).checked;
        } else if (type === 'textarea') {
            value = (ev.target as HTMLTextAreaElement).value;
        } else {
            value = (ev.target as HTMLInputElement).value
        }
    }

    function stopPropagation(ev: KeyboardEvent) {
        if (!keyPropagation) {
            ev.stopPropagation();
        }
    }
</script>

{#if type === 'checkbox' || type === 'radio'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <input type={type} on:change={changeValue} checked={value} disabled={disabled} class="{disabled ? 'cursor-not-allowed' : ''}"/><span class="inline-block ml-2"><slot></slot></span>
        {#if error !== ''}
            <span class="block pt-1 text-red-600 text-sm">{error}</span>
        {/if}
    </label>
{:else if type === 'textarea'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}"><slot></slot>
        <textarea on:change={changeValue} on:keydown={stopPropagation} on:keyup={stopPropagation} disabled={disabled} class="block w-full h-40 bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}">{value}</textarea>
        {#if error !== ''}
            <span class="block pt-1 text-red-600 text-sm">{error}</span>
        {/if}
    </label>
{:else if type === 'select'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}"><slot></slot>
        <select class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}" disabled={disabled} on:blur={changeValue} on:change={changeValue}>
            {#each values as [option_value, option_label]}
                <option value={option_value} selected={option_value === value ? 'selected' : null}>{option_label}</option>
            {/each}
        </select>
    </label>
{:else}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <span class="block mb-2 {disabled ? 'text-gray-700' : 'text-black'} transition-colors"><slot></slot></span><input type={type} value={value} disabled={disabled} on:change={changeValue} class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}"/>
        {#if error !== ''}
            <span class="block pt-1 text-red-600 text-sm">{error}</span>
        {/if}
    </label>
{/if}
