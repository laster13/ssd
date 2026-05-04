<script lang="ts">
	import ImageUploadButton from '$lib/components/forum/ImageUploadButton.svelte';
	import MarkdownContent from '$lib/components/forum/MarkdownContent.svelte';
	import MarkdownPreview from '$lib/components/forum/MarkdownPreview.svelte';
	import RevisionHistoryModal from '$lib/components/forum/RevisionHistoryModal.svelte';
	import MarkTopicNotificationsRead from '$lib/components/notifications/MarkTopicNotificationsRead.svelte';
	import type { ForumPostRevision, ForumTopicRevision } from '$lib/types/forum';

	let { data, form } = $props();

	const { topic, relatedTopics, user, csrfToken, postsSort } = data;

	let editingTopic = $state(false);
	let editingPostId = $state<string | null>(null);
	let reportingPostId = $state<string | null>(null);

	let topicHistoryOpen = $state(false);
	let postHistoryOpen = $state(false);

	let topicRevisions = $state<ForumTopicRevision[]>([]);
	let postRevisions = $state<ForumPostRevision[]>([]);

	let topicHistoryLoading = $state(false);
	let postHistoryLoading = $state(false);

	let topicHistoryError = $state('');
	let postHistoryError = $state('');

	let historyPostLabel = $state('');

	let editTopicTitle = $state(topic.title);
	let editTopicContent = $state(topic.content);

	let replyContent = $state(form?.replyContent ?? '');
	let replyTargetType = $state<'topic' | 'post' | null>(
		form?.replyTargetType === 'post' || form?.replyTargetType === 'topic'
			? form.replyTargetType
			: null
	);
	let replyTargetId = $state<string>(form?.replyTargetId ?? '');

	const editReplyContent = new Map<string, string>();
	for (const post of topic.posts) {
		editReplyContent.set(post.id, post.content);
	}

	function formatDate(value: string) {
		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(value));
	}

	function buildPostsSortHref(sortValue: string) {
		const params = new URLSearchParams();
		if (sortValue && sortValue !== 'oldest') {
			params.set('posts_sort', sortValue);
		}
		return params.toString() ? `/forum/${topic.slug}?${params.toString()}` : `/forum/${topic.slug}`;
	}

	function insertReplyImage(markdown: string) {
		replyContent = `${replyContent}\n${markdown}\n`.trim();
	}

	function insertTopicImage(markdown: string) {
		editTopicContent = `${editTopicContent}\n${markdown}\n`.trim();
	}

	function insertEditReplyImage(postId: string, markdown: string) {
		const current = editReplyContent.get(postId) ?? '';
		editReplyContent.set(postId, `${current}\n${markdown}\n`.trim());
	}

	function findPostById(postId: string | null | undefined) {
		if (!postId) return null;
		return topic.posts.find((post) => post.id === postId) ?? null;
	}

	function excerpt(value: string, max = 140) {
		const cleaned = value
			.replace(/[#>*_`~-]/g, '')
			.replace(/\s+/g, ' ')
			.trim();

		if (cleaned.length <= max) return cleaned;
		return `${cleaned.slice(0, max).trim()}…`;
	}

	function openReplyToTopic() {
		replyTargetType = 'topic';
		replyTargetId = topic.id;
		if (!replyContent.trim()) {
			replyContent = '';
		}
	}

	function openReplyToPost(postId: string) {
		const parent = findPostById(postId);
		replyTargetType = 'post';
		replyTargetId = postId;

		if (!parent) return;

		const quoted = `@${parent.author.email}

> ${excerpt(parent.content)}

`;
		replyContent = quoted;
	}

	function closeReplyEditor() {
		replyTargetType = null;
		replyTargetId = '';
		replyContent = '';
	}

	function isReplyOpenForTopic() {
		return replyTargetType === 'topic';
	}

	function isReplyOpenForPost(postId: string) {
		return replyTargetType === 'post' && replyTargetId === postId;
	}

	function replyParentPostId() {
		return replyTargetType === 'post' ? replyTargetId : '';
	}

	async function openTopicHistory() {
		topicHistoryLoading = true;
		topicHistoryError = '';

		try {
			const response = await fetch(`/api/forum/topic-revisions/${topic.id}`);
			const payload = await response.json();

			if (!response.ok) {
				throw new Error(payload?.error || "Impossible de charger l'historique du sujet.");
			}

			topicRevisions = payload;
			topicHistoryOpen = true;
		} catch (err) {
			topicHistoryError =
				err instanceof Error ? err.message : "Impossible de charger l'historique du sujet.";
		} finally {
			topicHistoryLoading = false;
		}
	}

	async function openPostHistory(postId: string, label: string) {
		postHistoryLoading = true;
		postHistoryError = '';
		historyPostLabel = label;

		try {
			const response = await fetch(`/api/forum/post-revisions/${postId}`);
			const payload = await response.json();

			if (!response.ok) {
				throw new Error(payload?.error || "Impossible de charger l'historique du message.");
			}

			postRevisions = payload;
			postHistoryOpen = true;
		} catch (err) {
			postHistoryError =
				err instanceof Error ? err.message : "Impossible de charger l'historique du message.";
		} finally {
			postHistoryLoading = false;
		}
	}

	const canEditTopic = !!user && user.email === topic.author.email;
	const canModerateAsAdmin = !!user?.is_admin;
	const canOpenHistory = !!user;
</script>

<svelte:head>
	<title>{topic.title} | Forum SSD</title>
</svelte:head>

{#if user}
	<MarkTopicNotificationsRead link={`/forum/${topic.slug}`} enabled={true} />
{/if}

<div class="mx-auto w-full max-w-7xl py-6 sm:px-6 sm:py-8 lg:px-8">
	<div class="px-4 sm:px-0">
		<a
			href={topic.related_tutorial_slug ? `/tutos/${topic.related_tutorial_slug}` : '/forum'}
			class="text-sm font-medium text-zinc-600 underline underline-offset-4 dark:text-zinc-300"
		>
			← Retour
		</a>
	</div>

	<div
		class={`mt-6 grid gap-6 ${
			relatedTopics.length > 0 ? 'xl:grid-cols-[minmax(0,1fr)_320px]' : 'grid-cols-1'
		}`}
	>
		<div class="space-y-6">
			<section class="border-b border-zinc-200 px-4 pb-6 dark:border-zinc-800 sm:rounded-3xl sm:border sm:bg-white sm:p-6 sm:shadow-sm dark:sm:bg-zinc-950/40">
				<div class="flex flex-wrap items-center gap-2">
					<span class="rounded-full border border-zinc-200 px-2.5 py-1 text-[11px] font-medium text-zinc-700 dark:border-zinc-700 dark:text-zinc-200">
						{topic.category.name}
					</span>

					{#if topic.related_tutorial_slug}
						<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-[11px] font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
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
				</div>

				{#if !editingTopic}
					<h1 class="mt-4 text-3xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-100">
						{topic.title}
					</h1>

					<div class="mt-4 flex flex-wrap gap-x-4 gap-y-2 text-sm text-zinc-500 dark:text-zinc-400">
						<span>Par {topic.author.email}</span>
						<span>Créé le {formatDate(topic.created_at)}</span>
						<span>{topic.views_count} vue{topic.views_count > 1 ? 's' : ''}</span>
						<span>{topic.posts.length} réponse{topic.posts.length > 1 ? 's' : ''}</span>
						<span>{topic.accepted_post_id ? 'Résolu' : 'Ouvert'}</span>
						{#if topic.is_edited}
							<span>Modifié le {formatDate(topic.updated_at)}</span>
						{/if}
					</div>

					<div class="mt-6">
						<MarkdownContent content={topic.content} />
					</div>

					<div class="mt-6 flex flex-wrap gap-2">
						{#if user && !topic.is_locked}
							<button
								type="button"
								class="rounded-2xl bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
								onclick={openReplyToTopic}
							>
								Répondre
							</button>
						{/if}

						{#if canEditTopic}
							<button
								type="button"
								class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
								onclick={() => (editingTopic = true)}
							>
								Modifier le sujet
							</button>

							<form method="POST" action="?/deleteTopic">
								<input type="hidden" name="_csrf" value={csrfToken} />
								<input type="hidden" name="topic_id" value={topic.id} />
								<button
									type="submit"
									class="rounded-2xl border border-red-300 px-4 py-2.5 text-sm font-medium text-red-700 transition hover:bg-red-50 dark:border-red-900/60 dark:text-red-300 dark:hover:bg-red-950/30"
								>
									Supprimer le sujet
								</button>
							</form>
						{/if}

						{#if canOpenHistory && topic.is_edited}
							<button
								type="button"
								class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
								onclick={openTopicHistory}
								disabled={topicHistoryLoading}
							>
								{topicHistoryLoading ? 'Chargement...' : 'Voir l’historique'}
							</button>
						{/if}

						{#if canModerateAsAdmin}
							{#if topic.is_pinned}
								<form method="POST" action="?/unpinTopic">
									<input type="hidden" name="_csrf" value={csrfToken} />
									<input type="hidden" name="topic_id" value={topic.id} />
									<button
										type="submit"
										class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
									>
										Désépingler
									</button>
								</form>
							{:else}
								<form method="POST" action="?/pinTopic">
									<input type="hidden" name="_csrf" value={csrfToken} />
									<input type="hidden" name="topic_id" value={topic.id} />
									<button
										type="submit"
										class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
									>
										Épingler
									</button>
								</form>
							{/if}
						{/if}
					</div>

					{#if isReplyOpenForTopic() && user && !topic.is_locked}
						<div class="mt-6 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
							<div class="mb-3 flex items-center justify-between gap-3">
								<div>
									<h3 class="text-base font-semibold text-zinc-950 dark:text-zinc-100">
										Répondre au sujet
									</h3>
									<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
										Ta réponse sera ajoutée à la discussion principale.
									</p>
								</div>

								<button
									type="button"
									class="rounded-xl border border-zinc-300 px-3 py-2 text-sm text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
									onclick={closeReplyEditor}
								>
									Annuler
								</button>
							</div>

							<form method="POST" action="?/createReply" class="space-y-4">
								<input type="hidden" name="_csrf" value={csrfToken} />
								<input type="hidden" name="topic_id" value={topic.id} />
								<input type="hidden" name="parent_post_id" value="" />
								<input type="hidden" name="reply_target_type" value="topic" />
								<input type="hidden" name="reply_target_id" value={topic.id} />

								<div class="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
									<div class="space-y-4">
										<div>
											<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
												Ta réponse
											</label>
											<textarea
												name="content"
												rows="8"
												required
												minlength="3"
												maxlength="20000"
												bind:value={replyContent}
												class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
												placeholder="Explique la solution ou la piste à tester."
											></textarea>
										</div>

										<div class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950/60">
											<ImageUploadButton onUploaded={insertReplyImage} />
										</div>
									</div>

									<div class="border-t border-zinc-200 pt-4 dark:border-zinc-800 xl:border-l xl:border-t-0 xl:pl-6 xl:pt-0">
										<label class="mb-3 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
											Aperçu
										</label>
										<MarkdownPreview content={replyContent} />
									</div>
								</div>

								<div class="flex flex-wrap gap-3">
									<button
										type="submit"
										class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
									>
										Publier la réponse
									</button>

									<button
										type="button"
										class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
										onclick={closeReplyEditor}
									>
										Annuler
									</button>
								</div>
							</form>
						</div>
					{/if}

					{#if topicHistoryError}
						<div class="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
							{topicHistoryError}
						</div>
					{/if}
				{:else}
					<form method="POST" action="?/editTopic" class="mt-6 space-y-5">
						<input type="hidden" name="_csrf" value={csrfToken} />
						<input type="hidden" name="topic_id" value={topic.id} />
						<input type="hidden" name="related_tutorial_slug" value={topic.related_tutorial_slug ?? ''} />

						<div>
							<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">Titre</label>
							<input
								name="title"
								type="text"
								required
								minlength="5"
								maxlength="200"
								bind:value={editTopicTitle}
								class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
							/>
						</div>

						<div class="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
							<div class="space-y-4">
								<div>
									<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">Contenu</label>
									<textarea
										name="content"
										rows="14"
										required
										minlength="10"
										maxlength="20000"
										bind:value={editTopicContent}
										class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
									></textarea>
								</div>

								<div class="rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
									<ImageUploadButton onUploaded={insertTopicImage} />
								</div>
							</div>

							<div class="border-t border-zinc-200 pt-4 dark:border-zinc-800 xl:border-l xl:border-t-0 xl:pl-6 xl:pt-0">
								<label class="mb-3 block text-sm font-medium text-zinc-800 dark:text-zinc-200">Aperçu</label>
								<MarkdownPreview content={editTopicContent} />
							</div>
						</div>

						<div class="flex flex-wrap gap-3">
							<button
								type="submit"
								class="rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
							>
								Enregistrer
							</button>
							<button
								type="button"
								class="rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
								onclick={() => {
									editingTopic = false;
									editTopicTitle = topic.title;
									editTopicContent = topic.content;
								}}
							>
								Annuler
							</button>
						</div>
					</form>
				{/if}

				{#if form?.topicError}
					<div class="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
						{form.topicError}
					</div>
				{/if}
			</section>

			{#if topic.accepted_post_id}
				<section class="border-b border-emerald-200 bg-emerald-50/60 px-4 py-6 dark:border-emerald-900/40 dark:bg-emerald-950/20 sm:rounded-3xl sm:border sm:p-6">
					<div class="flex items-center gap-3">
						<div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-600 text-sm font-semibold text-white">
							✓
						</div>
						<div>
							<h2 class="text-lg font-semibold text-emerald-800 dark:text-emerald-300">
								Solution retenue
							</h2>
							<p class="text-sm text-emerald-700/80 dark:text-emerald-200/70">
								La réponse ci-dessous a été validée comme solution.
							</p>
						</div>
					</div>

					{#each topic.posts as post}
						{#if post.id === topic.accepted_post_id}
							<div class="mt-5 rounded-2xl border border-emerald-200 bg-white p-4 dark:border-emerald-900/40 dark:bg-zinc-950/50">
								<div class="mb-3 text-sm text-zinc-500 dark:text-zinc-400">
									{post.author.email} • {formatDate(post.created_at)}
									{#if post.is_edited}
										• édité
									{/if}
								</div>
								<MarkdownContent content={post.content} />
							</div>
						{/if}
					{/each}
				</section>
			{/if}

			<section class="border-b border-zinc-200 dark:border-zinc-800 sm:overflow-hidden sm:rounded-3xl sm:border sm:border-zinc-200 sm:bg-white sm:shadow-sm dark:sm:border-zinc-800 dark:sm:bg-zinc-950/40">
				<div class="px-4 py-6 sm:px-6">
					<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
						<h2 class="text-2xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-100">
							Réponses ({topic.posts.length})
						</h2>

						<div class="flex flex-wrap gap-2">
							<a
								href={buildPostsSortHref('oldest')}
								class={`rounded-2xl border px-4 py-2 text-sm font-medium transition ${
									postsSort === 'oldest'
										? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
										: 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800'
								}`}
							>
								Plus anciennes
							</a>

							<a
								href={buildPostsSortHref('newest')}
								class={`rounded-2xl border px-4 py-2 text-sm font-medium transition ${
									postsSort === 'newest'
										? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
										: 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800'
								}`}
							>
								Plus récentes
							</a>

							<a
								href={buildPostsSortHref('useful')}
								class={`rounded-2xl border px-4 py-2 text-sm font-medium transition ${
									postsSort === 'useful'
										? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
										: 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800'
								}`}
							>
								Plus utiles
							</a>
						</div>
					</div>
				</div>

				{#if topic.posts.length > 0}
					<div class="divide-y divide-zinc-200 dark:divide-zinc-800">
						{#each topic.posts as post}
							<article class="px-4 py-5 transition sm:px-6">
								<div class="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
									<div class="min-w-0 flex-1">
										<div class="flex flex-wrap items-center gap-x-3 gap-y-2 text-sm text-zinc-500 dark:text-zinc-400">
											<div class="flex items-center gap-3">
												<div class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-200 bg-zinc-100 text-sm font-semibold text-zinc-900 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100">
													{post.author.email.slice(0, 1).toUpperCase()}
												</div>
												<div>
													<div class="font-medium text-zinc-900 dark:text-zinc-100">{post.author.email}</div>
													<div class="text-xs">{formatDate(post.created_at)}</div>
												</div>
											</div>

											<span>{post.useful_votes_count} utile{post.useful_votes_count > 1 ? 's' : ''}</span>

											{#if post.parent_post_id}
												{@const parent = findPostById(post.parent_post_id)}
												<span class="rounded-full bg-zinc-100 px-2.5 py-1 text-[11px] font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
													{parent ? `Réponse à ${parent.author.email}` : 'Réponse à un message'}
												</span>
											{/if}

											{#if post.is_edited}
												<span>édité</span>
											{/if}
										</div>
									</div>

									<div class="flex flex-wrap items-center gap-2">
										{#if user && !topic.is_locked}
											<button
												type="button"
												class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => openReplyToPost(post.id)}
											>
												Répondre
											</button>
										{/if}

										{#if topic.accepted_post_id === post.id}
											<span class="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
												Solution retenue
											</span>
										{:else if user && user.email === topic.author.email}
											<form method="POST" action="?/acceptReply">
												<input type="hidden" name="_csrf" value={csrfToken} />
												<input type="hidden" name="post_id" value={post.id} />
												<button
													type="submit"
													class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												>
													Marquer comme solution
												</button>
											</form>
										{/if}

										{#if user}
											<form method="POST" action="?/voteReply">
												<input type="hidden" name="_csrf" value={csrfToken} />
												<input type="hidden" name="post_id" value={post.id} />
												<button
													type="submit"
													class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												>
													Vote utile
												</button>
											</form>
										{/if}

										{#if user && user.email === post.author.email}
											<button
												type="button"
												class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => (editingPostId = editingPostId === post.id ? null : post.id)}
											>
												Modifier
											</button>

											<form method="POST" action="?/deleteReply">
												<input type="hidden" name="_csrf" value={csrfToken} />
												<input type="hidden" name="post_id" value={post.id} />
												<button
													type="submit"
													class="rounded-xl border border-red-300 px-3 py-1.5 text-xs font-medium text-red-700 transition hover:bg-red-50 dark:border-red-900/60 dark:text-red-300 dark:hover:bg-red-950/30"
												>
													Supprimer
												</button>
											</form>
										{/if}

										{#if canOpenHistory && post.is_edited}
											<button
												type="button"
												class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => openPostHistory(post.id, `Historique du message de ${post.author.email}`)}
												disabled={postHistoryLoading}
											>
												{postHistoryLoading ? 'Chargement...' : 'Historique'}
											</button>
										{/if}

										{#if user}
											<button
												type="button"
												class="rounded-xl border border-zinc-300 px-3 py-1.5 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => (reportingPostId = reportingPostId === post.id ? null : post.id)}
											>
												Signaler
											</button>
										{/if}
									</div>
								</div>

								{#if editingPostId === post.id}
									<form method="POST" action="?/editReply" class="mt-5 space-y-4">
										<input type="hidden" name="_csrf" value={csrfToken} />
										<input type="hidden" name="post_id" value={post.id} />

										<div class="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
											<div class="space-y-4">
												<textarea
													name="content"
													rows="10"
													required
													minlength="3"
													maxlength="20000"
													value={editReplyContent.get(post.id) ?? ''}
													oninput={(event) => {
														editReplyContent.set(
															post.id,
															(event.currentTarget as HTMLTextAreaElement).value
														);
													}}
													class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
												></textarea>

												<div class="rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
													<ImageUploadButton onUploaded={(markdown) => insertEditReplyImage(post.id, markdown)} />
												</div>
											</div>

											<div class="border-t border-zinc-200 pt-4 dark:border-zinc-800 xl:border-l xl:border-t-0 xl:pl-6 xl:pt-0">
												<MarkdownPreview content={editReplyContent.get(post.id) ?? ''} />
											</div>
										</div>

										<div class="flex flex-wrap gap-3">
											<button
												type="submit"
												class="rounded-2xl bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
											>
												Enregistrer
											</button>
											<button
												type="button"
												class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => {
													editingPostId = null;
													editReplyContent.set(post.id, post.content);
												}}
											>
												Annuler
											</button>
										</div>
									</form>
								{:else}
									<div class="mt-5">
										<MarkdownContent content={post.content} />
									</div>
								{/if}

								{#if isReplyOpenForPost(post.id) && user && !topic.is_locked}
									<div class="mt-5 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
										<div class="mb-3 flex items-center justify-between gap-3">
											<div>
												<h3 class="text-base font-semibold text-zinc-950 dark:text-zinc-100">
													Répondre à {post.author.email}
												</h3>
												<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
													Ta réponse sera liée à ce message.
												</p>
											</div>

											<button
												type="button"
												class="rounded-xl border border-zinc-300 px-3 py-2 text-sm text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={closeReplyEditor}
											>
												Annuler
											</button>
										</div>

										<div class="mb-4 rounded-2xl border border-zinc-200 bg-white p-4 text-sm text-zinc-600 dark:border-zinc-800 dark:bg-zinc-950/60 dark:text-zinc-300">
											<p class="font-medium text-zinc-900 dark:text-zinc-100">
												Message ciblé
											</p>
											<p class="mt-2 line-clamp-3">{excerpt(post.content, 180)}</p>
										</div>

										<form method="POST" action="?/createReply" class="space-y-4">
											<input type="hidden" name="_csrf" value={csrfToken} />
											<input type="hidden" name="topic_id" value={topic.id} />
											<input type="hidden" name="parent_post_id" value={replyParentPostId()} />
											<input type="hidden" name="reply_target_type" value="post" />
											<input type="hidden" name="reply_target_id" value={post.id} />

											<div class="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
												<div class="space-y-4">
													<div>
														<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
															Ta réponse
														</label>
														<textarea
															name="content"
															rows="8"
															required
															minlength="3"
															maxlength="20000"
															bind:value={replyContent}
															class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
															placeholder="Explique la solution ou la piste à tester."
														></textarea>
													</div>

													<div class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950/60">
														<ImageUploadButton onUploaded={insertReplyImage} />
													</div>
												</div>

												<div class="border-t border-zinc-200 pt-4 dark:border-zinc-800 xl:border-l xl:border-t-0 xl:pl-6 xl:pt-0">
													<label class="mb-3 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
														Aperçu
													</label>
													<MarkdownPreview content={replyContent} />
												</div>
											</div>

											<div class="flex flex-wrap gap-3">
												<button
													type="submit"
													class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
												>
													Publier la réponse
												</button>

												<button
													type="button"
													class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
													onclick={closeReplyEditor}
												>
													Annuler
												</button>
											</div>
										</form>
									</div>
								{/if}

								{#if reportingPostId === post.id}
									<form method="POST" action="?/reportReply" class="mt-5 space-y-3 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
										<input type="hidden" name="_csrf" value={csrfToken} />
										<input type="hidden" name="post_id" value={post.id} />

										<div>
											<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
												Raison
											</label>
											<select
												name="reason"
												class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
											>
												<option value="spam">Spam</option>
												<option value="offtopic">Hors sujet</option>
												<option value="abuse">Abus</option>
												<option value="other">Autre</option>
											</select>
										</div>

										<div>
											<label class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200">
												Détails
											</label>
											<textarea
												name="details"
												rows="3"
												class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
											></textarea>
										</div>

										<div class="flex flex-wrap gap-3">
											<button
												type="submit"
												class="rounded-2xl bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
											>
												Envoyer le signalement
											</button>
											<button
												type="button"
												class="rounded-2xl border border-zinc-300 px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
												onclick={() => (reportingPostId = null)}
											>
												Annuler
											</button>
										</div>
									</form>
								{/if}
							</article>
						{/each}
					</div>
				{:else}
					<div class="px-4 py-10 text-center sm:px-6">
						<h3 class="text-lg font-semibold text-zinc-950 dark:text-zinc-100">
							Aucune réponse pour le moment
						</h3>
						<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
							Sois le premier à proposer une piste ou une solution.
						</p>

						{#if user && !topic.is_locked}
							<div class="mt-5">
								<button
									type="button"
									class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
									onclick={openReplyToTopic}
								>
									Répondre
								</button>
							</div>
						{/if}
					</div>
				{/if}

				{#if form?.replyError}
					<div class="px-4 pb-4 sm:px-6">
						<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
							{form.replyError}
						</div>
					</div>
				{/if}

				{#if postHistoryError}
					<div class="px-4 pb-4 sm:px-6">
						<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
							{postHistoryError}
						</div>
					</div>
				{/if}
			</section>
		</div>

		{#if relatedTopics.length > 0}
			<aside class="space-y-6">
				<section class="border-b border-zinc-200 px-4 py-5 dark:border-zinc-800 sm:rounded-3xl sm:border sm:bg-white sm:p-5 sm:shadow-sm dark:sm:bg-zinc-950/40">
					<h2 class="text-base font-semibold text-zinc-950 dark:text-zinc-100">Autres sujets liés</h2>

					<div class="mt-4 space-y-3">
						{#each relatedTopics as item}
							<a
								href={`/forum/${item.slug}`}
								class="block rounded-2xl border border-zinc-200 p-4 transition hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900/50"
							>
								<div class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
									{item.title}
								</div>
								<div class="mt-2 text-xs text-zinc-500 dark:text-zinc-400">
									{item.posts_count} réponse{item.posts_count > 1 ? 's' : ''} • {item.views_count} vue{item.views_count > 1 ? 's' : ''}
								</div>
							</a>
						{/each}
					</div>
				</section>
			</aside>
		{/if}
	</div>
</div>

<RevisionHistoryModal
	open={topicHistoryOpen}
	data={{ mode: 'topic', title: `Historique du sujet`, revisions: topicRevisions }}
	onClose={() => {
		topicHistoryOpen = false;
	}}
/>

<RevisionHistoryModal
	open={postHistoryOpen}
	data={{ mode: 'post', title: historyPostLabel || 'Historique du message', revisions: postRevisions }}
	onClose={() => {
		postHistoryOpen = false;
	}}
/>