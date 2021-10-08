<script lang="ts">
    import { useNavigate } from 'svelte-navigator';

    import { busy, sendJsonApiRequest, authToken, authUser } from '../stores';
    import { localStoreValue, sessionStoreValue } from '../local-persistence';
    import Input from '../components/Input.svelte';
    import Button from '../components/Button.svelte';

    let email = '';
    let emailError = '';
    let success = false;
    const navigate = useNavigate();

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
                emailError = 'This e-mail address is not registered or the token is no longer valid';
            }
        } catch (error) {
            busy.endBusy();
            emailError = error;
        }
    }

    async function login_step2(params: URLSearchParams) {
        email = params.get('email');
        busy.startBusy();
        try {
            const response = await sendJsonApiRequest('POST', '/api/users/_login', {
                'type': 'users',
                'attributes': {
                    'email': email,
                    'token': params.get('token')
                }
            });
            busy.endBusy();
            if (response.status === 200) {
                const obj = await response.json();
                authUser.set(obj.data);
                authToken.set(obj.data.id + '$$' + params.get('token'));
                localStoreValue('auth', {id: obj.data.id, token: params.get('token')});
                navigate('/');
            } else {
                emailError = 'The e-mail address does not exist or the token is no longer valid';
            }
        } catch (error) {
            busy.endBusy();
            emailError = error;
        }
    }

    const params = new URLSearchParams(window.location.search);
    if (params.get('token') && params.get('email')) {
        login_step2(params);
    }
</script>

<article class="md:max-w-2xl mx-auto mb-12">
    {#if success}
        <h1 class="font-blackriver-bold text-4xl mb-8">Logged in to <span class="text-primary">The Old Joke Archive</span></h1>
        <p>You are being logged into The Old Joke Archive. You have been sent an e-mail with an access link. This is not a joke and it may have landed in your spam folder.</p>
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
