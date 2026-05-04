<script lang="ts">
	let { data, form } = $props();

	const { reports, status, loadError, csrfToken } = data;

	function formatDate(value: string | null) {
		if (!value) return '—';
		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(value));
	}
</script>

<svelte:head>
	<title>Signalements forum | Admin SSD</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8">
	<div class="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
		<div>
			<p class="text-sm font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
				Administration
			</p>
			<h1 class="mt-2 text-3xl font-semibold text-zinc-900 dark:text-zinc-100">
				Signalements forum
			</h1>
			<p class="mt-3 max-w-3xl text-sm text-zinc-600 dark:text-zinc-300">
				Gère les contenus signalés par les utilisateurs, supprime les messages problématiques ou
				classe les signalements.
			</p>
		</div>

		<a
			href="/forum"
			class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
		>
			Retour au forum
		</a>
	</div>

	<form method="GET" class="mb-6 flex flex-wrap gap-3 rounded-3xl border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-950/60">
		<select
			name="status"
			class="rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
		>
			<option value="" selected={status === ''}>Tous</option>
			<option value="open" selected={status === 'open'}>Ouverts</option>
			<option value="resolved" selected={status === 'resolved'}>Résolus</option>
			<option value="dismissed" selected={status === 'dismissed'}>Ignorés</option>
		</select>

		<button
			type="submit"
			class="rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
		>
			Filtrer
		</button>

		<a
			href="/admin/forum/reports"
			class="rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
		>
			Réinitialiser
		</a>
	</form>

	{#if loadError}
		<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
			{loadError}
		</div>
	{:else if form?.error}
		<div class="mb-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
			{form.error}
		</div>
	{/if}

	<div class="space-y-4">
		{#if reports.length > 0}
			{#each reports as report}
				<section class="rounded-3xl border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-950/60">
					<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-2">
								<span class="rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
									{report.reason}
								</span>

								{#if report.status === 'open'}
									<span class="rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
										Ouvert
									</span>
								{:else if report.status === 'resolved'}
									<span class="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
										Résolu
									</span>
								{:else}
									<span class="rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
										Ignoré
									</span>
								{/if}

								{#if report.post.is_deleted}
									<span class="rounded-full bg-rose-100 px-3 py-1 text-xs font-medium text-rose-700 dark:bg-rose-950/40 dark:text-rose-300">
										Message supprimé
									</span>
								{/if}
							</div>

							<h2 class="mt-3 text-lg font-semibold text-zinc-900 dark:text-zinc-100">
								{report.post.topic_title}
							</h2>

							<div class="mt-3 flex flex-wrap gap-x-4 gap-y-2 text-xs text-zinc-500 dark:text-zinc-400">
								<span>Signalé par {report.reporter.email}</span>
								<span>Auteur du message : {report.post.post_author.email}</span>
								<span>Créé le {formatDate(report.created_at)}</span>
								{#if report.reviewed_by}
									<span>Traité par {report.reviewed_by.email}</span>
									<span>Le {formatDate(report.reviewed_at)}</span>
								{/if}
							</div>

							{#if report.details}
								<div class="mt-4 rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-700 dark:bg-zinc-900 dark:text-zinc-200">
									<div class="mb-1 text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
										Détails du signalement
									</div>
									{report.details}
								</div>
							{/if}

							<div class="mt-4 rounded-2xl border border-zinc-200 p-4 dark:border-zinc-800">
								<div class="mb-2 text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
									Message signalé
								</div>
								<p class="whitespace-pre-wrap break-words text-sm leading-6 text-zinc-800 dark:text-zinc-100">
									{report.post.post_content}
								</p>
							</div>
						</div>

						<div class="w-full shrink-0 space-y-3 lg:w-64">
							<a
								href={`/forum/${report.post.topic_slug}`}
								class="block rounded-2xl border border-zinc-300 px-4 py-3 text-center text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
							>
								Voir le sujet
							</a>

							{#if report.status === 'open'}
								<form method="POST" action="?/resolveReport">
									<input type="hidden" name="_csrf" value={csrfToken} />
									<input type="hidden" name="report_id" value={report.id} />
									<button
										type="submit"
										class="w-full rounded-2xl bg-emerald-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-emerald-500"
									>
										Marquer résolu
									</button>
								</form>

								<form method="POST" action="?/dismissReport">
									<input type="hidden" name="_csrf" value={csrfToken} />
									<input type="hidden" name="report_id" value={report.id} />
									<button
										type="submit"
										class="w-full rounded-2xl border border-zinc-300 px-4 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
									>
										Ignorer
									</button>
								</form>

								{#if !report.post.is_deleted}
									<form method="POST" action="?/deletePost">
										<input type="hidden" name="_csrf" value={csrfToken} />
										<input type="hidden" name="report_id" value={report.id} />
										<input type="hidden" name="post_id" value={report.post.id} />
										<button
											type="submit"
											class="w-full rounded-2xl border border-red-300 px-4 py-3 text-sm font-medium text-red-700 transition hover:bg-red-50 dark:border-red-900/60 dark:text-red-300 dark:hover:bg-red-950/30"
										>
											Supprimer le message
										</button>
									</form>
								{/if}
							{/if}
						</div>
					</div>
				</section>
			{/each}
		{:else}
			<div class="rounded-3xl border border-dashed border-zinc-300 bg-zinc-50 p-6 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/50 dark:text-zinc-300">
				Aucun signalement trouvé.
			</div>
		{/if}
	</div>
</div>