<script lang="ts">
    import { tick } from 'svelte';

    import { saveJsonApiObject } from '../stores';
    import Input from './Input.svelte';

    export let user;

    let editing = false;
    let firstCell = null;

    async function startEditing(ev: Event) {
        ev.preventDefault();
        editing = true;
        await tick();
        if (firstCell) {
            firstCell.querySelector('input').focus();
        }
    }

    async function saveEdit(ev: Event) {
        ev.preventDefault();
        editing = false;
        await saveJsonApiObject(user);
    }

    function cancelEdit(ev: Event) {
        ev.preventDefault();
        editing = false;
    }
</script>

<tr>
    <td bind:this={firstCell} class="text-left border-b border-accent py-4">
        {#if editing}
            <Input type="text" bind:value={user.attributes.email}><span class="sr-only">E-Mail Address</span></Input>
        {:else}
            {user.attributes.email}
        {/if}
    </td>
    <td class="text-left border-b border-accent py-4">
        {#if editing}
            <Input type="email" bind:value={user.attributes.name}><span class="sr-only">Name</span></Input>
        {:else}
            {user.attributes.name}
        {/if}
    </td>
    <td class="text-left border-b border-accent py-4">
        {#if editing}
            <ul>
                <li><label class="mx-2 my-1"><input type="checkbox" checked={user.attributes.groups.indexOf('admin') >= 0}/> Superuser</label>
                <li><label class="mx-2 my-1"><input type="checkbox" checked={user.attributes.groups.indexOf('admin:user') >= 0}/> Admin: User</label>
            </ul>
        {:else}
            {user.attributes.groups.join(', ')}
        {/if}
    </td>
    <td class="text-left border-b border-accent py-4">
        {#if editing}
            <Input type="select" bind:value={user.attributes.status} values={[['active', 'Active'], ['blocked', 'Blocked'], ['inactive', 'Inactive'], ['new', 'New']]}><span class="sr-only">Status</span></Input>
        {:else}
            {user.attributes.status}
        {/if}
    </td>
    <td class="text-left border-b border-accent py-4">
        <ul class="flex">
            {#if editing}
                <li role="presentation" class="px-4 mr-4 border-r border-solid border-gray-300">
                    <button on:click={cancelEdit}>
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                        </svg>
                    </button>
                </li>
                <li role="presentation">
                    <button on:click={saveEdit}>
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                        </svg>
                    </button>
                </li>
            {:else}
                <li role="presentation" class="px-4 mr-4 border-r border-solid border-gray-300">
                    <button on:click={startEditing}>
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                        </svg>
                    </button>
                </li>
                <li role="presentation">
                    <button>
                        <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                            <path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                        </svg>
                    </button>
                </li>
            {/if}
        </ul>
    </td>
</tr>
