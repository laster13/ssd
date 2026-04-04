<script lang="ts">
	let { data } = $props();

	function humanStatus(status: unknown) {
		switch (String(status ?? '').toLowerCase()) {
			case 'pending':
				return 'En attente';
			case 'claimed':
				return 'Préparation';
			case 'running':
				return 'Installation en cours';
			case 'completed':
				return 'Terminée';
			case 'failed':
				return 'Échec';
			default:
				return String(status ?? 'Inconnu');
		}
	}

	function statusClasses(status: unknown) {
		switch (String(status ?? '').toLowerCase()) {
			case 'completed':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
			case 'failed':
				return 'border-red-200 bg-red-50 text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300';
			case 'running':
			case 'claimed':
				return 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300';
			default:
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
		}
	}

	function formatDate(value: unknown) {
		if (!value) return '-';

		const date = new Date(String(value));
		if (Number.isNaN(date.getTime())) return String(value);

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'short',
			timeStyle: 'short'
		}).format(date);
	}
</script>

<svelte:head>
	<title>Installations SSDv2</title>
</svelte:head>

<section class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/servers"
						class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						← Retour aux serveurs
					</a>
				</p>

				<div class="mb-6 rounded-[22px] border border-black/5 bg-white/70 p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
					<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Installations SSDv2
					</h1>

					<p class="mt-2 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Suis ici les installations SSDv2 lancées sur tes serveurs, avec leur statut et l’accès au suivi détaillé.
					</p>
				</div>

				{#if data.jobs.length > 0}
					<div class="grid gap-4">
						{#each data.jobs as job}
							<a
								href={`/ssdv2-installations/${job.id}`}
								class="block rounded-[24px] border border-black/5 bg-white/60 p-5 shadow-[0_12px_30px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_38px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[0_12px_30px_rgba(0,0,0,0.20)]"
							>
								<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
									<div class="min-w-0">
										<h2 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
											{job.machine?.hostname ?? 'Serveur SSDv2'}
										</h2>

										<p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
											Domaine : {job.payload?.domain ?? '-'}
										</p>

										<div class="mt-3 grid gap-2 text-sm text-zinc-700 dark:text-zinc-300 sm:grid-cols-2">
											<div>
												<span class="text-zinc-500 dark:text-zinc-400">Job ID :</span>
												<span class="ml-1 font-medium text-zinc-900 dark:text-zinc-100">{job.id}</span>
											</div>

											<div>
												<span class="text-zinc-500 dark:text-zinc-400">Créée le :</span>
												<span class="ml-1 font-medium text-zinc-900 dark:text-zinc-100">{formatDate(job.created_at)}</span>
											</div>
										</div>
									</div>

									<div class={`inline-flex w-fit items-center rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.12em] ${statusClasses(job.status)}`}>
										{humanStatus(job.status)}
									</div>
								</div>
							</a>
						{/each}
					</div>
				{:else}
					<div class="rounded-[24px] border border-black/5 bg-white/60 p-6 text-sm text-zinc-600 shadow-[0_10px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-[0_10px_30px_rgba(0,0,0,0.2)]">
						Aucune installation SSDv2 pour le moment.
					</div>
				{/if}
			</div>
		</div>
	</div>
</section>
