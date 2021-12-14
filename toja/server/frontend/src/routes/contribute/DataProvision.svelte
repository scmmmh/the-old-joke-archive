<script lang="ts">
    import { tick } from 'svelte';

    import { getJsonApiObjects, saveJsonApiObject } from '../../stores';
    import DataSourceEntry from '../../components/DataSourceEntry.svelte';
    import Input from '../../components/Input.svelte';
    import Button from '../../components/Button.svelte';

    let errors = {}
    let sources = [];
    let newType = 'newspaper';
    let newTitle = '';
    let newSubtitle = '';
    let newDate = '';
    let newPublisher = '';
    let newLocation = '';
    let newPageNumbers = '';
    let newImage = null;
    let confirmLicense = false;
    let confirmLicenseError = '';
    let submitBusy = false;

    async function loadSources() {
        sources = await getJsonApiObjects('sources');
    }

    async function createSource(ev: Event) {
        ev.preventDefault();
        confirmLicenseError = '';
        if (confirmLicense) {
            submitBusy = true;
            errors = {}
            try {
                await saveJsonApiObject({
                    type: 'sources',
                    attributes: {
                        type: newType,
                        title: newTitle,
                        subtitle: newSubtitle,
                        date: newDate,
                        publisher: newPublisher,
                        location: newLocation,
                        page_numbers: newPageNumbers,
                        data: newImage,
                    }
                });
                newType = 'newspaper';
                newTitle = '';
                newSubtitle = '';
                newDate = '';
                newPublisher = '';
                newLocation = '';
                newPageNumbers = '';
                newImage = null;
                confirmLicense = false;
                await loadSources();
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
            submitBusy = false;
        } else {
            confirmLicenseError = 'Please confirm that you are permitted to upload the file under the given license'
        }
    }

    loadSources();
</script>

<h1 class="font-blackriver-bold text-2xl md:text-3xl lg:text-4xl mb-8">Sources</h1>

<div class="flex flex-row space-x-16">
    <ul class="flex-auto space-y-8">
        {#each sources as source}
            <DataSourceEntry source={source} on:delete={loadSources}/>
        {:else}
            <li>You have not yet provided any data sources.</li>
        {/each}
    </ul>
    <form on:submit={createSource} class="flex-none w-1/3">
        <h2 class="font-blackriver-bold text-2xl md:text-3xl mb-2">Contribute a source</h2>
        <Input bind:value={newType} type="select" values={[['book', 'Book'], ['newspaper', 'Newspaper']]} error={errors['attributes.type']}>Publication Type</Input>
        <Input bind:value={newTitle} error={errors['attributes.title']}>Publication Title</Input>
        <Input bind:value={newSubtitle} error={errors['attributes.subtitle']}>Column / Chapter Title</Input>
        <Input bind:value={newDate} error={errors['attributes.date']}>Publication Date (YYYY, YYYY-MM, YYYY-MM-DD)</Input>
        <Input bind:value={newPublisher} error={errors['attributes.publisher']}>Publisher</Input>
        <Input bind:value={newLocation} error={errors['attributes.location']}>Publication Location</Input>
        <Input bind:value={newPageNumbers} error={errors['attributes.page_numbers']}>Page Numbers</Input>
        <Input bind:value={newImage} type="file" error={errors['attributes.data']}>Source Image</Input>
        <Input type="checkbox" bind:value={confirmLicense} error={confirmLicenseError}>Please confirm that you are permitted to upload this source image under a CC-BY-4.0
            license. For more details on the license, please use the Copyright questions link in the page's footer.</Input>
        <div class="text-right">
            <Button disabled={submitBusy}>{#if submitBusy}Adding source...{:else}Add source{/if}</Button>
        </div>
    </form>
</div>
