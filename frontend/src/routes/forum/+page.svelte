<script lang="ts">
	import { onMount } from 'svelte';

	let { data } = $props();
	const {
		topics,
		categories,
		tutorialSlug,
		categorySlug,
		onlyUnsolved,
		q,
		sort,
		page,
		hasNextPage,
		user
	} = data;

	let unreadTopicLinks = $state<Set<string>>(new Set());

	onMount(async () => {
		if (!user) return;

		try {
			const response = await fetch('/api/notifications/unread-topic-links');
			const payload = await response.json();

			if (response.ok && Array.isArray(payload?.links)) {
				unreadTopicLinks = new Set(payload.links);
			}
		} catch {
			// noop
		}
	});

	function formatDate(value: string) {
		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(value));
	}

	function buildPageHref(nextPage: number) {
		const params = new URLSearchParams();
		if (tutorialSlug) params.set('tutorial', tutorialSlug);
		if (categorySlug) params.set('category', categorySlug);
		if (onlyUnsolved) params.set('unsolved', '1');
		if (q) params.set('q', q);
		if (sort) params.set('sort', sort);
		params.set('page', String(nextPage));
		return `/forum?${params.toString()}`;
	}

	function topicLink(slug: string) {
		return `/forum/${slug}`;
	}

	function isUnreadTopic(slug: string) {
		return unreadTopicLinks.has(topicLink(slug));
	}

	const resolvedCount = topics.filter((topic) => !!topic.accepted_post_id).length;
	const openCount = topics.length - resolvedCount;
</script>

<svelte:head>
	<title>Forum SSD</title>
</svelte:head>

<div class="mx-auto w-full max-w-7xl py-6 pb-28 sm:px-6 sm:py-8 sm:pb-8 lg:px-8">
	<div class="px-4 sm:px-0">
		<div class="flex flex-wrap gap-3">
			<a
				href={tutorialSlug ? `/tutos/${tutorialSlug}` : '/tutos'}
				class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				← Retour tuto
			</a>

			<a
				href="/"
				class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				⌂ Accueil
			</a>
		</div>
	</div>

	<section class="mt-6 border-b border-zinc-200 px-4 pb-6 dark:border-zinc-800 sm:rounded-3xl sm:border sm:bg-white sm:p-6 dark:sm:bg-zinc-950/40">
		<div class="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
			<div class="max-w-3xl">
				<p class="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600 dark:text-indigo-300">
					Forum
				</p>

				<h1 class="mt-2 bg-gradient-to-r from-zinc-900 via-indigo-700 to-blue-600 bg-clip-text text-3xl font-semibold tracking-tight text-transparent dark:from-white dark:via-indigo-300 dark:to-blue-300">
					Support et discussions techniques SSD
				</h1>

				<p class="mt-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
					Retrouve les sujets liés aux tutoriels, aux déploiements et aux applications, puis
					ouvre une discussion claire quand tu bloques sur une étape.
				</p>

				<div class="mt-4 flex flex-wrap gap-x-3 gap-y-2 text-sm text-zinc-500 dark:text-zinc-400">
					<span class="rounded-full bg-zinc-100 px-3 py-1 dark:bg-zinc-800/80">
						{topics.length} sujet{topics.length > 1 ? 's' : ''}
					</span>
					<span class="rounded-full bg-zinc-100 px-3 py-1 dark:bg-zinc-800/80">
						{openCount} ouvert{openCount > 1 ? 's' : ''}
					</span>
					<span class="rounded-full bg-zinc-100 px-3 py-1 dark:bg-zinc-800/80">
						{resolvedCount} résolu{resolvedCount > 1 ? 's' : ''}
					</span>
				</div>
			</div>

			<div class="flex flex-wrap gap-3">
				<a
					href="/forum/new"
					class="inline-flex items-center justify-center rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400"
				>
					Créer un sujet
				</a>

				{#if user?.is_admin}
					<a
						href="/admin/forum/reports"
						class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-indigo-900/60 dark:hover:bg-indigo-950/20 dark:hover:text-indigo-300"
					>
						Signalements admin
					</a>
				{/if}

				{#if !user}
					<a
						href="/login?next=/forum/new"
						class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-indigo-900/60 dark:hover:bg-indigo-950/20 dark:hover:text-indigo-300"
					>
						Se connecter
					</a>
				{/if}
			</div>
		</div>
	</section>

	<form method="GET" class="border-b border-zinc-200 px-4 py-5 dark:border-zinc-800 sm:mt-6 sm:rounded-3xl sm:border sm:bg-zinc-50/40 sm:p-5 dark:sm:bg-zinc-950/30">
		<div class="grid gap-4 lg:grid-cols-12">
			<div class="lg:col-span-4">
				<label for="q" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
					Recherche
				</label>
				<input
					id="q"
					name="q"
					type="text"
					value={q}
					placeholder="Ex. nextcloud 502"
					class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 dark:focus:ring-indigo-950/40"
				/>
			</div>

			<div class="lg:col-span-2">
				<label for="tutorial" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
					Tutoriel
				</label>
				<input
					id="tutorial"
					name="tutorial"
					type="text"
					value={tutorialSlug}
					placeholder="Ex. nextcloud"
					class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 dark:focus:ring-indigo-950/40"
				/>
			</div>

			<div class="lg:col-span-2">
				<label for="category" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
					Catégorie
				</label>
				<select
					id="category"
					name="category"
					class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 dark:focus:ring-indigo-950/40"
				>
					<option value="">Toutes</option>
					{#each categories as category}
						<option value={category.slug} selected={categorySlug === category.slug}>
							{category.name}
						</option>
					{/each}
				</select>
			</div>

			<div class="lg:col-span-2">
				<label for="sort" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
					Tri
				</label>
				<select
					id="sort"
					name="sort"
					class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 dark:focus:ring-indigo-950/40"
				>
					<option value="recent" selected={sort === 'recent'}>Plus récents</option>
					<option value="active" selected={sort === 'active'}>Plus actifs</option>
					<option value="views" selected={sort === 'views'}>Plus vus</option>
					<option value="oldest" selected={sort === 'oldest'}>Plus anciens</option>
				</select>
			</div>

			<div class="lg:col-span-2">
				<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
					Statut
				</label>
				<label class="flex h-[50px] items-center gap-2 rounded-2xl border border-zinc-300 bg-white px-4 text-sm text-zinc-700 transition hover:border-indigo-300 hover:bg-indigo-50/60 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:border-indigo-900/60 dark:hover:bg-indigo-950/20">
					<input type="checkbox" name="unsolved" value="1" checked={onlyUnsolved} />
					Non résolus
				</label>
			</div>
		</div>

		<div class="mt-4 flex flex-wrap gap-3">
			<button
				type="submit"
				class="rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400"
			>
				Appliquer
			</button>

			<a
				href="/forum"
				class="rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				Réinitialiser
			</a>
		</div>
	</form>

	<div class="sm:mt-6 sm:overflow-hidden sm:rounded-3xl sm:border sm:border-zinc-200 sm:bg-white dark:sm:border-zinc-800 dark:sm:bg-zinc-950/40">
		{#if topics.length > 0}
			{#each topics as topic}
				<a
					href={`/forum/${topic.slug}`}
					class={`group block border-b border-zinc-200 px-4 py-5 transition last:border-b-0 hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900/50 sm:px-6 ${
						isUnreadTopic(topic.slug) ? 'bg-indigo-50/40 dark:bg-indigo-950/10' : ''
					}`}
				>
					<div class="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-2">
								<span class="rounded-full border border-zinc-200 bg-zinc-50 px-2.5 py-1 text-[11px] font-medium text-zinc-700 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200">
									{topic.category.name}
								</span>

								{#if topic.related_tutorial_slug}
									<span class="rounded-full bg-indigo-50 px-2.5 py-1 text-[11px] font-medium text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-300">
										{topic.related_tutorial_slug}
									</span>
								{/if}

								{#if topic.is_pinned}
									<span class="rounded-full bg-amber-100 px-2.5 py-1 text-[11px] font-medium text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
										Épinglé
									</span>
								{/if}

								{#if topic.accepted_post_id}
									<span class="rounded-full bg-emerald-100 px-2.5 py-1 text-[11px] font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
										Résolu
									</span>
								{/if}

								{#if isUnreadTopic(topic.slug)}
									<span class="rounded-full bg-indigo-600 px-2.5 py-1 text-[11px] font-medium text-white">
										Nouveau
									</span>
								{/if}
							</div>

							<h2 class="mt-3 text-lg font-semibold tracking-tight text-zinc-950 transition-colors group-hover:text-indigo-700 dark:text-zinc-100 dark:group-hover:text-indigo-300 sm:text-xl">
								{topic.title}
							</h2>

							<p class="mt-2 line-clamp-3 max-w-3xl text-sm leading-6 text-zinc-600 dark:text-zinc-300">
								{topic.content}
							</p>

							<div class="mt-4 flex flex-wrap gap-2 text-xs">
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
									Par {topic.author.email}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
									{topic.posts_count} réponse{topic.posts_count > 1 ? 's' : ''}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
									{topic.views_count} vue{topic.views_count > 1 ? 's' : ''}
								</span>
								<span
									class={`rounded-full px-2.5 py-1 ${
										topic.accepted_post_id
											? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300'
											: 'bg-amber-100 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300'
									}`}
								>
									{topic.accepted_post_id ? 'Résolu' : 'Ouvert'}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
									Mise à jour le {formatDate(topic.updated_at)}
								</span>
							</div>
						</div>
					</div>
				</a>
			{/each}
		{:else}
			<div class="px-4 py-10 text-center sm:px-6">
				<h2 class="text-lg font-semibold text-zinc-950 dark:text-zinc-100">Aucun sujet trouvé</h2>
				<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
					Essaie de modifier tes filtres ou crée un nouveau sujet.
				</p>

				<div class="mt-5">
					<a
						href="/forum/new"
						class="inline-flex rounded-2xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400"
					>
						Créer un sujet
					</a>
				</div>
			</div>
		{/if}
	</div>

	{#if topics.length > 0}
		<div class="border-t border-zinc-200 px-4 py-5 dark:border-zinc-800 sm:mt-6 sm:rounded-3xl sm:border sm:bg-white sm:px-5 dark:sm:bg-zinc-950/40">
			<div class="flex items-center justify-between">
				<div class="text-sm text-zinc-600 dark:text-zinc-300">Page {page}</div>

				<div class="flex gap-2">
					{#if page > 1}
						<a
							href={buildPageHref(page - 1)}
							class="rounded-2xl border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
						>
							Précédent
						</a>
					{/if}

					{#if hasNextPage}
						<a
							href={buildPageHref(page + 1)}
							class="rounded-2xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400"
						>
							Suivant
						</a>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>

<div class="fixed inset-x-0 bottom-0 z-30 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden">
	<div class="mx-auto max-w-sm rounded-[1.5rem] border border-zinc-200/70 bg-white/80 p-1.5 shadow-[0_10px_30px_rgba(0,0,0,0.10)] backdrop-blur-xl dark:border-zinc-800/70 dark:bg-zinc-900/80">
		<div class="grid grid-cols-3 gap-1.5">
			<a
				href="/"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100/80 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800/80 dark:hover:text-zinc-100"
			>
				<span class="text-base leading-none">⌂</span>
				<span>Accueil</span>
			</a>

			<a
				href={tutorialSlug ? `/tutos/${tutorialSlug}` : '/tutos'}
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100/80 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800/80 dark:hover:text-zinc-100"
			>
				<span class="text-base leading-none">←</span>
				<span>Tutos</span>
			</a>

			<a
				href="/forum/new"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] bg-gradient-to-r from-indigo-600 to-blue-600 px-3 py-2.5 text-sm font-semibold text-white shadow-sm transition active:scale-[0.98]"
			>
				<span class="text-base leading-none">＋</span>
				<span>Créer</span>
			</a>
		</div>
	</div>
</div>