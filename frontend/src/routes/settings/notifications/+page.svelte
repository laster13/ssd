<script lang="ts">
	let { data, form } = $props();

	const current = form?.preferences ??
		form?.values ??
		data.preferences ?? {
			notify_topic_replies: true,
			notify_accepted_answer: true,
			notify_participated_topic_replies: true
		};
</script>

<svelte:head>
	<title>Préférences de notifications | SSD</title>
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-8">
	<div class="mb-6">
		<a
			href="/notifications"
			class="text-sm font-medium text-zinc-600 underline underline-offset-4 dark:text-zinc-300"
		>
			← Retour aux notifications
		</a>
	</div>

	<section class="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-950/60">
		<p class="text-sm font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
			Réglages
		</p>
		<h1 class="mt-2 text-3xl font-semibold text-zinc-900 dark:text-zinc-100">
			Préférences de notifications
		</h1>
		<p class="mt-3 text-sm text-zinc-600 dark:text-zinc-300">
			Choisis les événements du forum qui doivent générer des notifications.
		</p>

		{#if data.loadError}
			<div class="mt-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
				{data.loadError}
			</div>
		{/if}

		{#if form?.error}
			<div class="mt-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
				{form.error}
			</div>
		{/if}

		{#if form?.success}
			<div class="mt-5 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900/60 dark:bg-emerald-950/40 dark:text-emerald-300">
				Préférences enregistrées.
			</div>
		{/if}

		<form method="POST" class="mt-6 space-y-4">
			<input type="hidden" name="_csrf" value={data.csrfToken} />

			<label class="flex items-start gap-3 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/50">
				<input
					type="checkbox"
					name="notify_topic_replies"
					checked={current.notify_topic_replies}
					class="mt-1"
				/>
				<span>
					<span class="block text-sm font-medium text-zinc-900 dark:text-zinc-100">
						Réponses à mes sujets
					</span>
					<span class="mt-1 block text-sm text-zinc-600 dark:text-zinc-300">
						Reçois une notification quand quelqu’un répond à un sujet que tu as créé.
					</span>
				</span>
			</label>

			<label class="flex items-start gap-3 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/50">
				<input
					type="checkbox"
					name="notify_accepted_answer"
					checked={current.notify_accepted_answer}
					class="mt-1"
				/>
				<span>
					<span class="block text-sm font-medium text-zinc-900 dark:text-zinc-100">
						Réponse retenue comme solution
					</span>
					<span class="mt-1 block text-sm text-zinc-600 dark:text-zinc-300">
						Reçois une notification quand une de tes réponses est marquée comme solution.
					</span>
				</span>
			</label>

			<label class="flex items-start gap-3 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/50">
				<input
					type="checkbox"
					name="notify_participated_topic_replies"
					checked={current.notify_participated_topic_replies}
					class="mt-1"
				/>
				<span>
					<span class="block text-sm font-medium text-zinc-900 dark:text-zinc-100">
						Activité dans les sujets où j’ai participé
					</span>
					<span class="mt-1 block text-sm text-zinc-600 dark:text-zinc-300">
						Reçois une notification quand quelqu’un répond dans un sujet où tu as déjà posté.
					</span>
				</span>
			</label>

			<div class="pt-2">
				<button
					type="submit"
					class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
				>
					Enregistrer
				</button>
			</div>
		</form>
	</section>
</div>