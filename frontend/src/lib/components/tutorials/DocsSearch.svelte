<script lang="ts">
	import type { Tutorial } from '$lib/data/tutorials';

	let {
		tutorials
	}: {
		tutorials: Tutorial[];
	} = $props();

	let query = $state('');

	const normalizedQuery = $derived(query.trim().toLowerCase());

	const results = $derived.by(() => {
		if (!normalizedQuery) return [];

		return tutorials
			.filter((tutorial) => {
				const title = tutorial.title?.toLowerCase() ?? '';
				const description = tutorial.description?.toLowerCase() ?? '';
				const category = tutorial.category?.toLowerCase() ?? '';
				const level = tutorial.level?.toLowerCase() ?? '';

				return (
					title.includes(normalizedQuery) ||
					description.includes(normalizedQuery) ||
					category.includes(normalizedQuery) ||
					level.includes(normalizedQuery)
				);
			})
			.slice(0, 8);
	});
</script>

<div class="rounded-[1.4rem] border border-zinc-200 bg-white p-3 dark:border-zinc-800 dark:bg-zinc-900">
	<div class="flex items-center gap-2 px-1 pb-2">
		<div class="h-2.5 w-2.5 rounded-full bg-gradient-to-br from-sky-500 to-violet-500"></div>
		<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-zinc-500 dark:text-zinc-400">
			Recherche
		</p>
	</div>

	<div class="relative">
		<div class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500">
			<svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" aria-hidden="true">
				<circle cx="11" cy="11" r="6.5" stroke="currentColor" stroke-width="1.8" />
				<path d="M16 16L21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
			</svg>
		</div>

		<input
			bind:value={query}
			type="search"
			placeholder="Rechercher un tutoriel..."
			class="w-full rounded-2xl border border-zinc-200 bg-zinc-50 py-3 pl-11 pr-10 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-sky-300 focus:bg-white dark:border-zinc-700 dark:bg-zinc-950 dark:text-zinc-100 dark:placeholder:text-zinc-500 dark:focus:border-sky-500/40"
		/>

		{#if query}
			<button
				type="button"
				onclick={() => (query = '')}
				aria-label="Effacer la recherche"
				class="absolute right-3 top-1/2 inline-flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-full text-zinc-400 transition hover:bg-zinc-200/70 hover:text-zinc-700 dark:text-zinc-500 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
			>
				✕
			</button>
		{/if}
	</div>

	{#if normalizedQuery}
		<div class="mt-3 rounded-2xl border border-zinc-200 bg-zinc-50/70 p-2 dark:border-zinc-800 dark:bg-zinc-950/50">
			{#if results.length > 0}
				<div class="mb-2 px-2">
					<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
						{results.length} résultat{results.length > 1 ? 's' : ''}
					</p>
				</div>

				<div class="space-y-1">
					{#each results as tutorial}
						<a
							href={`/tutos/${tutorial.slug}`}
							class="group block rounded-xl px-3 py-3 transition hover:bg-white dark:hover:bg-zinc-900"
						>
							<div class="flex items-start justify-between gap-3">
								<div class="min-w-0">
									<p class="truncate text-sm font-semibold text-zinc-900 group-hover:text-sky-700 dark:text-zinc-100 dark:group-hover:text-sky-300">
										{tutorial.title}
									</p>

									{#if tutorial.description}
										<p class="mt-1 line-clamp-2 text-xs leading-5 text-zinc-500 dark:text-zinc-400">
											{tutorial.description}
										</p>
									{/if}

									<div class="mt-2 flex flex-wrap items-center gap-2 text-[11px]">
										{#if tutorial.category}
											<span class="rounded-full border border-violet-200 bg-violet-50 px-2 py-0.5 text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300">
												{tutorial.category}
											</span>
										{/if}

										{#if tutorial.level}
											<span class="rounded-full border border-sky-200 bg-sky-50 px-2 py-0.5 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300">
												{tutorial.level}
											</span>
										{/if}
									</div>
								</div>

								<span class="shrink-0 text-zinc-400 transition-transform duration-200 group-hover:translate-x-0.5 dark:text-zinc-500">
									→
								</span>
							</div>
						</a>
					{/each}
				</div>
			{:else}
				<div class="px-3 py-4">
					<p class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Aucun tutoriel trouvé
					</p>
					<p class="mt-1 text-xs leading-5 text-zinc-500 dark:text-zinc-400">
						Essaie avec un autre mot-clé, une catégorie ou un niveau.
					</p>
				</div>
			{/if}
		</div>
	{:else}
		<div class="mt-3 px-1">
			<p class="text-xs leading-5 text-zinc-500 dark:text-zinc-400">
				Recherche par titre, description, catégorie ou niveau.
			</p>
		</div>
	{/if}
</div>