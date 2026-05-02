<script lang="ts">
	import DocsSearch from '$lib/components/tutorials/DocsSearch.svelte';
	import DocsSidebar from '$lib/components/tutorials/DocsSidebar.svelte';
	import TutorialBadge from '$lib/components/tutorials/TutorialBadge.svelte';
	import type { DocsNavGroup, Tutorial } from '$lib/data/tutorials';

	let {
		data
	}: {
		data: {
			tutorials: Tutorial[];
			docsNavGroups: DocsNavGroup[];
		};
	} = $props();

	let isMobileNavOpen = $state(false);
</script>

<svelte:head>
	<title>Documentation | SSD</title>
	<meta name="description" content="Documentation et tutoriels SSD." />
</svelte:head>

<section class="mx-auto max-w-7xl overflow-x-hidden py-6 pb-28 sm:px-6 sm:py-10 sm:pb-10 lg:px-8">
	<div class="grid gap-6 lg:grid-cols-[280px_minmax(0,1fr)] lg:gap-8">
		<div class="min-w-0 space-y-4 px-3 sm:space-y-6 sm:px-0">
			<a
				href="/"
				class="flex w-full min-w-0 items-center rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm font-medium text-zinc-600 shadow-sm transition hover:border-zinc-300 hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:border-zinc-700 dark:hover:bg-zinc-950 dark:hover:text-zinc-100"
			>
				← Retour à l’accueil
			</a>

			<div class="min-w-0 rounded-3xl border border-zinc-200 bg-white p-2 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
				<DocsSearch tutorials={data.tutorials} />
			</div>

			<div class="hidden lg:block">
				<div class="min-w-0 rounded-3xl border border-zinc-200 bg-white p-2 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
					<DocsSidebar groups={data.docsNavGroups} />
				</div>
			</div>
		</div>

		<div class="min-w-0">
			<div class="px-3 sm:px-0">
				<div class="max-w-4xl min-w-0">
					<div class="flex min-w-0 flex-wrap items-center gap-3">
						<div
							class="inline-flex max-w-full min-w-0 items-center gap-2 rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300"
						>
							<span class="h-2 w-2 shrink-0 rounded-full bg-sky-500"></span>
							<span class="min-w-0 truncate">Documentation SSD</span>
						</div>

						<div
							class="inline-flex max-w-full min-w-0 items-center rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300"
						>
							<span class="min-w-0 truncate">{data.tutorials.length} tutoriels</span>
						</div>
					</div>

					<p class="mt-5 text-xs font-medium uppercase tracking-[0.18em] text-zinc-500 sm:text-sm">
						Guides & tutoriels
					</p>

					<h1 class="mt-3 break-words text-3xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-4xl">
						Des guides
						<span class="bg-gradient-to-r from-sky-500 via-blue-600 to-violet-600 bg-clip-text text-transparent">
							plus clairs
						</span>
						pour aller plus vite
					</h1>

					<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-300 sm:text-base">
						Retrouve tous les tutoriels SSD dans un espace plus lisible, avec recherche rapide,
						navigation par thèmes et accès direct aux guides les plus utiles.
					</p>
				</div>
			</div>

			<div class="mt-8 grid gap-3 px-3 sm:grid-cols-3 sm:px-0">
				<div class="min-w-0 rounded-2xl border border-sky-200 bg-sky-50 px-4 py-4 dark:border-sky-500/20 dark:bg-sky-500/10">
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:text-sky-300">
						Recherche
					</p>
					<p class="mt-2 break-words text-sm text-zinc-700 dark:text-zinc-200">Trouve vite le bon tuto.</p>
				</div>

				<div
					class="min-w-0 rounded-2xl border border-violet-200 bg-violet-50 px-4 py-4 dark:border-violet-500/20 dark:bg-violet-500/10"
				>
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 dark:text-violet-300">
						Navigation
					</p>
					<p class="mt-2 break-words text-sm text-zinc-700 dark:text-zinc-200">Parcours par groupes et catégories.</p>
				</div>

				<div
					class="min-w-0 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-4 dark:border-emerald-500/20 dark:bg-emerald-500/10"
				>
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-emerald-700 dark:text-emerald-300">
						Progression
					</p>
					<p class="mt-2 break-words text-sm text-zinc-700 dark:text-zinc-200">Choisis selon ton niveau et ton temps.</p>
				</div>
			</div>

			<div class="mt-10 space-y-10 sm:mt-12">
				{#each data.docsNavGroups as group}
					<section class="min-w-0">
						<div class="px-3 sm:px-0">
							<h2 class="break-words text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-3xl">
								<span class="bg-gradient-to-r from-zinc-900 via-blue-700 to-violet-700 bg-clip-text text-transparent dark:from-white dark:via-sky-300 dark:to-violet-300">
									{group.name}
								</span>
							</h2>
						</div>

						<div class="mt-5 space-y-8">
							{#each group.categories as category}
								<div class="min-w-0">
									<div class="px-3 sm:px-0">
										<div class="flex min-w-0 items-center gap-3">
											<div class="h-2.5 w-2.5 shrink-0 rounded-full bg-gradient-to-br from-sky-500 to-violet-500"></div>
											<h3 class="min-w-0 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 sm:text-sm">
												<span class="block break-words">{category.name}</span>
											</h3>
										</div>
									</div>

                                                                        <div class="mt-4 overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
                                                                        	{#each category.items as item, index}
                                                                        		{@const tutorial = data.tutorials.find((t) => t.slug === item.slug)}
                                                                        		{#if tutorial}
                                                                        			<a
                                                                        				href={`/tutos/${tutorial.slug}`}
                                                                        				class="group block min-w-0 px-4 py-4 transition hover:bg-zinc-50 dark:hover:bg-zinc-800/50 sm:px-5"
                                                                        			>
                                                                        				<div class="flex min-w-0 flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
                                                                        					<div class="min-w-0 flex-1">
                                                                        						<div class="flex min-w-0 flex-wrap items-center gap-2">
                                                                        							<TutorialBadge text={tutorial.level} variant="level" />
                                                                        							<TutorialBadge text={tutorial.category} variant="category" />
                                                                        						</div>

                                                                        						<div class="mt-3 flex min-w-0 items-start gap-3">
                                                                        							<div class="mt-1 hidden h-2.5 w-2.5 shrink-0 rounded-full bg-gradient-to-br from-sky-500 to-violet-500 sm:block"></div>

                                                                        							<div class="min-w-0">
                                                                        								<h4 class="break-words text-base font-semibold tracking-tight text-zinc-900 transition-colors group-hover:text-sky-700 dark:text-zinc-100 dark:group-hover:text-sky-300 sm:text-lg">
                                                                        									{tutorial.title}
                                                                        								</h4>

                                                                        								<p class="mt-1 line-clamp-2 break-words text-sm leading-6 text-zinc-600 dark:text-zinc-300">
                                                                        									{tutorial.description}
                                                                        								</p>
                                                                        							</div>
                                                                        						</div>
                                                                        					</div>

                                                                        					<div class="flex min-w-0 flex-wrap items-center gap-3 text-xs text-zinc-500 dark:text-zinc-400 xl:ml-6 xl:shrink-0 xl:justify-end">
                                                                        						<span class="inline-flex items-center rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
                                                                        							{tutorial.duration}
                                                                        						</span>

                                                                        						<span class="inline-flex items-center rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
                                                                        							{tutorial.steps.length} étapes
                                                                        						</span>

                                                                        						<span
                                                                        							class="inline-flex items-center gap-2 font-medium text-sky-700 transition-transform duration-200 group-hover:translate-x-0.5 dark:text-sky-300"
                                                                        						>
                                                                        							Ouvrir
                                                                        							<span aria-hidden="true">→</span>
                                                                        						</span>
                                                                        					</div>
                                                                        				</div>
                                                                        			</a>

                                                                        			{#if index < category.items.length - 1}
                                                                        				<div class="mx-4 border-t border-zinc-200 dark:border-zinc-800 sm:mx-5"></div>
                                                                        			{/if}
                                                                        		{/if}
                                                                        	{/each}
                                                                        </div>
								</div>
							{/each}
						</div>
					</section>
				{/each}
			</div>
		</div>
	</div>
</section>

{#if isMobileNavOpen}
	<button
		type="button"
		class="fixed inset-0 z-40 bg-zinc-950/30 backdrop-blur-[3px] lg:hidden"
		aria-label="Fermer le menu"
		onclick={() => (isMobileNavOpen = false)}
	></button>

	<div
		class="fixed inset-x-0 bottom-0 z-50 max-h-[76vh] overflow-hidden rounded-t-[1.75rem] border-t border-zinc-200/80 bg-white/96 shadow-[0_-12px_40px_rgba(0,0,0,0.12)] backdrop-blur-xl dark:border-zinc-800/80 dark:bg-zinc-900/96 lg:hidden"
	>
		<div class="flex justify-center px-4 pb-2 pt-3">
			<div class="h-1 w-10 rounded-full bg-zinc-300 dark:bg-zinc-700"></div>
		</div>

		<div class="flex items-center justify-between px-4 pb-3">
			<div>
				<p class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Navigation</p>
				<p class="text-[11px] text-zinc-500 dark:text-zinc-400">Accès rapide aux catégories</p>
			</div>

			<button
				type="button"
				class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-zinc-100 text-zinc-500 transition hover:bg-zinc-200 hover:text-zinc-900 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700 dark:hover:text-zinc-100"
				aria-label="Fermer le menu"
				onclick={() => (isMobileNavOpen = false)}
			>
				✕
			</button>
		</div>

		<div class="overflow-y-auto px-3 pb-4">
			<div class="rounded-[1.4rem] border border-zinc-200/80 bg-white/90 p-2 dark:border-zinc-800/80 dark:bg-zinc-900/90">
				<DocsSidebar groups={data.docsNavGroups} />
			</div>
		</div>
	</div>
{/if}

<div class="fixed inset-x-0 bottom-0 z-30 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden">
	<div class="mx-auto max-w-sm rounded-[1.5rem] border border-zinc-200/70 bg-white/80 p-1.5 shadow-[0_10px_30px_rgba(0,0,0,0.10)] backdrop-blur-xl dark:border-zinc-800/70 dark:bg-zinc-900/80">
		<div class="grid grid-cols-2 gap-1.5">
			<a
				href="/"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100/80 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800/80 dark:hover:text-zinc-100"
			>
				<span class="text-base leading-none">⌂</span>
				<span>Accueil</span>
			</a>

			<button
				type="button"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] bg-gradient-to-r from-sky-500 to-violet-500 px-3 py-2.5 text-sm font-semibold text-white shadow-sm transition active:scale-[0.98]"
				onclick={() => (isMobileNavOpen = true)}
			>
				<span class="text-base leading-none">☰</span>
				<span>Menu</span>
			</button>
		</div>
	</div>
</div>