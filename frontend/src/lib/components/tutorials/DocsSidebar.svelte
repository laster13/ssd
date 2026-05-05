<script lang="ts">
	import type { DocsNavGroup } from '$lib/data/tutorials';

	let {
		groups
	}: {
		groups: DocsNavGroup[];
	} = $props();
</script>

<aside class="space-y-3">
	<div class="px-2">
		<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-zinc-500 dark:text-zinc-400">
			Navigation
		</p>
	</div>

	<a
		href="/forum"
		class="group flex min-w-0 items-center justify-between rounded-2xl border border-violet-200 bg-violet-50 px-4 py-3 text-sm font-semibold text-violet-700 transition hover:border-violet-300 hover:bg-violet-100 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300 dark:hover:border-violet-500/30 dark:hover:bg-violet-500/15"
	>
		<span class="min-w-0 truncate">Espace de discussion</span>
		<span
			class="ml-3 shrink-0 transition-transform duration-200 group-hover:translate-x-0.5"
			aria-hidden="true"
		>
			→
		</span>
	</a>

	{#each groups as group}
		<section class="rounded-2xl border border-zinc-200 bg-zinc-50/80 p-3 dark:border-zinc-800 dark:bg-zinc-950/40">
			<h2
				class="px-2 text-sm font-semibold tracking-tight text-zinc-900 dark:text-zinc-100"
			>
				<span class="break-words bg-gradient-to-r from-sky-500 via-blue-600 to-violet-600 bg-clip-text text-transparent">
					{group.name}
				</span>
			</h2>

			<div class="mt-3 space-y-3">
				{#each group.categories as category}
					<div>
						<h3
							class="break-words px-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400"
						>
							{category.name}
						</h3>

						<nav class="mt-2 space-y-1">
							{#each category.items as item}
								<a
									href={`/tutos/${item.slug}`}
									class="group flex min-w-0 items-center justify-between rounded-xl px-3 py-2 text-sm text-zinc-600 transition hover:bg-white hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-900 dark:hover:text-zinc-100"
								>
									<span class="min-w-0 truncate">{item.title}</span>
									<span
										class="ml-3 shrink-0 text-zinc-400 transition-transform duration-200 group-hover:translate-x-0.5 dark:text-zinc-500"
									>
										→
									</span>
								</a>
							{/each}
						</nav>
					</div>
				{/each}
			</div>
		</section>
	{/each}
</aside>