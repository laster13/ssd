<script lang="ts">
	let {
		count = 0,
		className = ''
	}: {
		count?: number;
		className?: string;
	} = $props();
</script>

<a
	href="/notifications"
	class={`relative inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-zinc-300 bg-white text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800 ${className}`}
	aria-label="Notifications"
	title="Notifications"
>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 24 24"
		fill="none"
		stroke="currentColor"
		stroke-width="1.8"
		stroke-linecap="round"
		stroke-linejoin="round"
		class="h-5 w-5"
	>
		<path d="M6 8a6 6 0 1 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
		<path d="M10.3 21a2 2 0 0 0 3.4 0" />
	</svg>

	{#if count > 0}
		<span
			class="absolute -right-1.5 -top-1.5 inline-flex min-h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1.5 text-[11px] font-semibold leading-none text-white"
		>
			{count > 99 ? '99+' : count}
		</span>
	{/if}
</a>