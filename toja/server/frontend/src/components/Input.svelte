<script lang="ts">
	import { createEventDispatcher } from 'svelte';

    export let type = 'text';
    export let value: string | boolean;
    export let values = [] as string[][];
    export let keyPropagation = false;
    export let error = '';
    export let disabled = false;

    const dispatch = createEventDispatcher();

    function changeValue(ev: Event) {
        if (type === 'checkbox' || type === 'radio') {
            value = (ev.target as HTMLInputElement).checked;
        } else if (type === 'textarea') {
            value = (ev.target as HTMLTextAreaElement).value;
        } else if (type === 'file') {
            const files = (ev.target as HTMLInputElement).files;
            if (files && files.length > 0) {
                const reader = new FileReader();
                reader.readAsDataURL(files[0]);
                reader.onload = (ev) => {
                    value = ev.target.result as string;
                }
            }
        } else if (type === 'select') {
            value = (ev.target as HTMLInputElement).value;
            if (value === 'null') {
                value = null;
            }
        } else {
            value = (ev.target as HTMLInputElement).value;
        }
        dispatch('change', value);
    }

    function stopPropagation(ev: KeyboardEvent) {
        if (!keyPropagation) {
            ev.stopPropagation();
        }
    }
</script>

{#if type === 'checkbox' || type === 'radio'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <input type={type} on:change={changeValue} checked={value} disabled={disabled} class="{disabled ? 'cursor-not-allowed' : ''}"/><span class="inline-block ml-2 text-sm"><slot></slot></span>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{:else if type === 'textarea'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}"><span class="block mb-2 {disabled ? 'text-gray-700' : 'text-black'} transition-colors text-sm"><slot></slot></span>
        <textarea on:change={changeValue} on:keydown={stopPropagation} on:keyup={stopPropagation} disabled={disabled} class="block w-full h-40 bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}">{value}</textarea>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{:else if type === 'select'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}"><span class="block mb-1 {disabled ? 'text-gray-700' : 'text-black'} transition-colors text-sm"><slot></slot></span>
        <select class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}" disabled={disabled} on:blur={changeValue} on:change={changeValue}>
            {#each values as [option_value, option_label]}
                <option value={option_value} selected={option_value === value}>{option_label}</option>
            {/each}
        </select>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{:else if type === 'file'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <span class="block mb-1 {disabled ? 'text-gray-700' : 'text-black'} transition-colors text-sm"><slot></slot></span><input type="file" disabled={disabled} on:change={changeValue} class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}"/>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{:else if type === 'textarea'}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <span class="block mb-1 {disabled ? 'text-gray-700' : 'text-black'} transition-colors text-sm"><slot></slot></span>
        <textarea disabled={disabled} on:change={changeValue} class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}">{value}</textarea>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{:else}
    <label class="block mb-4 {disabled ? 'cursor-not-allowed' : ''}">
        <span class="block mb-1 {disabled ? 'text-gray-700' : 'text-black'} transition-colors text-sm"><slot></slot></span><input type={type} value={value} disabled={disabled} on:change={changeValue} class="block w-full bg-gray-200 rounded px-4 py-3 focus:outline-primary {disabled ? 'cursor-not-allowed' : ''}"/>
        {#if error}
            <span class="block pt-1 text-red-600 text-sm role-error">{error}</span>
        {/if}
    </label>
{/if}
