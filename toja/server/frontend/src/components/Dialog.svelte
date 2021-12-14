<script lang="ts">
    import { onDestroy, tick } from 'svelte';

    import { dialog } from '../stores';
    import Button from './Button.svelte';

    let paragraphs = [];
    let headingElement = null;

    const dialogUnsubscribe = dialog.subscribe((dialog) => {
        paragraphs = [];
        if (dialog) {
            document.querySelector('body').classList.add('overflow-hidden');
            if (dialog.message) {
                paragraphs = dialog.message.split('\n');
            }
            tick().then(() => {
                if (headingElement) {
                    headingElement.focus();
                }
            });
        } else {
            document.querySelector('body').classList.remove('overflow-hidden');
        }
    });

    function handleCancel() {
        if ($dialog && $dialog.buttons) {
            for (let button of $dialog.buttons) {
                if (button.cancel) {
                    button.action();
                }
            }
        }
    }

    onDestroy(dialogUnsubscribe);
</script>

{#if $dialog}
    <div on:click={handleCancel} class="fixed left-0 top-0 w-full h-full bg-black bg-opacity-70">
        <div on:click={(ev) => { ev.preventDefault(); }} class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-9/10 max-h-9/10 bg-white rounded-lg p-4" role="dialog">
            <h2 bind:this={headingElement} class="font-blackriver-bold text-xl md:text-2xl mb-4" tabindex="-1">{$dialog.title}</h2>
            {#each paragraphs as paragraph}
                <p>{paragraph}</p>
            {/each}
            {#if $dialog.buttons}
                <ul class="flex flex-row justify-end space-x-2">
                    {#each $dialog.buttons as button}
                        <Button type={button.type} class={button.class} on:action={button.action}>{button.label}</Button>
                    {/each}
                </ul>
            {/if}
        </div>
    </div>
{/if}
