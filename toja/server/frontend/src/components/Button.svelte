<script lang="ts">
    export let disabled = false;
</script>

<button class="inline-block {disabled ? 'bg-gray-200 text-black cursor-not-allowed' : 'bg-primary text-white italic hover:bg-accent'} transition-colors text-sm font-bold rounded-full px-6 py-3" disabled={disabled}><slot></slot></button>
