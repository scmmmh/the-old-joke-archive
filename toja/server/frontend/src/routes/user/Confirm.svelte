<script lang="ts">
    import { useNavigate } from 'svelte-navigator';

    import { saveJsonApiObject, authToken, authUser, busy } from '../../stores';
    import { sessionStoreValue, localDeleteValue, sessionDeleteValue } from '../../local-persistence';
    import Input from '../../components/Input.svelte';
    import Button from '../../components/Button.svelte';

    const navigate = useNavigate();
    let step = 1;
    let password = '';
    let confirmPassword = '';
    let passwordError = '';

    const params = new URLSearchParams(window.location.search);
    if (params.get('token') && params.get('id')) {
        confirm_step(params);
    }

    const action = params.get('action');

    async function confirm_step(params) {
        busy.startBusy();
        try {
            localDeleteValue('auth');
            sessionDeleteValue('auth');
            authToken.set(params.get('id') + '$$' + params.get('token'));
            const response = await saveJsonApiObject({
                'type': 'users',
                'id': params.get('id'),
                'attributes': {
                }
            });
            sessionStoreValue('auth', {id: params.get('id'), token: params.get('token')});
            step = 2;
            busy.endBusy();
        } catch (error) {
            step = 3;
            busy.endBusy();
        }
    }

    async function setPassword(ev: Event) {
        ev.preventDefault();
        passwordError = '';
        if (password === confirmPassword) {
            try {
                authToken.set(params.get('id') + '$$' + params.get('token'));
                const user = await saveJsonApiObject({
                    type: 'users',
                    id: params.get('id'),
                    attributes: {
                        password: password,
                    }
                });
                authUser.set(user);
                busy.endBusy();
                navigate('/');
            } catch (error) {
                passwordError = error.errors[0].title;
                busy.endBusy();
            }
        } else {
            passwordError = 'The two passwords do not match.';
        }
    }
</script>

<div class="md:max-w-2xl mx-auto">
    {#if step === 1}
        <h1 class="font-blackriver-bold text-4xl mb-8">{#if action === 'password-reset'}Resetting your password for{:else}Confirming your account with{/if} <span class="text-primary">The Old Joke Archive</span></h1>
        <p>{#if action === 'password-reset'}Your password is being reset.{:else}Your account is being confirmed.{/if} Please wait...</p>
    {:else if step === 2}
        <h1 class="font-blackriver-bold text-4xl mb-8"><span class="text-primary">The Old Joke Archive</span> {#if action === 'password-reset'}password reset{:else}account confirmed{/if}</h1>
        <p>{#if action === 'password-reset'}Your password has been reset.{:else}Your account has been confirmed{/if}. Please set your password:</p>
        <form on:submit={setPassword}>
            <Input type="password" bind:value={password} error={passwordError}>Password</Input>
            <Input type="password" bind:value={confirmPassword} error={passwordError}>Confirm Password</Input>
            <div class="text-right">
                <Button>{#if $busy}Setting your password{:else}Set your password{/if}</Button>
            </div>
        </form>
    {:else if step === 3}
        <h1 class="font-blackriver-bold text-4xl mb-8"><span class="text-primary">The Old Joke Archive</span> account confirmation failed</h1>
        <p>The account confirmation failed. Either the account does not exist, is blocked, or the sign-up token is no longer valid.</p>
    {/if}
</div>
