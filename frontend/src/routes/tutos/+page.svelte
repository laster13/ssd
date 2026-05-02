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
</script>

<svelte:head>
	<title>Documentation | SSD</title>
	<meta name="description" content="Documentation et tutoriels SSD." />
</svelte:head>

<section class="mx-auto max-w-7xl px-3 py-6 sm:px-6 sm:py-10 lg:px-8">
	<div class="grid gap-6 lg:grid-cols-[280px_1fr] lg:gap-8">
		<div class="space-y-4 sm:space-y-6">
			<a
				href="/"
				class="flex w-full items-center rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm font-medium text-zinc-600 shadow-sm transition hover:border-zinc-300 hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:border-zinc-700 dark:hover:bg-zinc-950 dark:hover:text-zinc-100"
			>
				← Retour à l’accueil
			</a>

			<div class="rounded-3xl border border-zinc-200 bg-white p-2 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
				<DocsSearch tutorials={data.tutorials} />
			</div>

			<div class="rounded-3xl border border-zinc-200 bg-white p-2 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
				<DocsSidebar groups={data.docsNavGroups} />
			</div>
		</div>

		<div class="rounded-[1.75rem] border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:rounded-[2rem] sm:p-8">
			<div class="max-w-4xl">
				<div class="flex flex-wrap items-center gap-3">
					<div
						class="inline-flex items-center gap-2 rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300"
					>
						<span class="h-2 w-2 rounded-full bg-sky-500"></span>
						Documentation SSD
					</div>

					<div
						class="inline-flex items-center rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300"
					>
						{data.tutorials.length} tutoriels
					</div>
				</div>

				<p class="mt-5 text-xs font-medium uppercase tracking-[0.18em] text-zinc-500 sm:text-sm">
					Guides & tutoriels
				</p>

				<h1 class="mt-3 text-3xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-4xl">
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

			<div class="mt-8 grid gap-3 sm:grid-cols-3">
				<div class="rounded-2xl border border-sky-200 bg-sky-50 px-4 py-4 dark:border-sky-500/20 dark:bg-sky-500/10">
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:text-sky-300">
						Recherche
					</p>
					<p class="mt-2 text-sm text-zinc-700 dark:text-zinc-200">Trouve vite le bon tuto.</p>
				</div>

				<div
					class="rounded-2xl border border-violet-200 bg-violet-50 px-4 py-4 dark:border-violet-500/20 dark:bg-violet-500/10"
				>
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 dark:text-violet-300">
						Navigation
					</p>
					<p class="mt-2 text-sm text-zinc-700 dark:text-zinc-200">Parcours par groupes et catégories.</p>
				</div>

				<div
					class="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-4 dark:border-emerald-500/20 dark:bg-emerald-500/10"
				>
					<p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-emerald-700 dark:text-emerald-300">
						Progression
					</p>
					<p class="mt-2 text-sm text-zinc-700 dark:text-zinc-200">Choisis selon ton niveau et ton temps.</p>
				</div>
			</div>

			<div class="mt-10 space-y-10 sm:mt-12">
				{#each data.docsNavGroups as group}
					<section>
						<h2 class="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-3xl">
							<span class="bg-gradient-to-r from-zinc-900 via-blue-700 to-violet-700 bg-clip-text text-transparent dark:from-white dark:via-sky-300 dark:to-violet-300">
								{group.name}
							</span>
						</h2>

						<div class="mt-5 space-y-8">
							{#each group.categories as category}
								<div>
									<div class="flex items-center gap-3">
										<div class="h-2.5 w-2.5 rounded-full bg-gradient-to-br from-sky-500 to-violet-500"></div>
										<h3 class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 sm:text-sm">
											{category.name}
										</h3>
									</div>

									<div class="mt-4 grid gap-3 sm:gap-4 md:grid-cols-2 xl:grid-cols-3">
										{#each category.items as item}
											{@const tutorial = data.tutorials.find((t) => t.slug === item.slug)}
											{#if tutorial}
												<a
													href={`/tutos/${tutorial.slug}`}
													class="group rounded-3xl border border-zinc-200 bg-zinc-50 p-4 transition hover:-translate-y-0.5 hover:border-sky-200 hover:bg-white hover:shadow-md dark:border-zinc-800 dark:bg-zinc-950/50 dark:hover:border-sky-500/20 dark:hover:bg-zinc-900 sm:p-5"
												>
													<div class="flex flex-wrap items-center gap-2">
														<TutorialBadge text={tutorial.level} variant="level" />
														<TutorialBadge text={tutorial.category} variant="category" />
													</div>

													<h4 class="mt-4 text-lg font-semibold tracking-tight text-zinc-900 transition-colors group-hover:text-sky-700 dark:text-zinc-100 dark:group-hover:text-sky-300 sm:text-xl">
														{tutorial.title}
													</h4>

													<p class="mt-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
														{tutorial.description}
													</p>

													<div class="mt-5 flex items-center justify-between gap-3 text-xs text-zinc-500 dark:text-zinc-400">
														<span>{tutorial.duration}</span>
														<span class="inline-flex items-center gap-2">
															<span>{tutorial.steps.length} étapes</span>
															<span
																class="transition-transform duration-200 group-hover:translate-x-0.5"
															>
																→
															</span>
														</span>
													</div>
												</a>
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