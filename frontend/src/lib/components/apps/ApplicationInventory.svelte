<script lang="ts">
	import JobStatusBadge from '$lib/components/apps/JobStatusBadge.svelte';
	import type { ApplicationState, Machine, MachineConnectionStatus } from '$lib/utils/jobs';
	import {
		formatFrenchDateTime,
		machinePillClass,
		machineStatusLabel,
		resolveMachineConnectionStatus
	} from '$lib/utils/jobs';

	type InventoryView = 'all' | 'installed' | 'running' | 'failed' | 'servers';
	type ApplicationDisplayStatus = 'completed' | 'running' | 'failed';

	type InventoryItem = {
		id: string;
		machineId: string;
		machineName: string;
		machineStatus: MachineConnectionStatus;
		appTitle: string;
		appSlug: string;
		present: boolean;
		transition: ApplicationState['transition'];
		lastError?: string | null;
		lastJobId?: string | null;
		lastJobStatus?: string | null;
		publicUrl?: string | null;
		createdAt?: string | null;
		updatedAt?: string | null;
		installedAt?: string | null;
		displayStatus: ApplicationDisplayStatus;
	};

	type ServerItem = {
		machineId: string;
		machineName: string;
		machineStatus: MachineConnectionStatus;
		appCount: number;
		runningCount: number;
		failedCount: number;
		lastActivity: string | null;
	};

	let {
		applications = [],
		machines = [],
		uninstallError = null,
		uninstallSuccess = null,
		openError = null
	}: {
		applications?: ApplicationState[];
		machines?: Machine[];
		uninstallError?: string | null;
		uninstallSuccess?: string | null;
		openError?: string | null;
	} = $props();

	let selectedView = $state<InventoryView>('all');
	let showOfflineApplications = $state(false);

	function humanizeSlug(value: string) {
		return value
			.split(/[-_]/g)
			.filter(Boolean)
			.map((part) => part.charAt(0).toUpperCase() + part.slice(1))
			.join(' ');
	}

	function safeDate(value?: string | null) {
		if (!value) return null;
		const date = new Date(value);
		return Number.isNaN(date.getTime()) ? null : date;
	}

	function computeDisplayStatus(app: ApplicationState): ApplicationDisplayStatus {
		if (
			app.transition === 'installing' ||
			app.transition === 'uninstalling' ||
			['pending', 'claimed', 'running'].includes(String(app.last_job_status ?? ''))
		) {
			return 'running';
		}

		if (String(app.last_job_status ?? '') === 'failed' || app.last_error) {
			return 'failed';
		}

		return 'completed';
	}

	function subtitle(item: InventoryItem) {
		if (item.machineStatus === 'offline') {
			return 'Serveur temporairement indisponible. Application masquée par défaut tant que l’agent est hors ligne.';
		}
		if (item.transition === 'installing') return 'Déploiement en cours sur ce serveur.';
		if (item.transition === 'uninstalling') return 'Désinstallation en cours sur ce serveur.';
		if (item.lastError) return item.lastError;
		if (!item.present) return 'Application non présente actuellement sur le serveur.';
		return 'Application disponible sur ce serveur.';
	}

	function activeStatClass(view: InventoryView) {
		return selectedView === view
			? 'ring-2 ring-cyan-400/40 dark:ring-cyan-400/30'
			: 'ring-1 ring-black/5 dark:ring-white/10';
	}

	const machineById = $derived(new Map((machines ?? []).map((machine) => [machine.id, machine])));

	const appItems = $derived.by(() => {
		return (applications ?? [])
			.map((app) => {
				const machine = machineById.get(app.machine_id);
				if (!machine) return null;

				const machineStatus = resolveMachineConnectionStatus(machine);
				return {
					id: app.id,
					machineId: app.machine_id,
					machineName: machine.hostname?.trim() || machine.machine_uuid || app.machine_id,
					machineStatus,
					appTitle: app.app_name?.trim() || humanizeSlug(app.app_slug),
					appSlug: app.app_slug,
					present: app.present,
					transition: app.transition,
					lastError: app.last_error ?? null,
					lastJobId: app.last_job_id ?? null,
					lastJobStatus: app.last_job_status ?? null,
					publicUrl: app.public_url ?? null,
					createdAt: app.created_at ?? null,
					updatedAt: app.updated_at ?? null,
					installedAt: app.installed_at ?? null,
					displayStatus: computeDisplayStatus(app)
				} satisfies InventoryItem;
			})
			.filter((item): item is InventoryItem => Boolean(item))
			.filter((item) => item.present || item.displayStatus !== 'completed' || item.lastError);
	});

	const offlineItems = $derived(appItems.filter((item) => item.machineStatus === 'offline'));
	const hasOfflineApplications = $derived(offlineItems.length > 0);
	const hiddenOfflineCount = $derived(showOfflineApplications ? 0 : offlineItems.length);
	const hiddenUnpairedCount = $derived(Math.max((applications?.length ?? 0) - appItems.length, 0));

	const visiblePool = $derived(
		showOfflineApplications ? appItems : appItems.filter((item) => item.machineStatus === 'online')
	);

	const installedCount = $derived(visiblePool.filter((item) => item.displayStatus === 'completed').length);
	const runningCount = $derived(visiblePool.filter((item) => item.displayStatus === 'running').length);
	const failedCount = $derived(visiblePool.filter((item) => item.displayStatus === 'failed').length);
	const serverCount = $derived(new Set(visiblePool.map((item) => item.machineId)).size);

	const serverItems = $derived.by(() => {
		const grouped = new Map<string, ServerItem>();

		for (const item of visiblePool) {
			const existing = grouped.get(item.machineId);
			const activity = item.updatedAt ?? item.installedAt ?? item.createdAt ?? null;

			if (!existing) {
				grouped.set(item.machineId, {
					machineId: item.machineId,
					machineName: item.machineName,
					machineStatus: item.machineStatus,
					appCount: 1,
					runningCount: item.displayStatus === 'running' ? 1 : 0,
					failedCount: item.displayStatus === 'failed' ? 1 : 0,
					lastActivity: activity
				});
				continue;
			}

			existing.appCount += 1;
			if (item.displayStatus === 'running') existing.runningCount += 1;
			if (item.displayStatus === 'failed') existing.failedCount += 1;

			const current = safeDate(existing.lastActivity)?.getTime() ?? 0;
			const next = safeDate(activity)?.getTime() ?? 0;
			if (next >= current) {
				existing.lastActivity = activity;
			}
		}

		return Array.from(grouped.values()).sort((a, b) => {
			const aTime = safeDate(a.lastActivity)?.getTime() ?? 0;
			const bTime = safeDate(b.lastActivity)?.getTime() ?? 0;
			return bTime - aTime;
		});
	});

	const visibleItems = $derived.by(() => {
		switch (selectedView) {
			case 'installed':
				return visiblePool.filter((item) => item.displayStatus === 'completed');
			case 'running':
				return visiblePool.filter((item) => item.displayStatus === 'running');
			case 'failed':
				return visiblePool.filter((item) => item.displayStatus === 'failed');
			default:
				return visiblePool;
		}
	});

	function canOpen(item: InventoryItem) {
		if (item.machineStatus !== 'online') return false;
		if (!item.present) return false;
		if (item.transition !== 'idle') return false;
		return Boolean(item.publicUrl);
	}

	function appHref(item: InventoryItem) {
		if (!canOpen(item)) return null;
		return item.publicUrl ?? null;
	}

	function logHref(item: InventoryItem) {
		if (!item.lastJobId) return null;
		return item.lastJobStatus === 'failed' || item.transition === 'uninstalling'
			? `/uninstallations/${item.lastJobId}`
			: `/installations/${item.lastJobId}`;
	}

	function canUninstall(item: InventoryItem) {
		return item.machineStatus === 'online' && item.present && item.transition === 'idle';
	}

	function uninstallLabel(item: InventoryItem) {
		if (item.machineStatus !== 'online') return 'Serveur hors ligne';
		if (!item.present) return 'Déjà absente';
		if (item.transition === 'uninstalling') return 'Désinstallation en cours';
		if (item.transition === 'installing') return 'Déploiement en cours';
		return 'Désinstaller';
	}
</script>

{#if uninstallSuccess}
	<div class="mx-auto mt-6 max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="rounded-[18px] border border-emerald-200 bg-emerald-50/80 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/10 dark:text-emerald-300">
			{uninstallSuccess}
		</div>
	</div>
{/if}

{#if uninstallError}
	<div class="mx-auto mt-6 max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="rounded-[18px] border border-rose-200 bg-rose-50/80 px-4 py-3 text-sm text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/10 dark:text-rose-300">
			{uninstallError}
		</div>
	</div>
{/if}

{#if openError}
	<div class="mx-auto mt-6 max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="rounded-[18px] border border-amber-200 bg-amber-50/80 px-4 py-3 text-sm text-amber-700 dark:border-amber-400/15 dark:bg-amber-500/10 dark:text-amber-300">
			{openError}
		</div>
	</div>
{/if}

<section class="mx-auto max-w-7xl px-4 pt-6 sm:px-6 lg:px-8">
	<div class="rounded-[24px] border border-black/5 bg-white/80 p-5 shadow-[0_18px_50px_rgba(15,23,42,0.08)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_18px_50px_rgba(0,0,0,0.30)]">
		<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
			<div>
				<p class="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">
					Inventaire
				</p>
				<h2 class="mt-2 text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
					{selectedView === 'servers' ? 'Répartition par serveur' : 'Applications visibles'}
				</h2>
				<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
					{#if hiddenOfflineCount > 0}
						{hiddenOfflineCount} application{hiddenOfflineCount > 1 ? 's' : ''} masquée{hiddenOfflineCount > 1 ? 's' : ''} car leur serveur est hors ligne.
					{:else}
						Toutes les applications visibles appartiennent à des serveurs actuellement en ligne.
					{/if}
					{#if hiddenUnpairedCount > 0}
						 {hiddenUnpairedCount} application{hiddenUnpairedCount > 1 ? 's' : ''} supplémentaire{hiddenUnpairedCount > 1 ? 's' : ''} masquée{hiddenUnpairedCount > 1 ? 's' : ''} car le serveur n’est plus appairé.
					{/if}
				</p>
			</div>

			{#if hasOfflineApplications}
				<label class="inline-flex items-center gap-3 rounded-[16px] border border-black/5 bg-white/80 px-4 py-3 text-sm text-zinc-700 shadow-[0_10px_24px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200">
					<input bind:checked={showOfflineApplications} type="checkbox" class="h-4 w-4 rounded border-zinc-300 text-cyan-600 focus:ring-cyan-500" />
					<span>Afficher les applications des serveurs hors ligne</span>
				</label>
			{/if}
		</div>

		<div class="mt-6 grid gap-3 md:grid-cols-4">
			<button type="button" onclick={() => (selectedView = 'installed')} class={`inline-flex items-center justify-between rounded-[18px] border px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_12px_28px_rgba(0,0,0,0.20)] ${activeStatClass('installed')}`}>
				<span>
					<span class="block text-xs uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">Installées</span>
					<span class="mt-1 block text-lg font-semibold text-zinc-950 dark:text-zinc-50">{installedCount}</span>
				</span>
			</button>
			<button type="button" onclick={() => (selectedView = 'running')} class={`inline-flex items-center justify-between rounded-[18px] border border-cyan-200/70 bg-cyan-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(14,165,233,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-cyan-400/15 dark:bg-cyan-500/[0.08] ${activeStatClass('running')}`}>
				<span>
					<span class="block text-xs uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">En cours</span>
					<span class="mt-1 block text-lg font-semibold text-zinc-950 dark:text-zinc-50">{runningCount}</span>
				</span>
			</button>
			<button type="button" onclick={() => (selectedView = 'failed')} class={`inline-flex items-center justify-between rounded-[18px] border border-rose-200/70 bg-rose-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(244,63,94,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-rose-400/15 dark:bg-rose-500/[0.08] ${activeStatClass('failed')}`}>
				<span>
					<span class="block text-xs uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">Incidents</span>
					<span class="mt-1 block text-lg font-semibold text-zinc-950 dark:text-zinc-50">{failedCount}</span>
				</span>
			</button>
			<button type="button" onclick={() => (selectedView = 'servers')} class={`inline-flex items-center justify-between rounded-[18px] border border-indigo-200/70 bg-indigo-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(99,102,241,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-indigo-400/15 dark:bg-indigo-500/[0.08] ${activeStatClass('servers')}`}>
				<span>
					<span class="block text-xs uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400">Serveurs visibles</span>
					<span class="mt-1 block text-lg font-semibold text-zinc-950 dark:text-zinc-50">{serverCount}</span>
				</span>
			</button>
		</div>

		<div class="mt-4 flex flex-wrap items-center gap-2">
			<button type="button" onclick={() => (selectedView = 'all')} class={`inline-flex items-center justify-center rounded-[14px] border px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] transition ${selectedView === 'all' ? 'border-cyan-300 bg-cyan-50 text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-500/10 dark:text-cyan-300' : 'border-black/5 bg-white/80 text-zinc-600 hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300 dark:hover:border-white/14 dark:hover:bg-white/[0.06]'}`}>
				Tout afficher
			</button>
		</div>
	</div>
</section>

<section class="mx-auto max-w-7xl px-4 pb-8 sm:px-6 lg:px-8">
	{#if selectedView === 'servers'}
		{#if serverItems.length > 0}
			<div class="mt-6 grid gap-4 lg:grid-cols-2">
				{#each serverItems as server}
					<article class="rounded-[24px] border border-black/5 bg-white/80 p-5 shadow-[0_14px_36px_rgba(15,23,42,0.07)] backdrop-blur-xl dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_14px_36px_rgba(0,0,0,0.28)]">
						<div class="flex items-start justify-between gap-4">
							<div>
								<h3 class="text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">{server.machineName}</h3>
								<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">Apps : {server.appCount} · En cours : {server.runningCount} · Incidents : {server.failedCount}</p>
							</div>
							<span class={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${machinePillClass(server.machineStatus)}`}>{machineStatusLabel(server.machineStatus)}</span>
						</div>
						<p class="mt-4 text-sm text-zinc-500 dark:text-zinc-400">Dernière activité : {formatFrenchDateTime(server.lastActivity)}</p>
					</article>
				{/each}
			</div>
		{:else}
			<div class="mt-6 rounded-[24px] border border-dashed border-black/10 bg-white/70 px-6 py-10 text-center dark:border-white/10 dark:bg-white/[0.03]">
				<h3 class="text-lg font-semibold text-zinc-950 dark:text-zinc-50">Aucun serveur visible</h3>
			</div>
		{/if}
	{:else if visibleItems.length > 0}
		<div class="mt-6 grid gap-4">
			{#each visibleItems as item}
				<article class="rounded-[20px] border border-black/5 bg-white/70 p-5 shadow-[0_12px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03]">
					<div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-3">
								{#if appHref(item)}
									<h3 class="truncate text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">
										<a href={appHref(item) ?? '#'} target="_blank" rel="noreferrer" class="inline-flex items-center gap-2 underline-offset-4 transition hover:text-sky-600 hover:underline dark:hover:text-sky-300">
											<span class="truncate">{item.appTitle}</span>
											<span class="shrink-0">↗</span>
										</a>
									</h3>
								{:else}
									<h3 class="truncate text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">
										{item.appTitle}
									</h3>
								{/if}

								{#if item.machineStatus === 'offline'}
									<span class={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${machinePillClass(item.machineStatus)}`}>{machineStatusLabel(item.machineStatus)}</span>
								{:else}
									<JobStatusBadge status={item.displayStatus} variant="applications" className="shrink-0" />
								{/if}
							</div>

							<p class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Déployée sur {item.machineName}</p>

							<div class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
								<div>
									<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Application</p>
									<p class="mt-1 text-sm text-zinc-900 dark:text-zinc-100">{item.appSlug}</p>
								</div>
								<div>
									<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Serveur</p>
									<p class="mt-1 text-sm text-zinc-900 dark:text-zinc-100">{item.machineName}</p>
								</div>
								<div>
									<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Installée</p>
									<p class="mt-1 text-sm text-zinc-900 dark:text-zinc-100">{formatFrenchDateTime(item.installedAt)}</p>
								</div>
								<div>
									<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Mise à jour</p>
									<p class="mt-1 text-sm text-zinc-900 dark:text-zinc-100">{formatFrenchDateTime(item.updatedAt)}</p>
								</div>
							</div>

							<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-300">{subtitle(item)}</p>
						</div>

						<div class="flex flex-wrap items-center gap-2">
							{#if appHref(item)}
								<a
									href={appHref(item) ?? '#'}
									target="_blank"
									rel="noreferrer"
									class="inline-flex items-center justify-center rounded-[14px] border border-sky-200 bg-sky-50 px-3 py-2 text-sm font-medium text-sky-700 transition hover:border-sky-300 hover:bg-sky-100 dark:border-sky-400/20 dark:bg-sky-500/10 dark:text-sky-200 dark:hover:border-sky-400/30 dark:hover:bg-sky-500/15"
								>
									Ouvrir
								</a>
							{/if}

							{#if logHref(item)}
								<a href={logHref(item) ?? '#'} class="inline-flex items-center justify-center rounded-[14px] border border-black/5 bg-white px-3 py-2 text-sm font-medium text-zinc-700 transition hover:border-black/10 hover:bg-zinc-50 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]">Log</a>
							{/if}

							<form method="POST" action="?/uninstallApplication">
								<input type="hidden" name="machine_id" value={item.machineId} />
								<input type="hidden" name="app_slug" value={item.appSlug} />
								<button
									type="submit"
									disabled={!canUninstall(item)}
									onclick={(event) => {
										if (!canUninstall(item)) return;
										if (!confirm(`Désinstaller ${item.appTitle} de ${item.machineName} ?`)) {
											event.preventDefault();
										}
									}}
									class={`inline-flex items-center justify-center rounded-[14px] px-3 py-2 text-sm font-medium transition ${canUninstall(item) ? 'border border-rose-200 bg-rose-50 text-rose-700 hover:border-rose-300 hover:bg-rose-100 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/30 dark:hover:bg-rose-500/15' : 'cursor-not-allowed border border-black/5 bg-zinc-100 text-zinc-400 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-500'}`}
								>
									{uninstallLabel(item)}
								</button>
							</form>
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="mt-6 rounded-[24px] border border-dashed border-black/10 bg-white/70 px-6 py-10 text-center dark:border-white/10 dark:bg-white/[0.03]">
			<h3 class="text-lg font-semibold text-zinc-950 dark:text-zinc-50">Aucune application visible</h3>
			<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">Active le filtre hors ligne ou attends qu’un serveur se reconnecte.</p>
		</div>
	{/if}
</section>