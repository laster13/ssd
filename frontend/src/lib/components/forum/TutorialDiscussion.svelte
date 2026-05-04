<script lang="ts">
	import { onMount } from 'svelte';
	import ImageUploadButton from '$lib/components/forum/ImageUploadButton.svelte';
	import MarkdownPreview from '$lib/components/forum/MarkdownPreview.svelte';
	import type { ForumTopicListItem } from '$lib/types/forum';

	type Tutorial = {
		slug: string;
		title: string;
	};

	let {
		tutorial,
		topics = [],
		user = null,
		csrfToken,
		form = null
	}: {
		tutorial: Tutorial;
		topics: ForumTopicListItem[];
		user: { email: string } | null;
		csrfToken: string;
		form?: {
			createTopicError?: string;
			createTopicSuccess?: boolean;
			title?: string;
			content?: string;
		} | null;
	} = $props();

	let liveContent = $state(form?.content ?? '');
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
		const clean = value.replace(/[#>*_`~-]/g, '').trim();
		if (clean.length <= max) return clean;
		return `${clean.slice(0, max).trim()}…`;
	}

	function insertMarkdown(markdown: string) {
		liveContent = `${liveContent}\n${markdown}\n`.trim();
	}

	function topicLink(slug: string) {
		return `/forum/${slug}`;
	}

	function isUnreadTopic(slug: string) {
		return unreadTopicLinks.has(topicLink(slug));
	}

	const resolvedCount = topics.filter((topic) => !!topic.accepted_post_id).length;
</script>

<section class="mt-12 rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-950/60">
	<div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
		<div>
			<p class="text-sm font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
				Discussion
			</p>
			<h2 class="mt-1 text-2xl font-semibold text-zinc-900 dark:text-zinc-100">
				Questions sur ce tutoriel
			</h2>
			<p class="mt-2 max-w-2xl text-sm text-zinc-600 dark:text-zinc-300">
				Retrouve les sujets liés à <span class="font-medium">{tutorial.title}</span>, ou pose ta
				propre question si tu bloques sur une étape.
			</p>
		</div>

		<div class="grid grid-cols-2 gap-3">
			<div class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200">
				<div class="text-xs text-zinc-500 dark:text-zinc-400">Sujets</div>
				<div class="mt-1 text-lg font-semibold">{topics.length}</div>
			</div>
			<div class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200">
				<div class="text-xs text-zinc-500 dark:text-zinc-400">Résolus</div>
				<div class="mt-1 text-lg font-semibold">{resolvedCount}</div>
			</div>
		</div>
	</div>

	{#if topics.length > 0}
		<div class="mt-6 space-y-4">
			{#each topics as topic}
				<a
					href={`/forum/${topic.slug}`}
					class={`block rounded-2xl border p-4 transition ${
						isUnreadTopic(topic.slug)
							? 'border-blue-200 bg-blue-50/50 hover:border-blue-300 hover:bg-white dark:border-blue-900/40 dark:bg-blue-950/15 dark:hover:border-blue-800/60 dark:hover:bg-zinc-900'
							: 'border-zinc-200 bg-zinc-50 hover:border-zinc-300 hover:bg-white dark:border-zinc-800 dark:bg-zinc-900/70 dark:hover:border-zinc-700 dark:hover:bg-zinc-900'
					}`}
				>
					<div class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
						<div class="min-w-0">
							<div class="flex flex-wrap items-center gap-2">
								<h3 class="text-base font-semibold text-zinc-900 dark:text-zinc-100">
									{topic.title}
								</h3>

								{#if topic.is_pinned}
									<span class="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-medium text-amber-700 dark:bg-amber-950/50 dark:text-amber-300">
										Épinglé
									</span>
								{/if}

								{#if topic.accepted_post_id}
									<span class="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300">
										Résolu
									</span>
								{/if}

								{#if topic.is_locked}
									<span class="rounded-full bg-rose-100 px-2.5 py-1 text-xs font-medium text-rose-700 dark:bg-rose-950/50 dark:text-rose-300">
										Verrouillé
									</span>
								{/if}

								{#if topic.is_edited}
									<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
										Édité
									</span>
								{/if}

								{#if isUnreadTopic(topic.slug)}
									<span class="rounded-full bg-blue-600 px-2.5 py-1 text-xs font-medium text-white">
										Nouveau
									</span>
								{/if}
							</div>

							<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
								{excerpt(topic.content)}
							</p>
						</div>

						<div class="shrink-0 text-sm text-zinc-500 dark:text-zinc-400">
							<div>{topic.posts_count} réponse{topic.posts_count > 1 ? 's' : ''}</div>
							<div class="mt-1">{topic.views_count} vue{topic.views_count > 1 ? 's' : ''}</div>
						</div>
					</div>

					<div class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-zinc-500 dark:text-zinc-400">
						<span>Par {topic.author.email}</span>
						<span>Mis à jour le {formatDate(topic.updated_at)}</span>
					</div>
				</a>
			{/each}

			<div class="pt-2">
				<a
					href={`/forum?tutorial=${tutorial.slug}`}
					class="inline-flex rounded-2xl border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
				>
					Voir toutes les discussions
				</a>
			</div>
		</div>
	{:else}
		<div class="mt-6 rounded-2xl border border-dashed border-zinc-300 bg-zinc-50 p-5 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/50 dark:text-zinc-300">
			Aucun sujet n’est encore lié à ce tutoriel.
		</div>
	{/if}

	<div class="mt-8 border-t border-zinc-200 pt-8 dark:border-zinc-800">
		<h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Poser une question</h3>
		<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
			Crée un sujet qui sera automatiquement rattaché à ce tutoriel.
		</p>

		{#if user}
			<form method="POST" action="?/createTopic" class="mt-5 space-y-4">
				<input type="hidden" name="_csrf" value={csrfToken} />
				<input type="hidden" name="related_tutorial_slug" value={tutorial.slug} />
				<input type="hidden" name="category_slug" value="tutoriels" />

				<div>
					<label for="forum-title" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Titre
					</label>
					<input
						id="forum-title"
						name="title"
						type="text"
						required
						minlength="5"
						maxlength="200"
						value={form?.title ?? ''}
						placeholder="Ex. Erreur 502 à la fin du tutoriel"
						class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
					/>
				</div>

				<div class="grid gap-4 lg:grid-cols-2">
					<div class="space-y-3">
						<div>
							<label for="forum-content" class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
								Message en markdown
							</label>
							<textarea
								id="forum-content"
								name="content"
								required
								minlength="10"
								maxlength="20000"
								rows="8"
								bind:value={liveContent}
								placeholder="Décris ton problème, l’étape où tu bloques et le message d’erreur éventuel."
								class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
							></textarea>
						</div>

						<ImageUploadButton onUploaded={insertMarkdown} />
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
							Aperçu
						</label>
						<MarkdownPreview content={liveContent} />
					</div>
				</div>

				{#if form?.createTopicError}
					<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
						{form.createTopicError}
					</div>
				{/if}

				{#if form?.createTopicSuccess}
					<div class="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900/60 dark:bg-emerald-950/40 dark:text-emerald-300">
						Sujet créé avec succès.
					</div>
				{/if}

				<button
					type="submit"
					class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
				>
					Créer le sujet
				</button>
			</form>
		{:else}
			<div class="mt-5 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200">
				Tu dois être connecté pour poser une question.
				<a href={`/login?next=/tutos/${tutorial.slug}`} class="ml-1 font-medium underline underline-offset-4">
					Se connecter
				</a>
			</div>
		{/if}
	</div>
</section>