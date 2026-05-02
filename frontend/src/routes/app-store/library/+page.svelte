<script lang="ts">
	import AppTableRow from '$lib/components/store/AppTableRow.svelte';
	import AppMobileRow from '$lib/components/store/AppMobileRow.svelte';
	import { page } from '$app/state';

	let { data } = $props();

	let query = $state('');
	let sortBy = $state<'catalog' | 'az'>('catalog');
	let activeCategory = $state(page.url.searchParams.get('category') ?? 'Tous');

	type AppItem = {
		name: string;
		slug: string;
		description: string;
		tagline: string;
		category: string;
		status: string;
		order: number;
		docs_url?: string | null;
		docs_status?: string | null;
		aliases?: string[];
	};

	const isAuthenticated = $derived(Boolean(data.user));

	const apps = $derived(
		(data.apps ?? []).map((app: any, index: number) => ({
			...app,
			name: app.name ?? app.title ?? 'Application',
			slug: app.slug ?? '',
			description: app.description ?? '',
			tagline: app.tagline ?? app.description ?? '',
			category: app.category ?? 'Autre',
			status: app.status ?? 'Disponible',
			order: index
		})) satisfies AppItem[]
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

	const categoryCounts = $derived.by(() => {
		const counts = new Map<string, number>();
		counts.set('Tous', apps.length);

		for (const app of apps) {
			const category = app.category || 'Autre';
			counts.set(category, (counts.get(category) ?? 0) + 1);
		}

		return counts;
	});

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
				app.category.toLowerCase().includes(q) ||
				(app.aliases ?? []).some((alias) => alias.toLowerCase().includes(q));

			return matchesCategory && matchesQuery;
		});

		if (sortBy === 'az') {
			list = [...list].sort((a, b) => a.name.localeCompare(b.name, 'fr'));
		} else {
			list = [...list].sort((a, b) => a.order - b.order);
		}

		return list;
	});

	const categoryNavClass = (category: string, active: boolean) => {
		if (category === 'Tous') {
			return active
				? 'border border-black/8 bg-[linear-gradient(90deg,rgba(34,211,238,0.12),rgba(59,130,246,0.08),rgba(168,85,247,0.10))] text-zinc-950 shadow-[0_10px_24px_rgba(34,211,238,0.08)] dark:border-white/10 dark:bg-[linear-gradient(90deg,rgba(34,211,238,0.14),rgba(59,130,246,0.08),rgba(168,85,247,0.10))] dark:text-white'
				: 'text-zinc-600 hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-400 dark:hover:bg-white/[0.05] dark:hover:text-white';
		}

		if (category === 'media') {
			return active
				? 'border border-cyan-200/80 bg-cyan-50 text-cyan-800 shadow-[0_10px_24px_rgba(34,211,238,0.10)] dark:border-cyan-400/20 dark:bg-cyan-400/12 dark:text-cyan-200'
				: 'text-cyan-700 hover:bg-cyan-50 hover:text-cyan-900 dark:text-cyan-300 dark:hover:bg-cyan-400/10 dark:hover:text-cyan-200';
		}

		if (category === 'telechargement') {
			return active
				? 'border border-violet-200/80 bg-violet-50 text-violet-800 shadow-[0_10px_24px_rgba(139,92,246,0.10)] dark:border-violet-400/20 dark:bg-violet-400/12 dark:text-violet-200'
				: 'text-violet-700 hover:bg-violet-50 hover:text-violet-900 dark:text-violet-300 dark:hover:bg-violet-400/10 dark:hover:text-violet-200';
		}

		if (category === 'securite') {
			return active
				? 'border border-amber-200/80 bg-amber-50 text-amber-800 shadow-[0_10px_24px_rgba(245,158,11,0.10)] dark:border-amber-400/20 dark:bg-amber-400/12 dark:text-amber-200'
				: 'text-amber-700 hover:bg-amber-50 hover:text-amber-900 dark:text-amber-300 dark:hover:bg-amber-400/10 dark:hover:text-amber-200';
		}

		if (category === 'monitoring') {
			return active
				? 'border border-emerald-200/80 bg-emerald-50 text-emerald-800 shadow-[0_10px_24px_rgba(16,185,129,0.10)] dark:border-emerald-400/20 dark:bg-emerald-400/12 dark:text-emerald-200'
				: 'text-emerald-700 hover:bg-emerald-50 hover:text-emerald-900 dark:text-emerald-300 dark:hover:bg-emerald-400/10 dark:hover:text-emerald-200';
		}

		return active
			? 'border border-blue-200/80 bg-blue-50 text-blue-800 shadow-[0_10px_24px_rgba(59,130,246,0.10)] dark:border-blue-400/20 dark:bg-blue-400/12 dark:text-blue-200'
			: 'text-blue-700 hover:bg-blue-50 hover:text-blue-900 dark:text-blue-300 dark:hover:bg-blue-400/10 dark:hover:text-blue-200';
	};
</script>

<svelte:head>
	<title>Bibliothèque d’applications</title>
</svelte:head>

<div class="min-h-screen bg-[#f8fafc] text-zinc-900 dark:bg-[#06070b] dark:text-zinc-100">
	<div class="pointer-events-none fixed inset-0">
		<div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(15,23,42,0.03),transparent_35%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.03),transparent_35%)]"></div>
		<div class="absolute left-[10%] top-0 h-[380px] w-[380px] rounded-full bg-cyan-500/10 blur-3xl dark:bg-cyan-500/[0.05]"></div>
		<div class="absolute right-[10%] top-0 h-[380px] w-[380px] rounded-full bg-violet-500/10 blur-3xl dark:bg-violet-500/[0.05]"></div>
	</div>

	<!-- MOBILE -->
	<div class="relative md:hidden">
		<header class="border-y border-black/5 bg-white/70 dark:border-white/10 dark:bg-white/[0.035] backdrop-blur-xl">
			<div class="px-3 py-5">
				<div class="mb-4">
					<a
						href="/"
						class="inline-flex items-center text-sm text-zinc-500 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white"
					>
						← Retour à l’accueil
					</a>
				</div>

				<div class="inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-200">
					<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
					Library
				</div>

				<h1 class="mt-3 text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
					<span class="block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_22%,#2563eb_58%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#67e8f9_28%,#93c5fd_64%,#c4b5fd_100%)]">
						Bibliothèque complète
					</span>
				</h1>

				<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
					Accède à tout le catalogue avec recherche, tri et filtres.
				</p>

				{#if !isAuthenticated}
					<div class="mt-4 inline-flex rounded-full border border-amber-300/40 bg-amber-100/70 px-4 py-2 text-xs font-semibold text-amber-800 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-200">
						Mode visiteur · installation désactivée
					</div>
				{/if}

				<div class="mt-5 space-y-3">
					<div class="relative min-w-0">
						<svg
							viewBox="0 0 24 24"
							class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500 dark:text-zinc-500"
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
							class="h-12 w-full rounded-[18px] border border-black/8 bg-black/[0.03] pl-11 pr-4 text-sm text-zinc-900 placeholder:text-zinc-500 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:placeholder:text-zinc-500 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
						/>
					</div>

					<div class="grid grid-cols-2 gap-3">
						<select
							bind:value={activeCategory}
							class="h-12 rounded-[18px] border border-black/8 bg-black/[0.03] px-4 text-sm text-zinc-900 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
						>
							{#each categories as category}
								<option value={category}>
									{category} ({categoryCounts.get(category) ?? 0})
								</option>
							{/each}
						</select>

						<select
							bind:value={sortBy}
							class="h-12 rounded-[18px] border border-black/8 bg-black/[0.03] px-4 text-sm text-zinc-900 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
						>
							<option value="catalog">Catalogue</option>
							<option value="az">A → Z</option>
						</select>
					</div>
				</div>
			</div>
		</header>

		<section class="px-3 py-6">
			<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">Résultats</h2>
			<p class="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-zinc-500">
				{filteredApps.length} résultats
				{#if activeCategory !== 'Tous'} • {activeCategory}{/if}
			</p>
		</section>

		{#if filteredApps.length > 0}
			<section class="border-y border-black/5 bg-white/70 dark:border-white/10 dark:bg-white/[0.03] backdrop-blur-sm">
				{#each filteredApps as app, index (app.slug)}
					<AppMobileRow
						{app}
						installEnabled={isAuthenticated}
						isLast={index === filteredApps.length - 1}
					/>
				{/each}
			</section>
		{:else}
			<div class="border-y border-black/5 bg-white/60 py-6 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400">
				<div class="px-3">Aucune application ne correspond à ta recherche.</div>
			</div>
		{/if}
	</div>

	<!-- DESKTOP -->
	<div class="relative hidden md:block sm:mx-auto sm:max-w-7xl sm:px-6 sm:py-8 lg:px-8">
		<div class="lg:grid lg:grid-cols-[260px_minmax(0,1fr)] lg:gap-6">
			<aside class="hidden lg:block">
				<div class="sticky top-6 rounded-[26px] border border-black/5 bg-white/60 p-3 shadow-[0_18px_50px_rgba(15,23,42,0.08)] backdrop-blur-xl dark:border-white/10 dark:bg-[#0b0f19]/90 dark:shadow-[0_18px_50px_rgba(0,0,0,0.30)]">
					<div class="mb-2 px-3 pt-2">
						<a
							href="/"
							class="inline-flex items-center text-sm text-zinc-500 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white"
						>
							← Retour à l’accueil
						</a>
					</div>

					<div class="px-3 pb-2 pt-4 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-500">
						Catégories
					</div>

					<div class="space-y-1">
						{#each categories as category}
							<button
								type="button"
								onclick={() => (activeCategory = category)}
								class={`flex w-full items-center justify-between rounded-[16px] px-3 py-2.5 text-left text-sm transition ${categoryNavClass(category, activeCategory === category)}`}
							>
								<span class="font-medium">{category}</span>
								<span class="text-xs text-zinc-500 dark:text-zinc-500">
									{categoryCounts.get(category) ?? 0}
								</span>
							</button>
						{/each}
					</div>
				</div>
			</aside>

			<div class="min-w-0">
				<header class="mb-5">
					<div
						class="relative overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur-xl dark:border-white/10 dark:bg-[#0b0f19]/90 dark:shadow-[0_24px_80px_rgba(0,0,0,0.34)]"
					>
						<div class="pointer-events-none absolute inset-0">
							<div class="absolute -left-16 top-0 h-56 w-56 rounded-full bg-cyan-500/8 blur-3xl dark:bg-cyan-500/10"></div>
							<div class="absolute right-0 top-0 h-56 w-56 rounded-full bg-violet-500/8 blur-3xl dark:bg-violet-500/10"></div>
						</div>

						<div class="relative p-6">
							<div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
								<div>
									<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-200">
										<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
										Library
									</div>

									<h1 class="max-w-2xl text-xl font-semibold tracking-[-0.04em] text-zinc-950 xl:text-2xl xl:leading-[1.1] dark:text-white">
										<span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_22%,#2563eb_58%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#67e8f9_28%,#93c5fd_64%,#c4b5fd_100%)]">
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

							<div class="mt-5 grid gap-3 md:grid-cols-[minmax(0,1fr)_220px_160px]">
								<div class="relative min-w-0">
									<svg
										viewBox="0 0 24 24"
										class="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500 dark:text-zinc-500"
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
										class="h-12 w-full rounded-[18px] border border-black/8 bg-black/[0.03] pl-11 pr-4 text-sm text-zinc-900 placeholder:text-zinc-500 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:placeholder:text-zinc-500 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
									/>
								</div>

								<select
									bind:value={activeCategory}
									class="h-12 rounded-[18px] border border-black/8 bg-black/[0.03] px-4 text-sm text-zinc-900 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
								>
									{#each categories as category}
										<option value={category}>
											{category} ({categoryCounts.get(category) ?? 0})
										</option>
									{/each}
								</select>

								<select
									bind:value={sortBy}
									class="h-12 rounded-[18px] border border-black/8 bg-black/[0.03] px-4 text-sm text-zinc-900 outline-none shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] transition focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[#06090f] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] dark:focus:border-cyan-400/30 dark:focus:bg-[#080c14]"
								>
									<option value="catalog">Catalogue</option>
									<option value="az">A → Z</option>
								</select>
							</div>
						</div>
					</div>
				</header>

				<section class="pb-6">
					<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">Résultats</h2>
					<p class="mt-1 text-xs font-medium uppercase tracking-[0.12em] text-zinc-500">
						{filteredApps.length} résultats
						{#if activeCategory !== 'Tous'} • {activeCategory}{/if}
					</p>
				</section>

				{#if filteredApps.length > 0}
					<section>
						<div
							class="overflow-hidden rounded-[24px] border border-black/5 bg-white/70 shadow-[0_14px_50px_rgba(15,23,42,0.06)] backdrop-blur-xl dark:border-white/10 dark:bg-[#0b0f19]/92 dark:shadow-[0_18px_50px_rgba(0,0,0,0.32)]"
						>
							<div class="grid grid-cols-[minmax(0,1.1fr)_minmax(0,1.6fr)_170px_150px_220px] gap-4 border-b border-black/5 px-5 py-3 text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-500 dark:border-white/10 dark:text-zinc-500">
								<div>Application</div>
								<div>Description</div>
								<div>Catégorie</div>
								<div>Documentation</div>
								<div class="text-right">Actions</div>
							</div>

							{#each filteredApps as app, index (app.slug)}
								<AppTableRow
									{app}
									installEnabled={isAuthenticated}
									isLast={index === filteredApps.length - 1}
								/>
							{/each}
						</div>
					</section>
				{:else}
					<div class="rounded-[24px] border border-black/5 bg-white/60 p-6 text-sm text-zinc-600 shadow-[0_10px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-[0_10px_30px_rgba(0,0,0,0.22)]">
						Aucune application ne correspond à ta recherche.
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>