<script lang="ts">
	import type { PageData } from './$types';
	import type { LinkCategory } from '$lib/data/stremio-links';

	let { data }: { data: PageData } = $props();

	const categoryLabels: Record<LinkCategory, string> = {
		agrégateurs: 'Agrégateurs',
		catalogues: 'Catalogues',
		'sous-titres': 'Sous-titres',
		guides: 'Guides',
		outils: 'Outils'
	};

	const categories = $derived.by(() => {
		const usedCategories = [...new Set(data.links.map((item) => item.category))] as LinkCategory[];

		return [
			{ key: 'all' as const, label: 'Tout', count: data.links.length },
			...usedCategories.map((category) => ({
				key: category,
				label: categoryLabels[category],
				count: data.links.filter((item) => item.category === category).length
			}))
		];
	});

	let activeCategory = $state<'all' | LinkCategory>('all');
	let query = $state('');
	let copiedUrl = $state<string | null>(null);

	const filteredLinks = $derived.by(() => {
		const q = query.trim().toLowerCase();

		return data.links.filter((item) => {
			const inCategory = activeCategory === 'all' || item.category === activeCategory;
			const inQuery =
				!q ||
				item.title.toLowerCase().includes(q) ||
				item.description.toLowerCase().includes(q) ||
				(item.tags ?? []).some((tag) => tag.toLowerCase().includes(q));

			return inCategory && inQuery;
		});
	});

	const spotlightLink = $derived.by(() => {
		return (
			filteredLinks.find((item) => item.title.toLowerCase() === 'streamfusion') ??
			filteredLinks.find((item) => item.featured) ??
			null
		);
	});

	const remainingLinks = $derived.by(() => {
		if (!spotlightLink) return filteredLinks;
		return filteredLinks.filter((item) => item.title !== spotlightLink.title);
	});

	const groupedLinks = $derived.by(() => {
		const groups = new Map<string, typeof remainingLinks>();

		for (const link of remainingLinks) {
			if (!groups.has(link.category)) groups.set(link.category, []);
			groups.get(link.category)!.push(link);
		}

		return Array.from(groups.entries());
	});

	function categoryLabel(category: LinkCategory) {
		return categoryLabels[category] ?? category;
	}

	async function copyLink(url: string) {
		try {
			await navigator.clipboard.writeText(url);
			copiedUrl = url;
			setTimeout(() => {
				if (copiedUrl === url) copiedUrl = null;
			}, 1800);
		} catch {
			// noop
		}
	}
</script>

<svelte:head>
	<title>Stremio — SSD</title>
	<meta
		name="description"
		content="Un espace clair et premium pour retrouver les liens utiles, filtrer rapidement les addons et accéder aux services essentiels."
	/>
</svelte:head>

<div class="min-h-screen overflow-x-hidden text-zinc-950 dark:text-white">
	<section class="relative overflow-hidden">
		<div
			class="absolute inset-0 -z-30 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.18),transparent_28%),radial-gradient(circle_at_top_right,rgba(168,85,247,0.16),transparent_24%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.10),transparent_28%)]"
		></div>
		<div
			class="absolute inset-0 -z-20 bg-[linear-gradient(180deg,rgba(255,255,255,0.94),rgba(255,255,255,0.72),rgba(255,255,255,0.40),transparent)] dark:bg-[linear-gradient(180deg,rgba(7,17,31,0.92),rgba(7,17,31,0.72),rgba(7,17,31,0.34),transparent)]"
		></div>
		<div
			class="absolute inset-0 -z-10 opacity-[0.20] [background-image:linear-gradient(to_right,rgba(15,23,42,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(15,23,42,0.05)_1px,transparent_1px)] [background-size:36px_36px] dark:opacity-[0.08]"
		></div>

		<div class="mx-auto max-w-7xl py-6 sm:px-6 sm:py-8 lg:px-8">
			<div class="relative px-4 py-5 sm:p-8 lg:p-10 xl:p-12">
				<div class="pointer-events-none absolute inset-0">
					<div
						class="absolute -left-20 top-10 h-52 w-52 rounded-full bg-sky-300/20 blur-3xl dark:bg-sky-400/10"
					></div>
					<div
						class="absolute -right-16 top-24 h-56 w-56 rounded-full bg-violet-300/20 blur-3xl dark:bg-violet-400/10"
					></div>
					<div
						class="absolute bottom-0 left-1/3 h-44 w-44 rounded-full bg-emerald-300/20 blur-3xl dark:bg-emerald-400/10"
					></div>
				</div>

				<div class="relative max-w-4xl">
					<div class="flex flex-wrap items-center gap-3">
						<div
							class="inline-flex items-center gap-2 rounded-full border border-sky-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 shadow-[0_10px_24px_rgba(14,165,233,0.08)] dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300 dark:shadow-none"
						>
							<span class="h-2 w-2 rounded-full bg-sky-500"></span>
							Stremio
						</div>

						<div
							class="inline-flex items-center gap-2 rounded-full border border-violet-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 shadow-[0_10px_24px_rgba(139,92,246,0.10)] dark:border-violet-400/20 dark:bg-violet-400/[0.10] dark:text-violet-200 dark:shadow-none"
						>
							Centre de liens
						</div>
					</div>

					<h1
						class="mt-6 max-w-4xl text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white sm:text-3xl lg:text-[2.4rem] lg:leading-[1.08]"
					>
						Une sélection
						<span class="bg-[linear-gradient(90deg,#0ea5e9_0%,#2563eb_28%,#8b5cf6_62%,#10b981_100%)] bg-clip-text text-transparent">
							claire pour retrouver tes liens essentiels.
						</span>
					</h1>

					<p class="mt-6 max-w-2xl text-base leading-8 text-zinc-600 dark:text-zinc-300">
						Retrouve les agrégateurs, catalogues et outils dans une interface plus lisible,
						filtrable et pensée pour aller droit à l’essentiel.
					</p>
				</div>
			</div>

			{#if spotlightLink}
				<div class="mt-4">
					<div
						class="relative overflow-hidden border-y border-black/5 bg-white/80 p-6 dark:border-white/10 dark:bg-white/[0.05] sm:rounded-[30px] sm:border sm:shadow-[0_24px_60px_rgba(15,23,42,0.08)] dark:sm:shadow-[0_18px_50px_rgba(0,0,0,0.24)] sm:p-8"
					>
						<div
							class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.08),rgba(59,130,246,0.05),rgba(168,85,247,0.08))]"
						></div>
						<div
							class="pointer-events-none absolute -right-10 top-0 h-44 w-44 rounded-full bg-sky-300/20 blur-3xl dark:bg-sky-400/10"
						></div>

						<div class="relative">
							<div class="grid gap-3 md:grid-cols-2">
								<div
									class="rounded-[22px] border border-black/5 bg-white/78 p-5 shadow-[0_16px_34px_rgba(15,23,42,0.05)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-none"
								>
									<div
										class="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:text-zinc-400"
									>
										Pourquoi lui
									</div>
									<div class="mt-3 space-y-3 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
										<p>
											Stream Fusion Reborn est un addon Stremio haute performance pour la
											communauté francophone. Il agrège les sources debrid et les indexeurs
											torrents, optimise la recherche via un cache multi-couches (Redis,
											PostgreSQL, Meilisearch, DuckDB), et permet le partage inter-instances
											crypté via le protocole de peering.
										</p>
									</div>
								</div>

								<div
									class="rounded-[22px] border border-black/5 bg-white/78 p-5 shadow-[0_16px_34px_rgba(15,23,42,0.05)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-none"
								>
									<div
										class="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:text-zinc-400"
									>
										Accès rapide
									</div>
									<div class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
										Conçu pour la scalabilité (4 replicas, PgBouncer, sticky sessions), il
										intègre un pipeline de recherche multi-phases, un matching TMDB/IMDB
										automatique, la détection TRUEFRENCH/VFF/VOSTFR, et un panneau
										d'administration complet.
									</div>
								</div>
							</div>

							<div class="mt-8 flex flex-wrap items-center gap-2">
								<span
									class="inline-flex items-center rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300"
								>
									Produit phare
								</span>

								{#if spotlightLink.status}
									<span
										class="inline-flex items-center rounded-full border border-black/10 bg-white/80 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.06] dark:text-zinc-300"
									>
										{spotlightLink.status}
									</span>
									<a
										href="https://discord.gg/r3Nw4GAkJG"
										target="_blank"
										rel="noreferrer"
										class="group inline-flex items-center gap-2 rounded-full border border-violet-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 shadow-[0_10px_24px_rgba(139,92,246,0.10)] transition-all duration-300 hover:-translate-y-0.5 hover:border-violet-300 hover:bg-white hover:shadow-[0_14px_30px_rgba(139,92,246,0.16)] dark:border-violet-400/20 dark:bg-violet-400/[0.10] dark:text-violet-200 dark:shadow-none dark:hover:border-violet-400/30 dark:hover:bg-violet-400/[0.14]"
									>
										<svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor" aria-hidden="true">
											<path
												d="M20.317 4.369A19.791 19.791 0 0 0 15.885 3c-.191.328-.403.77-.554 1.116a18.27 18.27 0 0 0-5.487 0A12.64 12.64 0 0 0 9.29 3a19.736 19.736 0 0 0-4.438 1.372C2.05 8.554 1.288 12.633 1.67 16.656a19.9 19.9 0 0 0 5.993 3.03c.482-.662.91-1.361 1.279-2.092a12.96 12.96 0 0 1-2.013-.97c.168-.123.332-.252.49-.385 3.88 1.823 8.09 1.823 11.924 0 .16.133.324.262.492.385a12.9 12.9 0 0 1-2.017.972c.37.729.797 1.428 1.28 2.09a19.86 19.86 0 0 0 6-3.03c.447-4.663-.762-8.705-3.776-12.287ZM9.75 14.23c-1.165 0-2.124-1.06-2.124-2.362 0-1.303.94-2.364 2.124-2.364 1.193 0 2.143 1.07 2.124 2.364 0 1.302-.94 2.362-2.124 2.362Zm4.5 0c-1.165 0-2.124-1.06-2.124-2.362 0-1.303.94-2.364 2.124-2.364 1.193 0 2.143 1.07 2.124 2.364 0 1.302-.94 2.362-2.124 2.362Z"
											/>
										</svg>
										<span>Discord</span>
										<span class="transition-transform duration-300 group-hover:translate-x-0.5">↗</span>
									</a>
								{/if}
							</div>

							<h2
								class="mt-5 text-3xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white sm:text-4xl"
							>
								{spotlightLink.title}
							</h2>

							<p class="mt-4 max-w-2xl text-base leading-8 text-zinc-600 dark:text-zinc-300">
								{spotlightLink.description}
							</p>

							{#if spotlightLink.tags?.length}
								<div class="mt-6 flex flex-wrap gap-2">
									{#each spotlightLink.tags as tag}
										<span
											class="rounded-full border border-black/8 bg-white/85 px-3 py-1.5 text-xs font-medium text-zinc-700 shadow-sm dark:border-white/10 dark:bg-white/[0.06] dark:text-zinc-200"
										>
											#{tag}
										</span>
									{/each}
								</div>
							{/if}

							<div class="mt-8 flex flex-col gap-3 sm:flex-row">
								<a
									href={spotlightLink.url}
									target={spotlightLink.internal ? undefined : '_blank'}
									rel={spotlightLink.internal ? undefined : 'noreferrer'}
									class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
								>
									Ouvrir StreamFusion
								</a>

								<button
									type="button"
									on:click={() => copyLink(spotlightLink.url)}
									class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
								>
									{copiedUrl === spotlightLink.url ? 'Lien copié' : 'Copier le lien'}
								</button>
							</div>
						</div>
					</div>
				</div>
			{/if}

			<div class="px-4 pb-6 pt-4 sm:px-0">
				<div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
					<div class="flex flex-wrap gap-2">
						{#each categories as category}
							<button
								type="button"
								on:click={() => (activeCategory = category.key)}
								class={`inline-flex items-center rounded-full px-4 py-2.5 text-sm font-medium transition ${
									activeCategory === category.key
										? 'border border-zinc-950 bg-zinc-950 text-white shadow-[0_10px_24px_rgba(15,23,42,0.14)] dark:border-white dark:bg-white dark:text-zinc-950 dark:shadow-none'
										: 'border border-black/10 bg-white/88 text-zinc-700 hover:-translate-y-0.5 hover:bg-white dark:border-white/10 dark:bg-white/[0.06] dark:text-zinc-200 dark:hover:bg-white/[0.10]'
								}`}
							>
								<span>{category.label}</span>
								<span class="ml-2 opacity-65">{category.count}</span>
							</button>
						{/each}
					</div>

					<div class="w-full xl:max-w-md">
						<div class="relative">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
								<svg
									viewBox="0 0 24 24"
									class="h-4 w-4 text-zinc-400 dark:text-zinc-500"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									aria-hidden="true"
								>
									<circle cx="11" cy="11" r="7"></circle>
									<path d="m20 20-3.5-3.5"></path>
								</svg>
							</div>

							<input
								bind:value={query}
								type="search"
								placeholder="Rechercher un lien, un tag, un usage…"
								class="w-full rounded-[18px] border border-black/10 bg-white/88 py-3 pl-11 pr-4 text-sm text-zinc-900 outline-none shadow-[0_10px_24px_rgba(15,23,42,0.04)] placeholder:text-zinc-400 focus:border-black/20 dark:border-white/10 dark:bg-white/[0.06] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:shadow-none"
							/>
						</div>
					</div>
				</div>
			</div>

			<div class="pb-6">
				{#if !spotlightLink && filteredLinks.length === 0}
					<div
						class="border-y border-dashed border-black/10 bg-white/70 px-6 py-14 text-center text-zinc-500 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 sm:rounded-[28px] sm:border"
					>
						Aucun résultat pour ce filtre.
					</div>
				{:else if groupedLinks.length === 0}
					<div
						class="border-y border-dashed border-black/10 bg-white/70 px-6 py-14 text-center text-zinc-500 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 sm:rounded-[28px] sm:border"
					>
						Aucun autre lien pour ce filtre.
					</div>
				{:else}
					<div class="space-y-10">
						{#each groupedLinks as [groupName, items]}
							<div>
								<div class="mb-4 flex items-center justify-between gap-4 px-4 sm:px-0">
									<div>
										<h3
											class="text-2xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white"
										>
											{categoryLabel(groupName as LinkCategory)}
										</h3>
									</div>

									<div class="text-sm text-zinc-500 dark:text-zinc-400">{items.length} lien(s)</div>
								</div>

								<div class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
									{#each items as item}
										<article
											class="group relative overflow-hidden border-y border-black/5 bg-white/80 p-6 transition-all duration-300 dark:border-white/10 dark:bg-white/[0.045] sm:rounded-[28px] sm:border sm:shadow-[0_18px_40px_rgba(15,23,42,0.06)] sm:hover:-translate-y-1 sm:hover:shadow-[0_24px_52px_rgba(15,23,42,0.10)] dark:sm:shadow-none"
										>
											<div
												class="pointer-events-none absolute inset-x-0 top-0 h-1 bg-[linear-gradient(90deg,rgba(34,211,238,0.90),rgba(96,165,250,0.88),rgba(168,85,247,0.90))] opacity-0 transition-opacity duration-300 group-hover:opacity-100"
											></div>

											<div class="flex items-start justify-between gap-4">
												<div>
													<div class="flex flex-wrap items-center gap-2">
														<h4 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
															{item.title}
														</h4>

														{#if item.status}
															<span
																class="rounded-full border border-black/10 bg-white/80 px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.06] dark:text-zinc-300"
															>
																{item.status}
															</span>
														{/if}
													</div>

													<p class="mt-4 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
														{item.description}
													</p>
												</div>
											</div>

											{#if item.tags?.length}
												<div class="mt-5 flex flex-wrap gap-2">
													{#each item.tags as tag}
														<span
															class="rounded-full bg-black/[0.04] px-2.5 py-1 text-xs text-zinc-600 dark:bg-white/8 dark:text-zinc-300"
														>
															#{tag}
														</span>
													{/each}
												</div>
											{/if}

											<div class="mt-6 flex flex-col gap-3 sm:flex-row">
												<a
													href={item.url}
													target={item.internal ? undefined : '_blank'}
													rel={item.internal ? undefined : 'noreferrer'}
													class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-4 py-2.5 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.26)] dark:border-white/10"
												>
													Ouvrir
												</a>

												<button
													type="button"
													on:click={() => copyLink(item.url)}
													class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.05)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.16)]"
												>
													{copiedUrl === item.url ? 'Lien copié' : 'Copier le lien'}
												</button>
											</div>
										</article>
									{/each}
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>
	</section>
</div>