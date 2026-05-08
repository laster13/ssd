<script lang="ts">
	import { onMount } from 'svelte';
	import type { ForumTopicListItem } from '$lib/types/forum';

	let {
		tutorial,
		topics,
		user,
		csrfToken: _csrfToken,
		form: _form
	}: {
		tutorial: {
			slug: string;
			title: string;
		};
		topics: ForumTopicListItem[];
		user: { email: string } | null;
		csrfToken?: string;
		form?: {
			createTopicError?: string;
			createTopicSuccess?: boolean;
		} | null;
	} = $props();

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

	function excerpt(value: string, max = 180) {
		const cleaned = value.replace(/\s+/g, ' ').trim();
		if (cleaned.length <= max) return cleaned;
		return `${cleaned.slice(0, max).trim()}…`;
	}

	function topicLink(slug: string) {
		return `/forum/${slug}`;
	}

	function isUnreadTopic(slug: string) {
		return unreadTopicLinks.has(topicLink(slug));
	}

	function createTopicHref() {
		const params = new URLSearchParams();
		params.set('tutorial', tutorial.slug);
		params.set('tutorial_title', tutorial.title);
		params.set('category', 'tutoriels');
		return `/forum/new?${params.toString()}`;
	}

	const resolvedCount = topics.filter((topic) => !!topic.accepted_post_id).length;
</script>

<section class="mt-8 space-y-5 sm:mt-10 sm:space-y-6">
	<div class="px-3 sm:px-0">
		<p class="text-xs font-semibold uppercase tracking-[0.14em] text-violet-600 dark:text-violet-300">
			Discussion
		</p>

		<h2 class="mt-2 text-2xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-100 sm:text-3xl">
			Questions sur ce tutoriel
		</h2>

		<p class="mt-3 max-w-3xl text-sm leading-6 text-zinc-600 dark:text-zinc-300">
			Retrouve les sujets liés à {tutorial.title}, ou pose ta propre question si tu bloques sur une étape.
		</p>
	</div>

	<div class="grid gap-4 px-3 sm:grid-cols-2 sm:px-0">
		<div class="rounded-2xl border border-zinc-200 bg-white px-4 py-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
			<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Sujets
			</p>
			<p class="mt-2 text-2xl font-semibold text-zinc-950 dark:text-zinc-100">{topics.length}</p>
		</div>

		<div class="rounded-2xl border border-zinc-200 bg-white px-4 py-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
			<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Résolus
			</p>
			<p class="mt-2 text-2xl font-semibold text-zinc-950 dark:text-zinc-100">{resolvedCount}</p>
		</div>
	</div>

	{#if topics.length > 0}
		<div class="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
			{#each topics as topic, index}
				<a
					href={topicLink(topic.slug)}
					class={`group block px-4 py-4 transition hover:bg-zinc-50 dark:hover:bg-zinc-800/50 sm:px-5 ${
						isUnreadTopic(topic.slug) ? 'bg-violet-50/60 dark:bg-violet-950/20' : ''
					}`}
				>
					<div class="flex flex-col gap-3 xl:flex-row xl:items-start xl:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex min-w-0 flex-wrap items-center gap-2">
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

								{#if topic.is_locked}
									<span class="rounded-full bg-rose-100 px-2.5 py-1 text-[11px] font-medium text-rose-700 dark:bg-rose-950/40 dark:text-rose-300">
										Verrouillé
									</span>
								{/if}

								{#if topic.is_edited}
									<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-[11px] font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
										Édité
									</span>
								{/if}

								{#if isUnreadTopic(topic.slug)}
									<span class="rounded-full bg-violet-600 px-2.5 py-1 text-[11px] font-medium text-white">
										Nouveau
									</span>
								{/if}
							</div>

							<h3 class="mt-3 break-words text-base font-semibold tracking-tight text-zinc-950 transition-colors group-hover:text-violet-700 dark:text-zinc-100 dark:group-hover:text-violet-300 sm:text-lg">
								{topic.title}
							</h3>

							<p class="mt-2 line-clamp-2 max-w-3xl break-words text-sm leading-6 text-zinc-600 dark:text-zinc-300">
								{excerpt(topic.content)}
							</p>

							<div class="mt-3 flex flex-wrap gap-2 text-xs text-zinc-500 dark:text-zinc-400">
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
									{topic.posts_count} réponse{topic.posts_count > 1 ? 's' : ''}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
									{topic.views_count} vue{topic.views_count > 1 ? 's' : ''}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
									Par {topic.author.email}
								</span>
								<span class="rounded-full bg-zinc-100 px-2.5 py-1 dark:bg-zinc-800">
									Mis à jour le {formatDate(topic.updated_at)}
								</span>
							</div>
						</div>

						<div class="flex min-w-0 items-center gap-2 text-sm font-medium text-violet-700 dark:text-violet-300 xl:ml-6 xl:shrink-0">
							<span>Ouvrir</span>
							<span aria-hidden="true">→</span>
						</div>
					</div>
				</a>

				{#if index < topics.length - 1}
					<div class="mx-4 border-t border-zinc-200 dark:border-zinc-800 sm:mx-5"></div>
				{/if}
			{/each}
		</div>

		<div class="px-3 sm:px-0">
			<a
				href={`/forum?tutorial=${tutorial.slug}`}
				class="inline-flex items-center gap-2 rounded-2xl border border-zinc-300 px-4 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				Voir toutes les discussions
				<span aria-hidden="true">→</span>
			</a>
		</div>
	{:else}
		<div class="rounded-3xl border border-dashed border-zinc-300 bg-zinc-50 px-4 py-6 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/50 dark:text-zinc-300">
			Aucun sujet n’est encore lié à ce tutoriel.
		</div>
	{/if}

	<div class="rounded-3xl border border-violet-200 bg-violet-50/70 p-5 dark:border-violet-500/20 dark:bg-violet-500/10">
		<h3 class="text-lg font-semibold text-zinc-950 dark:text-zinc-100">
			Poser une question
		</h3>

		<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
			Crée un sujet automatiquement rattaché à ce tutoriel, avec un titre et un message déjà préparés.
		</p>

		<div class="mt-4">
			<a
				href={createTopicHref()}
				class="inline-flex items-center justify-center rounded-2xl bg-violet-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-violet-500 dark:bg-violet-500 dark:hover:bg-violet-400"
			>
				Poser une question sur ce tutoriel
			</a>
		</div>

		{#if !user}
			<p class="mt-3 text-xs text-zinc-500 dark:text-zinc-400">
				Tu pourras te connecter avant publication si nécessaire.
			</p>
		{/if}
	</div>
</section>