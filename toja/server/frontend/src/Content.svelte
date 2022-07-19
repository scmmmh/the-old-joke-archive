<script lang="ts">
	import { Route, useLocation } from "svelte-navigator";
    import { tick, onDestroy } from "svelte";

    import { isGroupAdmin, isGroupAdminUsers, isGroupEditor, isGroupDataProvider } from './stores';
    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import Loading from './components/Loading.svelte';
    import Dialog from './components/Dialog.svelte';
    import Home from './routes/Home.svelte';
    import Signup from './routes/user/Signup.svelte';
    import Login from './routes/user/Login.svelte';
    import ResetPassword from './routes/user/ResetPassword.svelte';
    import Confirm from './routes/user/Confirm.svelte';
    import Contribute from './routes/contribute/Contribute.svelte';
    import Search from './routes/explore/Search.svelte';
    import Joke from './routes/explore/Joke.svelte';

    const location = useLocation();
    let Admin = null;
    let Workbench = null;
    let DataProvision = null;

    function focusHeader() {
        const elem = document.querySelector('h1');
        if (elem) {
            elem.focus();
        }
    }

    const unsubscribeLocation = location.subscribe((location) => {
        if (location.pathname.startsWith('/admin')) {
            if (Admin === null) {
                import('./routes/Admin.svelte').then((mod) => {
                    Admin = mod.default;
                    tick().then(focusHeader);
                });
            }
        } else if (location.pathname === '/contribute/workbench') {
            import('./routes/contribute/Workbench.svelte').then((mod) => {
                Workbench = mod.default;
                tick().then(focusHeader);
            });
        } else if (location.pathname.startsWith('/contribute/data')) {
            import('./routes/contribute/DataProvision.svelte').then((mod) => {
                DataProvision = mod.default;
                tick().then(focusHeader);
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
    <Route path="/search"><Search/></Route>
    <Route path="/jokes/:joke_id"><Joke/></Route>
    {#if $isGroupAdmin || $isGroupAdminUsers}
        <Route path="/admin/*">{#if Admin}<svelte:component this={Admin}/>{:else}<Loading/>{/if}</Route>
    {/if}
    <Route path="/contribute"><Contribute/></Route>
    {#if $isGroupEditor}
        <Route path="/contribute/workbench">{#if Workbench}<svelte:component this={Workbench}/>{:else}<Loading/>{/if}</Route>
    {/if}
    {#if $isGroupDataProvider}
        <Route path="/contribute/data">{#if DataProvision}<svelte:component this={DataProvision}/>{:else}<Loading/>{/if}</Route>
    {/if}
    <Dialog/>
</article>
<Footer/>
