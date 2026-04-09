<script lang="ts">
	import AppCard from '$lib/components/store/AppCard.svelte';
	import { page } from '$app/state';

	let { data } = $props();

	let query = $state('');
	let sortBy = $state<'catalog' | 'az'>('catalog');

	const initialCategory = $derived(page.url.searchParams.get('category') ?? 'Tous');
	let activeCategory = $state('Tous');

	const isAuthenticated = $derived(Boolean(data.user));

	$effect(() => {
		activeCategory = initialCategory;
	});

	const apps = $derived(
		(data.apps ?? []).map((app: any, index: number) => ({
			...app,
			name: app.name ?? 'Application',
			slug: app.slug ?? '',
			description: app.description ?? '',
			tagline: app.tagline ?? app.description ?? '',
			category: app.category ?? 'Autre',
			status: app.status ?? 'Disponible',
			order: index
		}))
	);

	const categories = $derived([
		'Tous',
		...new Set(
			apps
				.map((app) => app.category)
				.filter(Boolean)
				.sort((a, b) => a.localeCompare(b, 'fr'))
		)
	]);

	const filteredApps = $derived.by(() => {
		const q = query.trim().toLowerCase();

		let list = apps.filter((app) => {
			const matchesCategory = activeCategory === 'Tous' || app.category === activeCategory;

			const matchesQuery =
				!q ||
				app.name.toLowerCase().includes(q) ||
				app.slug.toLowerCase().includes(q) ||
				app.description.toLowerCase().includes(q) ||
				app.tagline.toLowerCase().includes(q) ||
				app.category.toLowerCase().includes(q);

			return matchesCategory && matchesQuery;
		});

		if (sortBy === 'az') {
			list = [...list].sort((a, b) => a.name.localeCompare(b.name, 'fr'));
		} else {
			list = [...list].sort((a, b) => a.order - b.order);
		}

		return list;
	});
</script>

<svelte:head>
	<title>Bibliothèque d’applications</title>
</svelte:head>

<div class="min-h-screen bg-[#f8fafc] text-zinc-900 dark:bg-[#06070b] dark:text-zinc-100">
	<div class="pointer-events-none fixed inset-0">
		<div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(15,23,42,0.03),transparent_35%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.03),transparent_35%)]"></div>
		<div class="absolute left-[10%] top-0 h-[380px] w-[380px] rounded-full bg-cyan-500/10 blur-3xl dark:bg-cyan-500/[0.04]"></div>
		<div class="absolute right-[10%] top-0 h-[380px] w-[380px] rounded-full bg-violet-500/10 blur-3xl dark:bg-violet-500/[0.04]"></div>
	</div>

	<div class="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<header class="mb-5 overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.34)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.75),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.035),rgba(255,255,255,0.01))]"></div>

				<div class="relative p-5 sm:p-6">
					<div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
						<div>
							<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
								<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
								Library
							</div>

							<h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
								<span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
									Bibliothèque complète
								</span>
							</h1>

							<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
								Accède à tout le catalogue avec recherche, tri et filtres.
							</p>
						</div>

						{#if !isAuthenticated}
							<div class="rounded-full border border-amber-300/40 bg-amber-100/70 px-4 py-2 text-xs font-semibold text-amber-800 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-200">
								Mode visiteur · installation désactivée
							</div>
						{/if}
					</div>

					<div class="mt-5 flex flex-col gap-3 lg:flex-row lg:items-center">
						<div class="relative min-w-0 flex-1">
							<svg
								viewBox="0 0 24 24"
								class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<circle cx="11" cy="11" r="7"></circle>
								<path d="m20 20-3.5-3.5"></path>
							</svg>

							<input
								bind:value={query}
								placeholder="Rechercher une app, un slug, une catégorie..."
								class="h-12 w-full rounded-[18px] border border-black/8 bg-black/[0.03] pl-11 pr-4 text-sm text-zinc-900 placeholder:text-zinc-500 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.6)] transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-black/25 dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-black/35"
							/>
						</div>

						<div class="flex flex-wrap gap-2">
							<button
								type="button"
								onclick={() => (sortBy = 'catalog')}
								class={`rounded-[14px] px-3.5 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] transition-all duration-150 ${
									sortBy === 'catalog'
										? 'border border-black/10 bg-black/[0.08] text-zinc-950 dark:border-white/15 dark:bg-white/[0.09] dark:text-white'
										: 'border border-black/5 bg-black/[0.03] text-zinc-500 hover:text-zinc-900 dark:border-white/8 dark:bg-white/[0.03] dark:text-zinc-500 dark:hover:text-white'
								}`}
							>
								Catalogue
							</button>

							<button
								type="button"
								onclick={() => (sortBy = 'az')}
								class={`rounded-[14px] px-3.5 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] transition-all duration-150 ${
									sortBy === 'az'
										? 'border border-black/10 bg-black/[0.08] text-zinc-950 dark:border-white/15 dark:bg-white/[0.09] dark:text-white'
										: 'border border-black/5 bg-black/[0.03] text-zinc-500 hover:text-zinc-900 dark:border-white/8 dark:bg-white/[0.03] dark:text-zinc-500 dark:hover:text-white'
								}`}
							>
								A → Z
							</button>
						</div>
					</div>
				</div>
			</div>
		</header>

		<section class="mb-5">
			<div class="no-scrollbar -mx-4 overflow-x-auto px-4">
				<div class="flex min-w-max gap-2.5">
					{#each categories as category}
						<button
							type="button"
							onclick={() => (activeCategory = category)}
							class={`rounded-full px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] whitespace-nowrap transition-all duration-150 ${
								activeCategory === category
									? 'border border-black/10 bg-black/[0.08] text-zinc-950 dark:border-white/15 dark:bg-white/[0.1] dark:text-white'
									: 'border border-black/5 bg-black/[0.03] text-zinc-500 hover:bg-black/[0.05] hover:text-zinc-900 dark:border-white/8 dark:bg-white/[0.03] dark:text-zinc-500 dark:hover:bg-white/[0.05] dark:hover:text-white'
							}`}
						>
							{category}
						</button>
					{/each}
				</div>
			</div>
		</section>

		<section class="mb-4 flex items-center justify-between gap-4">
			<div>
				<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">Résultats</h2>
				<p class="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-zinc-500">
					{filteredApps.length} résultats • {activeCategory}
				</p>
			</div>
		</section>

		<section>
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
				{#each filteredApps as app}
					<AppCard {app} compact installEnabled={isAuthenticated} />
				{/each}
			</div>
		</section>

		{#if filteredApps.length === 0}
			<div class="mt-6 rounded-[24px] border border-black/5 bg-white/60 p-6 text-sm text-zinc-600 shadow-[0_10px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-[0_10px_30px_rgba(0,0,0,0.2)]">
				Aucune application ne correspond à ta recherche.
			</div>
		{/if}
	</div>
</div>