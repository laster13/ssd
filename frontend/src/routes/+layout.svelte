<script lang="ts">
	import '../app.css';
	import AppHeader from '$lib/components/layout/AppHeader.svelte';

	let { data, children } = $props();
</script>

<svelte:head>
	<title>SSD</title>
</svelte:head>

<div class="min-h-screen bg-[#f8fafc] text-zinc-900 dark:bg-[#06070b] dark:text-zinc-100">
	<AppHeader
		user={data.user}
		csrfToken={data.csrfToken}
		pathname={data.pathname ?? '/'}
	/>

	<main class="px-4 pb-10 sm:px-6 lg:px-8">
		{@render children()}
	</main>
</div>