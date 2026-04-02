<script lang="ts">
	import JobStatusBadge from '$lib/components/apps/JobStatusBadge.svelte';
	import {
		appName,
		appSlug,
		formatFrenchDateTime,
		jobStatusDotClass,
		machinePillClass,
		machineStatusLabel
	} from '$lib/utils/jobs';
	import type { Job, Machine } from '$lib/utils/jobs';

	let {
		jobs = [],
		machines = []
	}: {
		jobs?: Job[];
		machines?: Machine[];
	} = $props();

	const machineById = $derived(new Map(machines.map((machine) => [machine.id, machine])));

	const appItems = $derived.by(() => {
		const latestByKey = new Map<
			string,
			{
				key: string;
				jobId: string;
				appSlug: string;
				appTitle: string;
				status: string;
				createdAt?: string;
				updatedAt?: string;
				machineName: string;
				machineStatus: string;
			}
		>();

		for (const job of jobs) {
			const slug = appSlug(job);
			const key = `${job.machine_id}:${slug}`;
			const machine = machineById.get(job.machine_id);

			const candidate = {
				key,
				jobId: job.id,
				appSlug: slug,
				appTitle: appName(job),
				status: job.status,
				createdAt: job.created_at,
				updatedAt: job.updated_at,
				machineName: machine?.hostname || machine?.machine_uuid || 'Serveur inconnu',
				machineStatus: machine?.status || 'unknown'
			};

			const existing = latestByKey.get(key);

			if (!existing) {
				latestByKey.set(key, candidate);
				continue;
			}

			const existingTime = existing.updatedAt ? new Date(existing.updatedAt).getTime() : 0;
			const candidateTime = candidate.updatedAt ? new Date(candidate.updatedAt).getTime() : 0;

			if (candidateTime >= existingTime) {
				latestByKey.set(key, candidate);
			}
		}

		return Array.from(latestByKey.values()).sort((a, b) => {
			const aTime = a.updatedAt ? new Date(a.updatedAt).getTime() : 0;
			const bTime = b.updatedAt ? new Date(b.updatedAt).getTime() : 0;
			return bTime - aTime;
		});
	});

	const historyStats = $derived.by(() => ({
		total: jobs.length,
		running: jobs.filter((job) => ['pending', 'claimed', 'running'].includes(job.status)).length,
		failed: jobs.filter((job) => job.status === 'failed').length,
		completed: jobs.filter((job) => job.status === 'completed').length
	}));
</script>

<section class="relative isolate mx-auto max-w-7xl px-4 pb-14 sm:px-6 lg:px-8">
	<div class="pointer-events-none absolute inset-x-0 top-0 -z-10 h-40 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.85),transparent_68%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.05),transparent_68%)]"></div>

	<div class="mb-10 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
		<a
			href="/applications?tab=history&filter=all"
			class="group relative overflow-hidden rounded-[28px] border border-black/5 bg-white/78 p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:border-black/10 hover:shadow-[0_28px_70px_rgba(15,23,42,0.12)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_20px_60px_rgba(0,0,0,0.30)] dark:hover:border-white/14 dark:hover:bg-white/[0.055]"
		>
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.84),rgba(255,255,255,0.56))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"></div>
			<div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-zinc-300/20 blur-2xl dark:bg-white/10"></div>
			<div class="relative">
				<div class="flex items-center justify-between gap-3">
					<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-zinc-500 dark:text-zinc-400">
						Total
					</div>
					<div class="rounded-full border border-black/5 bg-white/70 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
						Historique
					</div>
				</div>
				<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">
					{historyStats.total}
				</div>
				<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Jobs d’installation</div>
			</div>
		</a>

		<a
			href="/applications?tab=history&filter=running"
			class="group relative overflow-hidden rounded-[28px] border border-cyan-200/70 bg-cyan-50/85 p-5 shadow-[0_20px_60px_rgba(14,165,233,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(14,165,233,0.16)] dark:border-cyan-400/15 dark:bg-cyan-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)]"
		>
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.72),rgba(255,255,255,0.32))] dark:bg-[linear-gradient(180deg,rgba(56,189,248,0.07),rgba(56,189,248,0.02))]"></div>
			<div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-cyan-300/35 blur-2xl dark:bg-cyan-400/20"></div>
			<div class="relative">
				<div class="flex items-center justify-between gap-3">
					<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-cyan-700 dark:text-cyan-200/90">
						En cours
					</div>
					<div class="h-2.5 w-2.5 rounded-full bg-cyan-500 shadow-[0_0_16px_rgba(6,182,212,0.45)] dark:bg-cyan-400"></div>
				</div>
				<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">
					{historyStats.running}
				</div>
				<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
					Jobs en attente ou déploiement
				</div>
			</div>
		</a>

		<a
			href="/applications?tab=history&filter=completed"
			class="group relative overflow-hidden rounded-[28px] border border-emerald-200/70 bg-emerald-50/85 p-5 shadow-[0_20px_60px_rgba(16,185,129,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(16,185,129,0.16)] dark:border-emerald-400/15 dark:bg-emerald-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)]"
		>
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.72),rgba(255,255,255,0.32))] dark:bg-[linear-gradient(180deg,rgba(16,185,129,0.07),rgba(16,185,129,0.02))]"></div>
			<div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-emerald-300/35 blur-2xl dark:bg-emerald-400/18"></div>
			<div class="relative">
				<div class="flex items-center justify-between gap-3">
					<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-emerald-700 dark:text-emerald-200/90">
						En ligne
					</div>
					<div class="h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_16px_rgba(16,185,129,0.45)] dark:bg-emerald-400"></div>
				</div>
				<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">
					{historyStats.completed}
				</div>
				<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Jobs terminés avec succès</div>
			</div>
		</a>

		<a
			href="/applications?tab=history&filter=failed"
			class="group relative overflow-hidden rounded-[28px] border border-rose-200/70 bg-rose-50/85 p-5 shadow-[0_20px_60px_rgba(244,63,94,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(244,63,94,0.16)] dark:border-rose-400/15 dark:bg-rose-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)]"
		>
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.72),rgba(255,255,255,0.32))] dark:bg-[linear-gradient(180deg,rgba(244,63,94,0.07),rgba(244,63,94,0.02))]"></div>
			<div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-rose-300/35 blur-2xl dark:bg-rose-400/18"></div>
			<div class="relative">
				<div class="flex items-center justify-between gap-3">
					<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-rose-700 dark:text-rose-200/90">
						Incidents
					</div>
					<div class="h-2.5 w-2.5 rounded-full bg-rose-500 shadow-[0_0_16px_rgba(244,63,94,0.45)] dark:bg-rose-400"></div>
				</div>
				<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">
					{historyStats.failed}
				</div>
				<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Jobs en échec</div>
			</div>
		</a>
	</div>

	{#if appItems.length > 0}
		<div class="mb-6 flex items-center justify-between gap-4">
			<div>
				<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/70 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
					<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
					Inventaire premium
				</div>
				<h2 class="text-2xl font-semibold tracking-[-0.06em] text-zinc-950 dark:text-zinc-50 sm:text-3xl">
					Inventaire des applications
				</h2>
				<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
					Vue consolidée par application et par serveur.
				</p>
			</div>

			<div class="hidden rounded-full border border-black/5 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.2em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400 md:block">
				Triées par activité récente
			</div>
		</div>

		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 2xl:grid-cols-3">
			{#each appItems as item}
				<article
					class="group relative overflow-hidden rounded-[32px] border border-black/5 bg-white/82 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.09)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1.5 hover:border-black/10 hover:shadow-[0_32px_85px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_24px_70px_rgba(0,0,0,0.34)] dark:hover:border-white/14 dark:hover:bg-white/[0.055]"
				>
					<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.86),rgba(255,255,255,0.58)_42%,rgba(255,255,255,0.46))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.025)_42%,rgba(255,255,255,0.015))]"></div>
					<div class="pointer-events-none absolute inset-0 opacity-0 transition duration-300 group-hover:opacity-100 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.10),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(16,185,129,0.10),transparent_32%)] dark:bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.10),transparent_26%),radial-gradient(circle_at_bottom_left,rgba(16,185,129,0.08),transparent_30%)]"></div>
					<div class="pointer-events-none absolute -right-10 -top-10 h-24 w-24 rounded-full bg-cyan-300/25 blur-2xl dark:bg-cyan-400/12"></div>

					<div class="relative">
						<div class="mb-5 flex items-start justify-between gap-4">
							<div class="min-w-0">
								<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/75 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
									<span class={`h-2 w-2 rounded-full ${jobStatusDotClass(item.status)}`}></span>
									Statut
								</div>

								<h3 class="truncate text-[1.28rem] font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50 sm:text-[1.42rem]">
									{item.appTitle}
								</h3>

								<p class="mt-1 truncate text-sm text-zinc-500 dark:text-zinc-400">
									Déployée sur {item.machineName}
								</p>
							</div>

							<JobStatusBadge status={item.status} variant="applications" className="shrink-0" />
						</div>

						<div class="rounded-[24px] border border-black/5 bg-white/72 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
							<div class="mb-4 flex items-center justify-between gap-3">
								<span class="text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 dark:text-zinc-400">
									Détails
								</span>

								<span
									class={`rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] ${machinePillClass(item.machineStatus)}`}
								>
									{machineStatusLabel(item.machineStatus)}
								</span>
							</div>

							<dl class="space-y-3">
								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Application</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{item.appSlug}
									</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Serveur</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{item.machineName}
									</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Créée le</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{formatFrenchDateTime(item.createdAt)}
									</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Dernière mise à jour</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{formatFrenchDateTime(item.updatedAt)}
									</dd>
								</div>
							</dl>
						</div>

						<div class="mt-5 flex items-center gap-3">
							<a
								href={`/installations/${item.jobId}`}
								class="relative inline-flex flex-1 items-center justify-center gap-2 overflow-hidden rounded-[20px] border border-cyan-200 px-4 py-3 text-sm font-semibold text-white shadow-[0_16px_36px_rgba(37,99,235,0.24)] transition duration-200 hover:scale-[1.01] hover:shadow-[0_20px_40px_rgba(37,99,235,0.30)] dark:border-cyan-400/15 dark:shadow-[0_16px_34px_rgba(0,0,0,0.30)]"
							>
								<span class="absolute inset-0 bg-[linear-gradient(135deg,rgba(14,165,233,0.98),rgba(37,99,235,0.96),rgba(124,58,237,0.92))]"></span>
								<span class="absolute inset-0 opacity-80 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.24),transparent_55%)]"></span>
								<span class="relative">Voir les logs</span>
							</a>

							<a
								href={`/installations/new?app=${encodeURIComponent(item.appSlug)}`}
								class="inline-flex items-center justify-center rounded-[20px] border border-black/5 bg-white/80 px-4 py-3 text-sm font-medium text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] transition hover:border-black/10 hover:bg-white hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.06] dark:hover:text-zinc-50"
							>
								Réinstaller
							</a>
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="relative overflow-hidden rounded-[32px] border border-black/5 bg-white/80 p-8 shadow-[0_24px_70px_rgba(15,23,42,0.10)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_24px_70px_rgba(0,0,0,0.32)]">
			<div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(14,165,233,0.10),transparent_34%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.10),transparent_30%)] dark:bg-[radial-gradient(circle_at_top,rgba(56,189,248,0.08),transparent_34%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.08),transparent_30%)]"></div>
			<div class="relative mx-auto max-w-xl text-center">
				<div class="mx-auto flex h-16 w-16 items-center justify-center rounded-[24px] border border-black/5 bg-white text-2xl shadow-[0_14px_34px_rgba(15,23,42,0.10),inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_14px_30px_rgba(0,0,0,0.24)]">
					✦
				</div>

				<h2 class="mt-5 text-2xl font-semibold tracking-[-0.06em] text-zinc-950 dark:text-zinc-50">
					Aucune application lancée
				</h2>

				<p class="mt-3 text-base leading-7 text-zinc-600 dark:text-zinc-400">
					Ton espace est prêt pour accueillir un premier déploiement.
				</p>

				<a
					href="/app-store"
					class="relative mt-6 inline-flex items-center justify-center overflow-hidden rounded-[20px] border border-cyan-200 px-5 py-3 text-sm font-semibold text-white shadow-[0_18px_40px_rgba(37,99,235,0.22)] transition hover:scale-[1.01] dark:border-cyan-400/15"
				>
					<span class="absolute inset-0 bg-[linear-gradient(135deg,rgba(14,165,233,0.98),rgba(59,130,246,0.96),rgba(124,58,237,0.92))]"></span>
					<span class="absolute inset-0 opacity-80 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.24),transparent_55%)]"></span>
					<span class="relative">Ouvrir l’App Store</span>
				</a>
			</div>
		</div>
	{/if}
</section>