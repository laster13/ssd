<script lang="ts">
	import JobStatusBadge from '$lib/components/apps/JobStatusBadge.svelte';
	import {
		appName,
		appSlug,
		formatFrenchDateTime,
		machinePillClass,
		machineStatusLabel
	} from '$lib/utils/jobs';
	import type { Job, Machine } from '$lib/utils/jobs';

	type InventoryView = 'all' | 'installed' | 'running' | 'failed' | 'servers';

	type InventoryItem = {
		key: string;
		jobId: string;
		appSlug: string;
		appTitle: string;
		status: string;
		createdAt?: string;
		updatedAt?: string;
		machineId: string;
		machineName: string;
		machineStatus?: string;
		action: 'install' | 'uninstall';
	};

	type ServerItem = {
		machineId: string;
		machineName: string;
		machineStatus?: string;
		appCount: number;
		runningCount: number;
		failedCount: number;
		lastActivity?: string;
	};

	let {
		jobs = [],
		machines = [],
		uninstallError = null,
		uninstallSuccess = null
	}: {
		jobs?: Job[];
		machines?: Machine[];
		uninstallError?: string | null;
		uninstallSuccess?: string | null;
	} = $props();

	let selectedView = $state<InventoryView>('all');

	const machineById = $derived(new Map(machines.map((machine) => [machine.id, machine])));

	const latestByApp = $derived.by(() => {
		const latestByKey = new Map<string, InventoryItem>();

		for (const job of jobs) {
			const slug = appSlug(job);

			if (!slug || slug === 'unknown') continue;
			if (job.type === 'install_ssdv2') continue;

			const key = `${job.machine_id}:${slug}`;
			const machine = machineById.get(job.machine_id);

			const candidate: InventoryItem = {
				key,
				jobId: job.id,
				appSlug: slug,
				appTitle: appName(job),
				status: job.status,
				createdAt: job.created_at,
				updatedAt: job.updated_at,
				machineId: job.machine_id,
				machineName: machine?.hostname || machine?.machine_uuid || 'Serveur inconnu',
				machineStatus: machine?.status || 'unknown',
				action: job.type === 'uninstall_app' ? 'uninstall' : 'install'
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

	const appItems = $derived.by(() =>
		latestByApp.filter((item) => !(item.action === 'uninstall' && item.status === 'completed'))
	);

	const installedItems = $derived.by(() =>
		appItems.filter((item) => item.action === 'install' && item.status === 'completed')
	);

	const runningItems = $derived.by(() =>
		appItems.filter((item) => ['pending', 'claimed', 'running'].includes(item.status))
	);

	const failedItems = $derived.by(() => appItems.filter((item) => item.status === 'failed'));

	const serverItems = $derived.by(() => {
		const grouped = new Map<string, ServerItem>();

		for (const item of appItems) {
			const existing = grouped.get(item.machineId);

			if (!existing) {
				grouped.set(item.machineId, {
					machineId: item.machineId,
					machineName: item.machineName,
					machineStatus: item.machineStatus,
					appCount: item.action === 'install' ? 1 : 0,
					runningCount: ['pending', 'claimed', 'running'].includes(item.status) ? 1 : 0,
					failedCount: item.status === 'failed' ? 1 : 0,
					lastActivity: item.updatedAt
				});
				continue;
			}

			existing.appCount += item.action === 'install' ? 1 : 0;
			existing.runningCount += ['pending', 'claimed', 'running'].includes(item.status) ? 1 : 0;
			existing.failedCount += item.status === 'failed' ? 1 : 0;

			const existingTime = existing.lastActivity ? new Date(existing.lastActivity).getTime() : 0;
			const candidateTime = item.updatedAt ? new Date(item.updatedAt).getTime() : 0;

			if (candidateTime >= existingTime) {
				existing.lastActivity = item.updatedAt;
				existing.machineStatus = item.machineStatus;
				existing.machineName = item.machineName;
			}
		}

		return Array.from(grouped.values()).sort((a, b) => {
			const aTime = a.lastActivity ? new Date(a.lastActivity).getTime() : 0;
			const bTime = b.lastActivity ? new Date(b.lastActivity).getTime() : 0;
			return bTime - aTime;
		});
	});

	const visibleItems = $derived.by(() => {
		switch (selectedView) {
			case 'installed':
				return installedItems;
			case 'running':
				return runningItems;
			case 'failed':
				return failedItems;
			default:
				return appItems;
		}
	});

	const installedCount = $derived(installedItems.length);
	const activeCount = $derived(runningItems.length);
	const incidentCount = $derived(failedItems.length);
	const serverCount = $derived(serverItems.length);

	function canUninstall(item: InventoryItem) {
		return item.action === 'install' && item.status === 'completed';
	}

	function subtitle(item: InventoryItem) {
		if (item.action === 'uninstall' && ['pending', 'claimed', 'running'].includes(item.status)) {
			return `Désinstallation en cours sur ${item.machineName}`;
		}

		if (item.action === 'uninstall' && item.status === 'failed') {
			return `Échec de désinstallation sur ${item.machineName}`;
		}

		return `Déployée sur ${item.machineName}`;
	}

	function sectionTitle() {
		switch (selectedView) {
			case 'installed':
				return 'Applications installées';
			case 'running':
				return 'Applications en cours';
			case 'failed':
				return 'Applications en incident';
			case 'servers':
				return 'Serveurs actifs';
			default:
				return 'Inventaire des applications';
		}
	}

	function sectionDescription() {
		switch (selectedView) {
			case 'installed':
				return 'Applications actuellement installées avec succès.';
			case 'running':
				return 'Toutes les opérations encore en attente, préparation ou déploiement.';
			case 'failed':
				return 'Applications ou opérations ayant rencontré une erreur.';
			case 'servers':
				return 'Vue regroupée par serveur.';
			default:
				return 'Vue consolidée par application et par serveur.';
		}
	}

	function activeStatClass(view: InventoryView) {
		if (selectedView !== view) return '';
		switch (view) {
			case 'running':
				return 'ring-2 ring-cyan-300 dark:ring-cyan-400/30';
			case 'failed':
				return 'ring-2 ring-rose-300 dark:ring-rose-400/30';
			case 'servers':
				return 'ring-2 ring-emerald-300 dark:ring-emerald-400/30';
			default:
				return 'ring-2 ring-zinc-300 dark:ring-white/20';
		}
	}
</script>

<section class="relative isolate mx-auto max-w-7xl px-4 pb-14 sm:px-6 lg:px-8">
	{#if uninstallSuccess}
		<div class="mb-4 rounded-[18px] border border-emerald-200 bg-emerald-50/90 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-500/10 dark:text-emerald-200">
			{uninstallSuccess}
		</div>
	{/if}

	{#if uninstallError}
		<div class="mb-4 rounded-[18px] border border-rose-200 bg-rose-50/90 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200">
			{uninstallError}
		</div>
	{/if}

	<div class="mb-5 flex flex-wrap gap-3">
		<button
			type="button"
			onclick={() => (selectedView = 'installed')}
			class={`inline-flex items-center gap-3 rounded-[18px] border border-black/5 bg-white/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_12px_28px_rgba(0,0,0,0.20)] ${activeStatClass('installed')}`}
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">Installées</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{installedCount}</span>
		</button>

		<button
			type="button"
			onclick={() => (selectedView = 'running')}
			class={`inline-flex items-center gap-3 rounded-[18px] border border-cyan-200/70 bg-cyan-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(14,165,233,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-cyan-400/15 dark:bg-cyan-500/[0.08] ${activeStatClass('running')}`}
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-700 dark:text-cyan-200">En cours</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{activeCount}</span>
		</button>

		<button
			type="button"
			onclick={() => (selectedView = 'failed')}
			class={`inline-flex items-center gap-3 rounded-[18px] border border-rose-200/70 bg-rose-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(244,63,94,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-rose-400/15 dark:bg-rose-500/[0.08] ${activeStatClass('failed')}`}
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-rose-700 dark:text-rose-200">Incidents</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{incidentCount}</span>
		</button>

		<button
			type="button"
			onclick={() => (selectedView = 'servers')}
			class={`inline-flex items-center gap-3 rounded-[18px] border border-emerald-200/70 bg-emerald-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(16,185,129,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-emerald-400/15 dark:bg-emerald-500/[0.08] ${activeStatClass('servers')}`}
		>
			<span class="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700 dark:text-emerald-200">Serveurs</span>
			<span class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{serverCount}</span>
		</button>
	</div>

	<div class="mb-5">
		<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.18em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
			<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
			Inventaire
		</div>

		<h2 class="text-xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
			{sectionTitle()}
		</h2>

		<p class="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
			{sectionDescription()}
		</p>
	</div>

	<div class="mb-5 flex flex-wrap gap-2">
		<button
			type="button"
			onclick={() => (selectedView = 'all')}
			class="inline-flex items-center justify-center rounded-[14px] border border-black/5 bg-white/80 px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-600 transition hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300 dark:hover:border-white/14 dark:hover:bg-white/[0.06]"
		>
			Tout afficher
		</button>
	</div>

	<div class="mb-5 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
		<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
		Filtre actif :
		{selectedView === 'installed'
			? 'Installées'
			: selectedView === 'running'
				? 'En cours'
				: selectedView === 'failed'
					? 'Incidents'
					: selectedView === 'servers'
						? 'Serveurs'
						: 'Toutes'}
	</div>

	{#if selectedView === 'servers'}
		{#if serverItems.length > 0}
			<div class="grid gap-3">
				{#each serverItems as server}
					<article class="relative overflow-hidden rounded-[20px] border border-black/5 bg-white/78 p-4 shadow-[0_14px_34px_rgba(15,23,42,0.07)] backdrop-blur-2xl transition duration-200 hover:-translate-y-0.5 hover:shadow-[0_20px_42px_rgba(15,23,42,0.11)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_14px_30px_rgba(0,0,0,0.22)]">
						<div class="relative flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
							<div class="min-w-0 flex-1">
								<div class="flex flex-wrap items-center gap-3">
									<h3 class="truncate text-base font-semibold tracking-[-0.03em] text-zinc-950 dark:text-zinc-50">
										{server.machineName}
									</h3>

									<span class={`rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.12em] ${machinePillClass(server.machineStatus)}`}>
										{machineStatusLabel(server.machineStatus)}
									</span>
								</div>

								<div class="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-sm text-zinc-500 dark:text-zinc-400">
									<span><span class="font-medium text-zinc-700 dark:text-zinc-300">Apps :</span> {server.appCount}</span>
									<span><span class="font-medium text-zinc-700 dark:text-zinc-300">En cours :</span> {server.runningCount}</span>
									<span><span class="font-medium text-zinc-700 dark:text-zinc-300">Incidents :</span> {server.failedCount}</span>
									<span><span class="font-medium text-zinc-700 dark:text-zinc-300">Dernière activité :</span> {formatFrenchDateTime(server.lastActivity)}</span>
								</div>
							</div>
						</div>
					</article>
				{/each}
			</div>
		{:else}
			<div class="relative overflow-hidden rounded-[24px] border border-black/5 bg-white/80 p-7 shadow-[0_20px_60px_rgba(15,23,42,0.10)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_20px_60px_rgba(0,0,0,0.30)]">
				<div class="relative mx-auto max-w-xl text-center">
					<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-[18px] border border-black/5 bg-white text-2xl shadow-[0_12px_26px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_12px_24px_rgba(0,0,0,0.24)]">
						✦
					</div>

					<h2 class="mt-4 text-xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
						Aucun serveur trouvé
					</h2>

					<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
						Aucune activité serveur n’est encore disponible.
					</p>
				</div>
			</div>
		{/if}
	{:else if visibleItems.length > 0}
		<div class="grid gap-3">
			{#each visibleItems as item}
				<article class="relative overflow-hidden rounded-[20px] border border-black/5 bg-white/78 p-4 shadow-[0_14px_34px_rgba(15,23,42,0.07)] backdrop-blur-2xl transition duration-200 hover:-translate-y-0.5 hover:shadow-[0_20px_42px_rgba(15,23,42,0.11)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_14px_30px_rgba(0,0,0,0.22)]">
					<div class="relative flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-3">
								<h3 class="truncate text-base font-semibold tracking-[-0.03em] text-zinc-950 dark:text-zinc-50">
									{item.appTitle}
								</h3>

								<JobStatusBadge status={item.status} variant="applications" className="shrink-0" />
							</div>

							<div class="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-sm text-zinc-500 dark:text-zinc-400">
								<span>
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Application :</span>
									{item.appSlug}
								</span>

								<span>
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Serveur :</span>
									{item.machineName}
								</span>

								<span>
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Créée :</span>
									{formatFrenchDateTime(item.createdAt)}
								</span>

								<span>
									<span class="font-medium text-zinc-700 dark:text-zinc-300">Maj :</span>
									{formatFrenchDateTime(item.updatedAt)}
								</span>

								<span class={`inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.12em] ${machinePillClass(item.machineStatus)}`}>
									{machineStatusLabel(item.machineStatus)}
								</span>
							</div>

							<p class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
								{subtitle(item)}
							</p>
						</div>

						<div class="flex flex-wrap gap-2 md:justify-end">
							<a
								href={`/installations/${item.jobId}`}
								class="inline-flex min-w-[84px] items-center justify-center rounded-[14px] border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm font-semibold text-cyan-700 transition hover:border-cyan-300 hover:bg-cyan-100 dark:border-cyan-400/20 dark:bg-cyan-500/10 dark:text-cyan-200 dark:hover:border-cyan-400/30 dark:hover:bg-cyan-500/15"
							>
								Log
							</a>

							<a
								href={`/installations/new?app=${encodeURIComponent(item.appSlug)}`}
								class="inline-flex items-center justify-center rounded-[14px] border border-black/5 bg-white/80 px-3 py-2 text-sm font-medium text-zinc-700 transition hover:border-black/10 hover:bg-white hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.06] dark:hover:text-zinc-50"
							>
								Réinstaller
							</a>

							{#if canUninstall(item)}
								<form method="POST" action="?/uninstallApplication" class="contents">
									<input type="hidden" name="machine_id" value={item.machineId} />
									<input type="hidden" name="app_slug" value={item.appSlug} />

									<button
										type="submit"
										class="inline-flex items-center justify-center rounded-[14px] border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700 transition hover:border-rose-300 hover:bg-rose-100 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/30 dark:hover:bg-rose-500/15"
										onclick={(event) => {
											if (!confirm(`Désinstaller ${item.appTitle} de ${item.machineName} ?`)) {
												event.preventDefault();
											}
										}}
									>
										Désinstaller
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
					✦
				</div>

				<h2 class="mt-4 text-xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
					Aucun contenu pour ce filtre
				</h2>

				<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
					Essaie une autre carte ou clique sur “Tout afficher”.
				</p>
			</div>
		</div>
	{/if}
</section>