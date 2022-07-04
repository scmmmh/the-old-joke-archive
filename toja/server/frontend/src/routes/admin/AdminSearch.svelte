<script lang="ts">
    import { get } from 'svelte/store';

    import { getCookie } from '../../stores/jsonapi';
    import { authToken } from '../../stores';

    async function reIndex() {
        const response = await window.fetch('/api/admin/search', {
            method: 'POST',
            body: JSON.stringify({'action': 're-index'}),
            headers: {
                'Content-Type': 'application/json',
                'X-XSRFToken': getCookie('_xsrf'),
                'X-Toja-Auth': get(authToken)
            }
        });
    }
</script>

<h2 class="sr-only">Search Administration</h2>

<button class="text-accent" on:click={reIndex}>Re-index all published jokes</button>
