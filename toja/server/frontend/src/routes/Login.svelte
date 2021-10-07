<script lang="ts">
    import { busy, sendJsonApiRequest } from '../stores';
    import Input from '../components/Input.svelte';
    import Button from '../components/Button.svelte';

    let email = '';
    let emailError = '';
    let success = false;

    async function login(ev: Event) {
        ev.preventDefault();
        busy.startBusy();
        emailError = '';

        try {
            const response = await sendJsonApiRequest('POST', '/api/users/_login', {
                'type': 'users',
                'attributes': {
                    'email': email
                }
            });
            busy.endBusy();
            if (response.status === 204) {
                success = true;
            } else {
                emailError = 'This e-mail address is not registered or your account has been blocked';
            }
        } catch (error) {
            busy.endBusy();
            emailError = error;
        }
    }
</script>

<article class="md:max-w-2xl mx-auto mb-12">
    {#if success}
        <h1 class="font-blackriver-bold text-4xl mb-8">Logged in to <span class="text-primary">The Old Joke Archive</span></h1>
        <p>You have logged in to The Old Joke Archive. You have been sent a login e-mail. This may have landed in your spam folder.</p>
    {:else}
        <h1 class="font-blackriver-bold text-4xl mb-8">Log in to <span class="text-primary">The Old Joke Archive</span></h1>
        <form on:submit={login}>
            <Input bind:value={email} type="email" error={emailError} disabled={$busy}>E-Mail Address</Input>
            <div class="mt-8 text-right">
                <Button disabled={$busy}>{#if $busy}Logging in...{:else}Log in{/if}</Button>
            </div>
        </form>
    {/if}
</article>
