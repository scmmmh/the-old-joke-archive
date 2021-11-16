<script lang="ts">
    import { useNavigate } from 'svelte-navigator';

    import { busy, sendJsonApiRequest, authToken, authUser, getJsonApiObject } from '../stores';
    import { localStoreValue, sessionStoreValue, localDeleteValue, sessionDeleteValue } from '../local-persistence';
    import Input from '../components/Input.svelte';
    import Button from '../components/Button.svelte';

    let email = '';
    let emailError = '';
    let password = '';
    let passwordError = '';
    let remember = false;
    const navigate = useNavigate();

    async function login(ev: Event) {
        ev.preventDefault();
        busy.startBusy();
        emailError = '';

        try {
            const response = await sendJsonApiRequest('POST', '/api/users/_login', {
                'type': 'users',
                'attributes': {
                    'email': email,
                    'password': password,
                }
            });
            busy.endBusy();
            if (response.status === 200) {
                localDeleteValue('auth');
                sessionDeleteValue('auth');
                const obj = await response.json();
                authToken.set(obj.data.id + '$$' + obj.data.attributes.token);
                const user = await getJsonApiObject('users', obj.data.id);
                authUser.set(user);
                if (remember) {
                    localStoreValue('auth', {
                        id: user.id,
                        token: obj.data.attributes.token,
                    });
                } else {
                    sessionStoreValue('auth', {
                        id: user.id,
                        token: obj.data.attributes.token,
                    });
                }
                navigate('/');
            } else {
                emailError = 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.';
                passwordError = 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.';
            }
        } catch (error) {
            busy.endBusy();
            emailError = error;
            passwordError = error;
        }
    }
</script>

<div class="md:max-w-2xl mx-auto">
    <h1 class="font-blackriver-bold text-4xl mb-8">Log in to <span class="text-primary">The Old Joke Archive</span></h1>
    <form on:submit={login}>
        <Input bind:value={email} type="email" error={emailError} disabled={$busy}>E-Mail Address</Input>
        <Input bind:value={password} type="password" error={passwordError} disabled={$busy}>Password</Input>
        <Input bind:value={remember} type="checkbox" disabled={$busy}>Remember me <span class="text-sm">(do not select this on a shared or public system)</span></Input>
        <div class="mt-8 text-right">
            <Button disabled={$busy}>{#if $busy}Logging in...{:else}Log in{/if}</Button>
        </div>
    </form>
</div>
