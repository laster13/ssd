<script lang="ts">
	import { renderMarkdown } from '$lib/utils/markdown';

	let {
		content,
		className = ''
	}: {
		content: string;
		className?: string;
	} = $props();

	const html = $derived(renderMarkdown(content));
</script>

<div class={`prose prose-zinc max-w-none dark:prose-invert forum-markdown ${className}`}>
	{@html html}
</div>