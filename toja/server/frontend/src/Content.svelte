<script lang="ts">
	import { Route, useLocation } from "svelte-navigator";
    import { tick, onDestroy } from "svelte";

    import { isGroupAdminUsers } from './stores';
    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import Loading from './components/Loading.svelte';
    import Home from './routes/Home.svelte';
    import Signup from './routes/user/Signup.svelte';
    import Login from './routes/user/Login.svelte';
    import ResetPassword from './routes/user/ResetPassword.svelte';
    import Confirm from './routes/user/Confirm.svelte';
    import Contribute from './routes/contribute/Contribute.svelte';

    const location = useLocation();
    let Admin = null;
    let Workbench = null;
    const unsubscribeLocation = location.subscribe((location) => {
        if (location.pathname.startsWith('/admin')) {
            if (Admin === null) {
                import('./routes/Admin.svelte').then((mod) => {
                    Admin = mod.default;
                    tick().then(() => {
                        const elem = document.querySelector('h1');
                        if (elem) {
                            elem.focus();
                        }
                    });
                });
            }
        } else if (location.pathname === '/contribute/workbench') {
            import('./routes/contribute/Workbench.svelte').then((mod) => {
                Workbench = mod.default;
                tick().then(() => {
                    const elem = document.querySelector('h1');
                    if (elem) {
                        elem.focus();
                    }
                });
            });
        }
    });

    onDestroy(unsubscribeLocation);
</script>

<Header/>
<article class="container mx-auto mb-12">
    <Route path="/"><Home/></Route>
    <Route path="/user/sign-up"><Signup/></Route>
    <Route path="/user/confirm"><Confirm/></Route>
    <Route path="/user/log-in"><Login/></Route>
    <Route path="/user/reset-password"><ResetPassword/></Route>
    {#if $isGroupAdminUsers}
        <Route path="/admin/*">{#if Admin}<svelte:component this={Admin}/>{:else}<Loading/>{/if}</Route>
    {/if}
    <Route path="/contribute"><Contribute/></Route>
    <Route path="/contribute/workbench">{#if Workbench}<svelte:component this={Workbench}/>{:else}<Loading/>{/if}</Route>
</article>
<Footer/>
