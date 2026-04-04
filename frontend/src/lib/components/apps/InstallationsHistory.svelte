<script lang="ts">
	import JobStatusBadge from '$lib/components/apps/JobStatusBadge.svelte';
	import {
		appName,
		formatFrenchDate,
		historyFilterLabel,
		matchesHistoryFilter
	} from '$lib/utils/jobs';
	import type { HistoryFilter, Job } from '$lib/utils/jobs';

	let {
		jobs = [],
		filter = 'all',
		deleteError = null,
		deleteSuccess = null
	}: {
		jobs?: Job[];
		filter?: HistoryFilter;
		deleteError?: string | null;
		deleteSuccess?: string | null;
	} = $props();

	function canDeleteJob(job: Job) {
		return job.status === 'completed' || job.status === 'failed';
	}

	const sortedJobs = $derived.by(() => {
		return [...jobs].sort((a, b) => {
			const aTime = a.created_at ? new Date(a.created_at).getTime() : 0;
			const bTime = b.created_at ? new Date(b.created_at).getTime() : 0;
			return bTime - aTime;
		});
	});

	const filteredJobs = $derived.by(() => {
		return sortedJobs.filter((job) => matchesHistoryFilter(job, filter));
	});

	const stats = $derived.by(() => ({
		all: jobs.length,
		running: jobs.filter((job) => ['pending', 'claimed', 'running'].includes(job.status)).length,
		completed: jobs.filter((job) => job.status === 'completed').length,
		failed: jobs.filter((job) => job.status === 'failed').length
	}));
</script>

<section class="relative isolate mx-auto max-w-7xl px-4 pb-14 sm:px-6 lg:px-8">
	{#if deleteSuccess}
		<div class="mb-4 rounded-[18px] border border-emerald-200 bg-emerald-50/90 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-500/10 dark:text-emerald-200">
			{deleteSuccess}
		</div>
	{/if}

	{#if deleteError}
		<div class="mb-4 rounded-[18px] border border-rose-200 bg-rose-50/90 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200">
			{deleteError}
		</div>
	{/if}

	<div class="mb-5 flex flex-wrap gap-3">
		<a
			href="/applications?tab=history&filter=all"
			class="inline-flex items-center gap-3 rounded-[18px] border border-black/5 bg-white/80 px-4 py-3 text-sm shadow-[0_12px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_12px_28px_rgba(0,0,0,0.20)]"
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">Total</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{stats.all}</span>
		</a>

		<a
			href="/applications?tab=history&filter=running"
			class="inline-flex items-center gap-3 rounded-[18px] border border-cyan-200/70 bg-cyan-50/80 px-4 py-3 text-sm shadow-[0_12px_30px_rgba(14,165,233,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-cyan-400/15 dark:bg-cyan-500/[0.08]"
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700 dark:text-cyan-200">En cours</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{stats.running}</span>
		</a>

		<a
			href="/applications?tab=history&filter=completed"
			class="inline-flex items-center gap-3 rounded-[18px] border border-emerald-200/70 bg-emerald-50/80 px-4 py-3 text-sm shadow-[0_12px_30px_rgba(16,185,129,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-emerald-400/15 dark:bg-emerald-500/[0.08]"
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700 dark:text-emerald-200">En ligne</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{stats.completed}</span>
		</a>

		<a
			href="/applications?tab=history&filter=failed"
			class="inline-flex items-center gap-3 rounded-[18px] border border-rose-200/70 bg-rose-50/80 px-4 py-3 text-sm shadow-[0_12px_30px_rgba(244,63,94,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-rose-400/15 dark:bg-rose-500/[0.08]"
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-rose-700 dark:text-rose-200">Incidents</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{stats.failed}</span>
		</a>
	</div>

	<div class="mb-5">
		<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.18em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
			<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
			Historique
		</div>

		<h2 class="text-xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
			Historique des installations
		</h2>

		<p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
			Vue compacte des installations récentes, avec accès rapide aux logs et suppression des jobs terminés.
		</p>
	</div>


	<div class="mb-5 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
		<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
		Filtre actif : {historyFilterLabel(filter)}
	</div>

	{#if filteredJobs.length > 0}
		<div class="grid gap-3">
			{#each filteredJobs as job}
				<article class="relative overflow-hidden rounded-[20px] border border-black/5 bg-white/78 p-4 shadow-[0_14px_34px_rgba(15,23,42,0.07)] backdrop-blur-2xl transition duration-200 hover:-translate-y-0.5 hover:shadow-[0_20px_42px_rgba(15,23,42,0.11)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_14px_30px_rgba(0,0,0,0.22)]">
					<div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.07),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(124,58,237,0.06),transparent_28%)] dark:bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.07),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(124,58,237,0.06),transparent_28%)]"></div>

					<div class="relative flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-3">
								<h3 class="truncate text-base font-semibold tracking-[-0.03em] text-zinc-950 dark:text-zinc-50">
									{appName(job)}
								</h3>

								<JobStatusBadge status={job.status} variant="history" className="shrink-0" />
							</div>

							<div class="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-sm text-zinc-500 dark:text-zinc-400">
								<span>
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Créée :</span>
									{formatFrenchDate(job.created_at)}
								</span>

								{#if job.type}
									<span>
										<span class="font-medium text-zinc-700 dark:text-zinc-300">Type :</span>
										{job.type}
									</span>
								{/if}

								<span class="truncate">
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Job :</span>
									{job.id}
								</span>
							</div>
						</div>

						<div class="flex flex-wrap gap-2 md:justify-end">
							<a
								href={`/installations/${job.id}`}
								class="inline-flex min-w-[84px] items-center justify-center rounded-[14px] border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm font-semibold text-cyan-700 transition hover:border-cyan-300 hover:bg-cyan-100 dark:border-cyan-400/20 dark:bg-cyan-500/10 dark:text-cyan-200 dark:hover:border-cyan-400/30 dark:hover:bg-cyan-500/15"
							>
								Log
							</a>

							{#if canDeleteJob(job)}
								<form method="POST" action="?/deleteInstallation" class="contents">
									<input type="hidden" name="job_id" value={job.id} />
									<button
										type="submit"
										class="inline-flex items-center justify-center rounded-[14px] border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700 transition hover:border-rose-300 hover:bg-rose-100 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/30 dark:hover:bg-rose-500/15"
										onclick={(event) => {
											if (!confirm('Supprimer définitivement ce job de l’historique ?')) {
												event.preventDefault();
											}
										}}
									>
										Supprimer
									</button>
								</form>
							{/if}
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="relative overflow-hidden rounded-[24px] border border-black/5 bg-white/80 p-7 shadow-[0_20px_60px_rgba(15,23,42,0.10)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_20px_60px_rgba(0,0,0,0.30)]">
			<div class="relative mx-auto max-w-xl text-center">
				<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-[18px] border border-black/5 bg-white text-2xl shadow-[0_12px_26px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_12px_24px_rgba(0,0,0,0.24)]">
					⌁
				</div>

				<h2 class="mt-4 text-xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
					Aucune installation trouvée
				</h2>

				<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
					Aucun job ne correspond actuellement au filtre <strong>{historyFilterLabel(filter)}</strong>.
				</p>
			</div>
		</div>
	{/if}
</section>