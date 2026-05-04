<script lang="ts">
	import { onMount } from 'svelte';

	let {
		link,
		enabled = true
	}: {
		link: string;
		enabled?: boolean;
	} = $props();

	onMount(async () => {
		if (!enabled || !link) return;

		try {
			await fetch('/api/notifications/mark-link-read', {
				method: 'POST',
				headers: {
					'content-type': 'application/json'
				},
				body: JSON.stringify({ link })
			});
		} catch {
			// noop
		}
	});
</script>