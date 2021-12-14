<script lang="ts">
    import { tick, createEventDispatcher } from 'svelte';
    import deepcopy from 'deepcopy';

    import { yearFromDate, monthDayFromDate } from '../util';
    import { isGroupAdmin, isGroupDataProvider, authUser, saveJsonApiObject, deleteJsonApiObject, dialog } from '../stores';
    import Input from './Input.svelte';
    import ImagePopup from './ImagePopup.svelte';

    export let source = null;

    const dispatch = createEventDispatcher();
    let showPopup = false;
    let editing = false;
    let firstCell = null;
    let editSource = null;
    let newImage = null;
    let confirmLicense = false;
    let errors = {}

    async function startEditing(ev: Event) {
        ev.preventDefault();
        editing = true;
        editSource = deepcopy(source);
        confirmLicense = false;
        await tick();
        if (firstCell) {
            firstCell.querySelector('input').focus();
        }
    }

    async function saveEdit(ev: Event) {
        ev.preventDefault();
        errors = {}
        if (!newImage || (newImage && confirmLicense)) {
            try {
                if (newImage) {
                    editSource.attributes.data = newImage;
                }
                source = await saveJsonApiObject(editSource);
                editing = false;
            } catch (e) {
                for (let error of e.errors) {
                    errors[error.source.pointer] = error.title;
                }
                await tick();
                const errorElement = document.querySelector('.role-error');
                if (errorElement) {
                    errorElement.parentElement.scrollIntoView({behavior: 'smooth', 'block': 'nearest'});
                }
            }
        } else {
            errors['confirmLicense'] = 'Please confirm that you are permitted to upload the file under the given license';
        }
    }

    function cancelEdit(ev: Event) {
        ev.preventDefault();
        editing = false;
    }

    async function deleteSource(ev: Event) {
        ev.preventDefault();
        dialog.set({
            title: 'Confirm deleting',
            message: 'Please confirm you wish to delete the source "' + source.attributes.title + '". This step cannot be undone.',
            buttons: [
                {
                    label: "Don't delete",
                    action() {
                        dialog.set(null);
                    },
                    type: 'secondary',
                    cancel: true,
                },
                {
                    label: 'Delete',
                    async action() {
                        dialog.set(null);
                        if (await deleteJsonApiObject('sources', source.id)) {
                           dispatch('delete');
                        }
                    }
                }
            ]
        });
    }
</script>

{#if source}
    <li>
        <div class="w-full flex flex-row space-x-8">
            <div class="flex-none">
                <div class="w-60 h-32 border border-gray-500 rounded-lg overflow-hidden">
                    <button on:click={() => { showPopup = true; }} aria-label="Show a popup with the source in full size">
                        <img src={source.attributes.data} alt="" class="max-w-none"/>
                    </button>
                </div>
            </div>
            {#if editing}
                <form on:submit={saveEdit} class="flex-auto">
                    <Input type="select" bind:value={editSource.attributes.type} values={[['book', 'Book'], ['newspaper', 'Newspaper']]} error={errors['attributes.type']}>Publication Type</Input>
                    <Input bind:value={editSource.attributes.title} error={errors['attributes.title']}>Publication Title</Input>
                    <Input bind:value={editSource.attributes.subtitle} error={errors['attributes.subtitle']}>Column / Chapter Title</Input>
                    <Input bind:value={editSource.attributes.date} error={errors['attributes.date']}>Publication Date (YYYY, YYYY-MM, YYYY-MM-DD)</Input>
                    <Input bind:value={editSource.attributes.publisher} error={errors['attributes.publisher']}>Publisher</Input>
                    <Input bind:value={editSource.attributes.location} error={errors['attributes.location']}>Publication Location</Input>
                    <Input bind:value={editSource.attributes.page_numbers} error={errors['attributes.page_numbers']}>Page Numbers</Input>
                    <Input bind:value={newImage} type="file" error={errors['attributes.data']}>New Source Image</Input>
                    <Input bind:value={confirmLicense} type="checkbox" error={errors['confirmLicense']}>Please confirm that you are permitted to upload this source image under a CC-BY-4.0
                        license. For more details on the license, please use the Copyright questions link in the page's footer.</Input>
                    <button class="hidden"></button>
                </form>
            {:else}
                <div class="flex-auto">
                    <h2 class="font-merriweather-bold text-2xl md:text-3xl italic uppercase mb-2">{source.attributes.title}</h2>
                    {#if source.attributes.subtitle}
                        <p>{source.attributes.subtitle}</p>
                    {/if}
                    {#if source.attributes.publisher || source.attributes.location}
                        <p>{source.attributes.publisher}{#if source.attributes.publisher && source.attributes.location}. {/if}{source.attributes.location}</p>
                    {/if}
                </div>
                <time class="flex-none block w-24">
                    <p class="font-blackriver-bold text-2xl md:text-4xl text-center">{yearFromDate(source.attributes.date)}</p>
                    <p class="text-center">{monthDayFromDate(source.attributes.date)}</p>
                </time>
            {/if}
        </div>
        {#if $isGroupAdmin || ($isGroupDataProvider && source.attributes.creator === $authUser.id)}
            <ul class="flex flex-row justify-end">
                {#if editing}
                    <li role="presentation" class="px-4 mr-4 border-r border-solid border-gray-300">
                        <button on:click={cancelEdit} aria-label="Discard changes">
                            <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
                            </svg>
                        </button>
                    </li>
                    <li role="presentation">
                        <button on:click={saveEdit} aria-label="Save changes">
                            <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                                <path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                            </svg>
                        </button>
                    </li>
                {:else}
                    <li role="presentation" class="px-4 mr-4 border-r border-solid border-gray-300">
                        <button on:click={startEditing} aria-label="Edit this source">
                            <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                                <path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                            </svg>
                        </button>
                    </li>
                    <li role="presentation">
                        <button on:click={deleteSource} aria-label="Delete this source">
                            <svg viewBox="0 0 24 24" class="w-6 h-6 text-accent hover:text-primary transition-colors">
                                <path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                            </svg>
                        </button>
                    </li>
                {/if}
            </ul>
        {/if}
        {#if showPopup}
            <ImagePopup imageUrl={source.attributes.data} on:close={() => { showPopup = false; }}/>
        {/if}
    </li>
{/if}
