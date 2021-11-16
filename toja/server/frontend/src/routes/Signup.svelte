<script lang="ts">
    import { saveJsonApiObject, sendJsonApiRequest, busy } from '../stores';
    import Input from '../components/Input.svelte';
    import Button from '../components/Button.svelte';

    let email = '';
    let emailError = '';
    let name = '';
    let nameError = '';

    let success = false;

    async function register(ev: Event) {
        ev.preventDefault();
        busy.startBusy();
        emailError = '';
        nameError = '';

        try {
            const user = await saveJsonApiObject({
                'type': 'users',
                'attributes': {
                    'email': email,
                    'name': name,
                },
            });
            busy.endBusy();
            success = true;
        } catch (error) {
            busy.endBusy();
            for (const err of error.errors) {
                if (err.source) {
                    if (err.source.pointer === 'attributes.email') {
                        emailError = err.title;
                    } else if (err.source.pointer === 'attributes.name') {
                        nameError = err.title;
                    }
                } else {
                    emailError = err.title;
                    nameError = err.title;
                }
            }
        }
    }
</script>

<div class="md:max-w-2xl mx-auto">
    {#if success}
        <h1 class="font-blackriver-bold text-4xl mb-8">Signed up to <span class="text-primary">The Old Joke Archive</span></h1>
        <p>Welcome to The Old Joke Archive! We hope you have a fun time here.</p>
        <p>You have been sent an e-mail to confirm your account and allow you to log in. The e-mail may have landed <span class="text-primary">in your spam folder</span>.</p>
    {:else}
        <h1 class="font-blackriver-bold text-4xl mb-8">Sign up to <span class="text-primary">The Old Joke Archive</span></h1>
        <form on:submit={register}>
            <Input bind:value={email} type="email" error={emailError} disabled={$busy}>E-Mail Address</Input>
            <Input bind:value={name} type="text" error={nameError} disabled={$busy}>Name</Input>
            <div class="mt-8 text-right">
                <Button disabled={$busy}>{#if $busy}Signing up...{:else}Sign up{/if}</Button>
            </div>
        </form>
    {/if}
</div>
