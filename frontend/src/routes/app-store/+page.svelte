<script lang="ts">
	import AppCard from '$lib/components/store/AppCard.svelte';

	let { data } = $props();

	let activeCategory = $state('Tous');

	const SUGGESTED_SLUGS = ['radarr', 'sonarr', 'overseerr', 'plex', 'prowlarr', 'nextcloud'];

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

	const suggestedApps = $derived(
		apps.filter((app) => SUGGESTED_SLUGS.includes(app.slug.toLowerCase()))
	);

	const libraryHref = $derived(
		activeCategory !== 'Tous'
			? `/app-store/library?category=${encodeURIComponent(activeCategory)}`
			: '/app-store/library'
	);
</script>

<svelte:head>
	<title>App Store</title>
</svelte:head>

<div class="min-h-screen bg-[#f8fafc] text-zinc-900 dark:bg-[#06070b] dark:text-zinc-100">
	<div class="pointer-events-none fixed inset-0">
		<div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(15,23,42,0.04),transparent_35%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.035),transparent_35%)]"></div>
		<div class="absolute left-0 top-0 h-[420px] w-[420px] rounded-full bg-cyan-500/10 blur-3xl dark:bg-cyan-500/[0.06]"></div>
		<div class="absolute right-0 top-0 h-[420px] w-[420px] rounded-full bg-violet-500/10 blur-3xl dark:bg-violet-500/[0.05]"></div>
	</div>

	<div class="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<header class="mb-8 overflow-hidden rounded-[32px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.35)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.75),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.04),rgba(255,255,255,0.01))]"></div>

				<div class="relative p-6 sm:p-8 lg:p-10">
					<div class="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
						<div class="max-w-3xl">
							<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
								<span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
								App Store
							</div>

                                                        <h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
	                                                        <span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
		                                                Explore le Catalogue
	                                                        </span>
                                                        </h1>

							<p class="mt-4 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								Une sélection soignée pour démarrer vite, puis une bibliothèque complète pour
								accéder à l’ensemble des applications.
							</p>
						</div>

						<div class="flex flex-wrap gap-3">
							<a
								href={libraryHref}
								class="inline-flex items-center rounded-[18px] border border-black/8 bg-black/[0.05] px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.55)] transition-all duration-200 hover:border-black/12 hover:bg-black/[0.08] dark:border-white/10 dark:bg-white/[0.06] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] dark:hover:border-white/20 dark:hover:bg-white/[0.1]"
							>
								Voir toute la bibliothèque
							</a>
						</div>
					</div>

					<div class="mt-8 grid gap-3 sm:grid-cols-3">
						<div class="rounded-[22px] border border-black/5 bg-white/70 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
							<div class="text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-500">Catalogue</div>
							<div class="mt-2 text-2xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">{apps.length}</div>
						</div>

						<div class="rounded-[22px] border border-black/5 bg-white/70 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
							<div class="text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-500">Expérience</div>
							<div class="mt-2 text-sm font-medium text-zinc-800 dark:text-zinc-200">Store + Library</div>
						</div>

						<div class="rounded-[22px] border border-black/5 bg-white/70 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
							<div class="text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-500">Accès</div>
							<div class="mt-2 text-sm font-medium text-zinc-800 dark:text-zinc-200">Par catégories ou vue complète</div>
						</div>
					</div>
				</div>
			</div>
		</header>

		<section class="mb-8">
			<div class="no-scrollbar -mx-4 overflow-x-auto px-4">
				<div class="flex min-w-max gap-2.5">
					{#each categories as category}
						<button
							type="button"
							onclick={() => (activeCategory = category)}
							class={`rounded-full px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] whitespace-nowrap transition-all duration-150 ${
								activeCategory === category
									? 'border border-black/10 bg-black/[0.08] text-zinc-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.5)] dark:border-white/15 dark:bg-white/[0.1] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]'
									: 'border border-black/5 bg-black/[0.03] text-zinc-500 hover:border-black/10 hover:bg-black/[0.05] hover:text-zinc-900 dark:border-white/8 dark:bg-white/[0.03] dark:text-zinc-500 dark:hover:border-white/12 dark:hover:bg-white/[0.05] dark:hover:text-white'
							}`}
						>
							{category}
						</button>
					{/each}
				</div>
			</div>
		</section>

		<section class="rounded-[30px] border border-black/5 bg-white/60 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.025] dark:shadow-[0_12px_40px_rgba(0,0,0,0.24)] sm:p-6">
			<div class="mb-5 flex items-center justify-between">
				<div>
					<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">Suggestions</h2>
					<p class="mt-1 text-sm text-zinc-500">Les applications les plus utilisées.</p>
				</div>

				<a href={libraryHref} class="text-sm font-medium text-zinc-500 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white">
					Tout voir
				</a>
			</div>

			<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
				{#each suggestedApps as app}
					<AppCard {app} />
				{/each}
			</div>
		</section>
	</div>
</div>