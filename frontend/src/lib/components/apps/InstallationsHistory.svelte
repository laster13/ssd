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
</script>

<section class="relative isolate mx-auto max-w-7xl px-4 pb-14 sm:px-6 lg:px-8">
	<div class="relative overflow-hidden rounded-[34px] border border-black/5 bg-white/78 shadow-[0_28px_90px_rgba(15,23,42,0.10)] backdrop-blur-3xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_90px_rgba(0,0,0,0.36)]">
		<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.88),rgba(255,255,255,0.62)_44%,rgba(255,255,255,0.50)_100%)] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.03)_44%,rgba(255,255,255,0.02)_100%)]"></div>
		<div class="pointer-events-none absolute -left-16 top-0 h-72 w-72 rounded-full bg-cyan-300/20 blur-3xl dark:bg-cyan-400/12"></div>
		<div class="pointer-events-none absolute right-[-4rem] top-[-2rem] h-80 w-80 rounded-full bg-violet-300/16 blur-3xl dark:bg-violet-400/12"></div>

		<div class="relative p-6 sm:p-8">
			<div class="mb-7 flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
				<div>
					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						Historique premium
					</div>

                                        <h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
	                                        <span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
		                                Historique des Installations
	                                        </span>
                                        </h1>

					<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Suis l’avancement des installations lancées depuis l’App Store.
					</p>
				</div>

				<div class="w-full max-w-2xl">
					<div class="grid grid-cols-2 gap-2 rounded-[24px] border border-black/5 bg-black/[0.03] p-2 shadow-[inset_0_1px_0_rgba(255,255,255,0.75)] sm:grid-cols-4 dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
						<a
							href="/applications?tab=history&filter=all"
							class={`inline-flex items-center justify-center rounded-[16px] px-3 py-2.5 text-xs font-semibold uppercase tracking-[0.14em] transition ${
								filter === 'all'
									? 'border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.96),rgba(37,99,235,0.96),rgba(124,58,237,0.92))] text-white shadow-[0_12px_28px_rgba(37,99,235,0.20)]'
									: 'border border-transparent bg-white/75 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.055]'
							}`}
						>
							Toutes
						</a>

						<a
							href="/applications?tab=history&filter=running"
							class={`inline-flex items-center justify-center rounded-[16px] px-3 py-2.5 text-xs font-semibold uppercase tracking-[0.14em] transition ${
								filter === 'running'
									? 'border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.96),rgba(37,99,235,0.96),rgba(124,58,237,0.92))] text-white shadow-[0_12px_28px_rgba(37,99,235,0.20)]'
									: 'border border-transparent bg-white/75 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.055]'
							}`}
						>
							En cours
						</a>

						<a
							href="/applications?tab=history&filter=completed"
							class={`inline-flex items-center justify-center rounded-[16px] px-3 py-2.5 text-xs font-semibold uppercase tracking-[0.14em] transition ${
								filter === 'completed'
									? 'border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.96),rgba(37,99,235,0.96),rgba(124,58,237,0.92))] text-white shadow-[0_12px_28px_rgba(37,99,235,0.20)]'
									: 'border border-transparent bg-white/75 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.055]'
							}`}
						>
							En ligne
						</a>

						<a
							href="/applications?tab=history&filter=failed"
							class={`inline-flex items-center justify-center rounded-[16px] px-3 py-2.5 text-xs font-semibold uppercase tracking-[0.14em] transition ${
								filter === 'failed'
									? 'border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.96),rgba(37,99,235,0.96),rgba(124,58,237,0.92))] text-white shadow-[0_12px_28px_rgba(37,99,235,0.20)]'
									: 'border border-transparent bg-white/75 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.055]'
							}`}
						>
							Incidents
						</a>
					</div>
				</div>
			</div>

			<div class="mb-6 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
				<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
				Filtre actif : {historyFilterLabel(filter)}
			</div>

			{#if deleteSuccess}
				<div class="mb-4 rounded-[20px] border border-emerald-200 bg-emerald-50/90 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-500/10 dark:text-emerald-200">
					{deleteSuccess}
				</div>
			{/if}

			{#if deleteError}
				<div class="mb-4 rounded-[20px] border border-rose-200 bg-rose-50/90 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200">
					{deleteError}
				</div>
			{/if}

			{#if filteredJobs.length > 0}
				<div class="grid gap-4">
					{#each filteredJobs as job}
						<div
							class="group relative flex items-center justify-between gap-4 overflow-hidden rounded-[24px] border border-black/5 bg-white/72 px-5 py-4 text-zinc-900 shadow-[0_16px_40px_rgba(15,23,42,0.07)] backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-black/10 hover:shadow-[0_22px_48px_rgba(15,23,42,0.11)] dark:border-white/10 dark:bg-white/[0.035] dark:text-white dark:shadow-[0_14px_34px_rgba(0,0,0,0.22)] dark:hover:border-white/14 dark:hover:bg-white/[0.05]"
						>
							<div class="pointer-events-none absolute inset-0 opacity-0 transition duration-300 group-hover:opacity-100 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.08),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(124,58,237,0.08),transparent_28%)] dark:bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.08),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(124,58,237,0.08),transparent_28%)]"></div>

							<a href={`/installations/${job.id}`} class="relative flex min-w-0 flex-1 items-center justify-between gap-4">
								<div class="min-w-0">
									<div class="truncate text-[15px] font-semibold tracking-[-0.02em] text-zinc-950 dark:text-white sm:text-base">
										{appName(job)}
									</div>

									<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
										{formatFrenchDate(job.created_at)}
									</div>
								</div>

								<div class="relative shrink-0">
									<JobStatusBadge status={job.status} variant="history" className="shrink-0" />
								</div>
							</a>

							{#if canDeleteJob(job)}
								<form method="POST" action="?/deleteInstallation" class="relative shrink-0">
									<input type="hidden" name="job_id" value={job.id} />
									<button
										type="submit"
										class="inline-flex items-center justify-center rounded-[14px] border border-rose-200 bg-rose-50 px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] text-rose-700 transition hover:border-rose-300 hover:bg-rose-100 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/30 dark:hover:bg-rose-500/15"
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
					{/each}
				</div>
			{:else}
				<div class="rounded-[26px] border border-black/5 bg-white/65 p-6 text-sm text-zinc-600 shadow-[0_16px_40px_rgba(15,23,42,0.06)] backdrop-blur-xl dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-[0_14px_34px_rgba(0,0,0,0.22)]">
					Aucune installation ne correspond au filtre <strong>{historyFilterLabel(filter)}</strong>.
				</div>
			{/if}
		</div>
	</div>
</section>