<script lang="ts">
	let { data } = $props();
</script>

<h1>Interface</h1>

{#if data.user}
	<p>Bienvenue {data.user.email}</p>
{:else}
	<p>Vous n'êtes pas connecté.</p>
{/if}