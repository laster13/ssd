<script lang="ts">
	import { renderMarkdown } from '$lib/utils/markdown';

	let {
		content = '',
		emptyMessage = 'Aucun contenu à prévisualiser.'
	}: {
		content?: string;
		emptyMessage?: string;
	} = $props();

	const html = $derived(renderMarkdown(content));
</script>

<div class="rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
	{#if content.trim()}
		<div class="prose prose-zinc max-w-none dark:prose-invert forum-markdown">
			{@html html}
		</div>
	{:else}
		<p class="text-sm text-zinc-500 dark:text-zinc-400">{emptyMessage}</p>
	{/if}
</div>