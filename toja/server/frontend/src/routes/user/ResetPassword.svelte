<script lang="ts">
    import { busy, sendJsonApiRequest } from '../../stores';
    import Input from '../../components/Input.svelte';
    import Button from '../../components/Button.svelte';

    let email = '';
    let emailError = '';
    let complete = false;

    async function login(ev: Event) {
        ev.preventDefault();
        busy.startBusy();
        emailError = '';

        try {
            const response = await sendJsonApiRequest('POST', '/api/users/_reset-password', {
                'type': 'users',
                'attributes': {
                    'email': email,
                }
            });
            busy.endBusy();
            if (response.status === 204) {
                complete = true;
            } else {
                emailError = 'Unfortunately the password could not be reset.';
            }
        } catch (error) {
            busy.endBusy();
            emailError = error;
        }
    }
</script>

<div class="md:max-w-2xl mx-auto">
    <h1 class="font-blackriver-bold text-4xl mb-8">Reset your password for the <span class="text-primary">The Old Joke Archive</span></h1>
    {#if complete}
        <p>Your password has been reset. You will receive an e-mail with a link to reset your password. <span class="text-primary">Please check your spam folder.</span></p>
    {:else}
        <form on:submit={login}>
            <Input bind:value={email} type="email" error={emailError} disabled={$busy}>E-Mail Address</Input>
            <div class="mt-8 text-right">
                <Button disabled={$busy}>{#if $busy}Resetting...{:else}Reset password{/if}</Button>
            </div>
        </form>
    {/if}
</div>
