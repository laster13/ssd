<script lang="ts">
	import JobStatusBadge from '$lib/components/apps/JobStatusBadge.svelte';
	import { formatFrenchDateTime, machinePillClass, machineStatusLabel } from '$lib/utils/jobs';
	import type { ApplicationState, Machine } from '$lib/utils/jobs';

	type InventoryView = 'all' | 'installed' | 'running' | 'failed' | 'servers';

	type InventoryItem = ApplicationState & {
		appTitle: string;
		machineName: string;
		machineStatus?: string;
		displayStatus: string;
		public_url?: string | null;
	};

	type ServerItem = {
		machineId: string;
		machineName: string;
		machineStatus?: string;
		appCount: number;
		runningCount: number;
		failedCount: number;
		lastActivity?: string | null;
	};

	let {
		applications = [],
		machines = [],
		uninstallError = null,
		uninstallSuccess = null
	}: {
		applications?: ApplicationState[];
		machines?: Machine[];
		uninstallError?: string | null;
		uninstallSuccess?: string | null;
	} = $props();

	let selectedView = $state<InventoryView>('all');

	const machineById = $derived(new Map(machines.map((machine) => [machine.id, machine])));

	function applicationDisplayStatus(app: ApplicationState) {
		if (app.transition === 'installing' || app.transition === 'uninstalling') return 'running';
		if (app.last_job_status === 'failed') return 'failed';
		if (app.present) return 'completed';
		return 'pending';
	}

	function appTitle(app: ApplicationState) {
		return app.app_name?.trim() || app.app_slug;
	}

	function canUninstall(item: InventoryItem) {
		return item.present && item.transition === 'idle';
	}

	function logHref(item: InventoryItem) {
		if (!item.last_job_id) return null;
		return item.last_operation === 'uninstall'
			? `/uninstallations/${item.last_job_id}`
			: `/installations/${item.last_job_id}`;
	}

	function appHref(item: InventoryItem) {
		if (!item.present) return null;
		if (item.transition !== 'idle') return null;
		if (!item.public_url) return null;
		return item.public_url;
	}

	function subtitle(item: InventoryItem) {
		if (item.transition === 'installing') return 'Installation en cours';
		if (item.transition === 'uninstalling') return 'Désinstallation en cours';
		if (item.last_job_status === 'failed') return item.last_error || 'Dernière opération en échec';
		if (item.present) return 'Application installée sur ce serveur';
		return 'Application non installée';
	}

	function activeStatClass(view: InventoryView) {
		return selectedView === view
			? 'ring-2 ring-black/5 dark:ring-white/10'
			: 'ring-1 ring-transparent';
	}

	function sectionTitle() {
		switch (selectedView) {
			case 'installed':
				return 'Applications installées';
			case 'running':
				return 'Opérations en cours';
			case 'failed':
				return 'Incidents';
			case 'servers':
				return 'Vue par serveur';
			default:
				return 'Inventaire actuel';
		}
	}

	function sectionDescription() {
		switch (selectedView) {
			case 'installed':
				return 'Uniquement les applications réellement présentes.';
			case 'running':
				return 'Installations et désinstallations actuellement en cours.';
			case 'failed':
				return 'Applications dont la dernière opération a échoué.';
			case 'servers':
				return 'Résumé par machine.';
			default:
				return 'État courant des applications, séparé de l’historique des jobs.';
		}
	}

	const items = $derived.by(() => {
		return applications
			.filter((app) => app.present || app.transition !== 'idle' || app.last_job_status === 'failed')
			.map((app) => {
				const machine = machineById.get(app.machine_id);

				return {
					...app,
					appTitle: appTitle(app),
					machineName: machine?.hostname ?? machine?.machine_uuid ?? app.machine_id,
					machineStatus: machine?.status,
					displayStatus: applicationDisplayStatus(app)
				} satisfies InventoryItem;
			})
			.sort((a, b) => {
				const aTime = a.updated_at ? new Date(a.updated_at).getTime() : 0;
				const bTime = b.updated_at ? new Date(b.updated_at).getTime() : 0;
				return bTime - aTime;
			});
	});

	const installedItems = $derived.by(() =>
		items.filter((item) => item.present && item.transition === 'idle' && item.last_job_status !== 'failed')
	);

	const runningItems = $derived.by(() =>
		items.filter((item) => item.transition === 'installing' || item.transition === 'uninstalling')
	);

	const failedItems = $derived.by(() => items.filter((item) => item.last_job_status === 'failed'));

	const serverItems = $derived.by(() => {
		const grouped = new Map<string, ServerItem>();

		for (const item of items) {
			const existing = grouped.get(item.machine_id);
			const activity = item.updated_at ?? item.installed_at ?? null;

			if (!existing) {
				grouped.set(item.machine_id, {
					machineId: item.machine_id,
					machineName: item.machineName,
					machineStatus: item.machineStatus,
					appCount: item.present ? 1 : 0,
					runningCount: item.transition !== 'idle' ? 1 : 0,
					failedCount: item.last_job_status === 'failed' ? 1 : 0,
					lastActivity: activity
				});
				continue;
			}

			if (item.present) existing.appCount += 1;
			if (item.transition !== 'idle') existing.runningCount += 1;
			if (item.last_job_status === 'failed') existing.failedCount += 1;

			if (activity) {
				const current = existing.lastActivity ? new Date(existing.lastActivity).getTime() : 0;
				const next = new Date(activity).getTime();
				if (next >= current) {
					existing.lastActivity = activity;
				}
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
				return items;
		}
	});

	const installedCount = $derived(installedItems.length);
	const activeCount = $derived(runningItems.length);
	const incidentCount = $derived(failedItems.length);
	const serverCount = $derived(serverItems.length);
</script>

<section class="bg-zinc-50 pb-8 dark:bg-[#07111f]">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		{#if uninstallSuccess}
			<div
				class="mb-4 rounded-[18px] border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-500/10 dark:text-emerald-200"
			>
				{uninstallSuccess}
			</div>
		{/if}

		{#if uninstallError}
			<div
				class="mb-4 rounded-[18px] border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200"
			>
				{uninstallError}
			</div>
		{/if}

		<div class="grid gap-3 md:grid-cols-4">
			<button
				type="button"
				onclick={() => (selectedView = 'installed')}
				class={`inline-flex items-center justify-between rounded-[18px] border px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_12px_28px_rgba(0,0,0,0.20)] ${activeStatClass('installed')}`}
			>
				<span>Installées</span>
				<span class="font-semibold">{installedCount}</span>
			</button>

			<button
				type="button"
				onclick={() => (selectedView = 'running')}
				class={`inline-flex items-center justify-between rounded-[18px] border border-cyan-200/70 bg-cyan-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(14,165,233,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-cyan-400/15 dark:bg-cyan-500/[0.08] ${activeStatClass('running')}`}
			>
				<span>En cours</span>
				<span class="font-semibold">{activeCount}</span>
			</button>

			<button
				type="button"
				onclick={() => (selectedView = 'failed')}
				class={`inline-flex items-center justify-between rounded-[18px] border border-rose-200/70 bg-rose-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(244,63,94,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-rose-400/15 dark:bg-rose-500/[0.08] ${activeStatClass('failed')}`}
			>
				<span>Incidents</span>
				<span class="font-semibold">{incidentCount}</span>
			</button>

			<button
				type="button"
				onclick={() => (selectedView = 'servers')}
				class={`inline-flex items-center justify-between rounded-[18px] border border-emerald-200/70 bg-emerald-50/80 px-4 py-3 text-left text-sm shadow-[0_12px_30px_rgba(16,185,129,0.08)] backdrop-blur-xl transition hover:-translate-y-0.5 dark:border-emerald-400/15 dark:bg-emerald-500/[0.08] ${activeStatClass('servers')}`}
			>
				<span>Serveurs</span>
				<span class="font-semibold">{serverCount}</span>
			</button>
		</div>

		<div
			class="mt-6 rounded-[24px] border border-black/5 bg-white/80 p-5 shadow-[0_18px_50px_rgba(15,23,42,0.08)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_18px_50px_rgba(0,0,0,0.30)]"
		>
			<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
				<div>
					<p
						class="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:text-zinc-400"
					>
						Inventaire
					</p>
					<h2
						class="mt-2 text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50"
					>
						{sectionTitle()}
					</h2>
					<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
						{sectionDescription()}
					</p>
				</div>

				<button
					type="button"
					onclick={() => (selectedView = 'all')}
					class="inline-flex items-center justify-center rounded-[14px] border border-black/5 bg-white/80 px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-600 transition hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300 dark:hover:border-white/14 dark:hover:bg-white/[0.06]"
				>
					Tout afficher
				</button>
			</div>

			<p class="mt-3 text-xs font-medium uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
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
			</p>

			{#if selectedView === 'servers'}
				{#if serverItems.length > 0}
					<div class="mt-6 grid gap-4 md:grid-cols-2">
						{#each serverItems as server}
							<article
								class="rounded-[20px] border border-black/5 bg-white/70 p-5 shadow-[0_12px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03]"
							>
								<div class="flex items-start justify-between gap-4">
									<div>
										<h3
											class="text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50"
										>
											{server.machineName}
										</h3>
										<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
											Apps : {server.appCount} · En cours : {server.runningCount} · Incidents :
											{server.failedCount}
										</p>
										<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
											Dernière activité : {formatFrenchDateTime(server.lastActivity)}
										</p>
									</div>

									<span
										class={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${machinePillClass(server.machineStatus)}`}
									>
										{machineStatusLabel(server.machineStatus)}
									</span>
								</div>
							</article>
						{/each}
					</div>
				{:else}
					<div
						class="mt-6 rounded-[20px] border border-black/5 bg-white/70 p-8 text-center dark:border-white/10 dark:bg-white/[0.03]"
					>
						<div class="text-2xl">✦</div>
						<h3
							class="mt-3 text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50"
						>
							Aucun serveur trouvé
						</h3>
						<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
							Aucune activité serveur n’est encore disponible.
						</p>
					</div>
				{/if}
			{:else if visibleItems.length > 0}
				<div class="mt-6 grid gap-4">
					{#each visibleItems as item}
						<article
							class="rounded-[20px] border border-black/5 bg-white/70 p-5 shadow-[0_12px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03]"
						>
							<div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
								<div class="min-w-0 flex-1">
									<div class="flex flex-wrap items-center gap-3">
										{#if appHref(item)}
											<h3
												class="truncate text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50"
											>
												<a
													href={appHref(item) ?? '#'}
													target="_blank"
													rel="noreferrer"
													class="inline-flex items-center gap-2 underline-offset-4 transition hover:text-sky-600 hover:underline dark:hover:text-sky-300"
												>
													<span class="truncate">{item.appTitle}</span>
													<span class="shrink-0">↗</span>
												</a>
											</h3>
										{:else}
											<h3
												class="truncate text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50"
											>
												{item.appTitle}
											</h3>
										{/if}

										<JobStatusBadge
											status={item.displayStatus}
											variant="applications"
											className="shrink-0"
										/>
									</div>

									<div class="mt-2 flex flex-wrap gap-x-5 gap-y-1 text-sm text-zinc-500 dark:text-zinc-400">
										<span>Application : {item.app_slug}</span>
										<span>Serveur : {item.machineName}</span>
										<span>Installée : {formatFrenchDateTime(item.installed_at)}</span>
										<span>Maj : {formatFrenchDateTime(item.updated_at)}</span>
										<span
											class={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${machinePillClass(item.machineStatus)}`}
										>
											{machineStatusLabel(item.machineStatus)}
										</span>
									</div>

									<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
										{subtitle(item)}
									</p>
								</div>

								<div class="flex flex-wrap items-center gap-2">
									{#if logHref(item)}
										<a
											href={logHref(item) ?? '#'}
											class="inline-flex items-center justify-center rounded-[14px] border border-black/5 bg-white px-3 py-2 text-sm font-medium text-zinc-700 transition hover:border-black/10 hover:bg-zinc-50 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
										>
											Log
										</a>
									{/if}

									{#if canUninstall(item)}
										<form method="POST" action="?/uninstallApplication">
											<input type="hidden" name="machine_id" value={item.machine_id} />
											<input type="hidden" name="app_slug" value={item.app_slug} />
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
				<div
					class="mt-6 rounded-[20px] border border-black/5 bg-white/70 p-8 text-center dark:border-white/10 dark:bg-white/[0.03]"
				>
					<div class="text-2xl">✦</div>
					<h3
						class="mt-3 text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50"
					>
						Aucun contenu pour ce filtre
					</h3>
					<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
						Essaie une autre carte ou clique sur “Tout afficher”.
					</p>
				</div>
			{/if}
		</div>
	</div>
</section>