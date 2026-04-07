<script lang="ts">
	import { tick } from 'svelte';

	let { data, form } = $props();

	const jobs = data.jobs ?? [];
	const machines = data.machines ?? [];
	const csrfToken = data.csrfToken as string;

	const deleteMachineError = $derived((form?.deleteMachineError ?? null) as string | null);
	const deleteMachineSuccess = $derived((form?.deleteMachineSuccess ?? null) as string | null);

	const RUNNING_JOB_STATUSES = ['running', 'processing', 'pending'];
	const FAILED_JOB_STATUSES = ['failed', 'error'];
	const SUCCESS_JOB_STATUSES = ['completed', 'success', 'done'];

	let machineFilter = $state<'all' | 'active' | 'offline' | 'error' | 'revoked'>('all');
	let jobFilter = $state<'all' | 'running' | 'failed' | 'success'>('all');

	let machinesSection = $state<HTMLElement | null>(null);
	let jobsSection = $state<HTMLElement | null>(null);

	function toTimestamp(value: unknown): number | null {
		if (!value) return null;
		const date = new Date(String(value));
		const time = date.getTime();
		return Number.isNaN(time) ? null : time;
	}

	function formatAbsoluteDate(value: unknown) {
		const ts = toTimestamp(value);
		if (!ts) return '-';

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'short',
			timeStyle: 'short'
		}).format(new Date(ts));
	}

	function formatRelativeDate(value: unknown) {
		const ts = toTimestamp(value);
		if (!ts) return '-';

		const diffMs = ts - Date.now();
		const diffMin = Math.round(diffMs / 60000);

		const rtf = new Intl.RelativeTimeFormat('fr', { numeric: 'auto' });

		if (Math.abs(diffMin) < 1) return 'à l’instant';
		if (Math.abs(diffMin) < 60) return rtf.format(diffMin, 'minute');

		const diffHours = Math.round(diffMin / 60);
		if (Math.abs(diffHours) < 24) return rtf.format(diffHours, 'hour');

		const diffDays = Math.round(diffHours / 24);
		return rtf.format(diffDays, 'day');
	}

	function formatDateLabel(value: unknown) {
		const absolute = formatAbsoluteDate(value);
		const relative = formatRelativeDate(value);

		if (absolute === '-') return '-';
		return `${relative} · ${absolute}`;
	}

	function machineCategory(status: string) {
		switch (status?.toLowerCase()) {
			case 'paired':
			case 'online':
			case 'connected':
			case 'active':
				return 'active';

			case 'offline':
			case 'disconnected':
			case 'inactive':
				return 'offline';

			case 'error':
			case 'failed':
				return 'error';

			case 'revoked':
				return 'revoked';

			default:
				return 'unknown';
		}
	}

	function normalizeMachineStatus(status: string) {
		switch (machineCategory(status)) {
			case 'active':
				return 'En ligne';
			case 'offline':
				return 'Hors ligne';
			case 'error':
				return 'En erreur';
			case 'revoked':
				return 'Révoquée';
			default:
				return status || 'Inconnu';
		}
	}

	function normalizeJobStatus(status: string) {
		switch (status?.toLowerCase()) {
			case 'pending':
				return 'En attente';
			case 'running':
			case 'processing':
				return 'En cours';
			case 'completed':
			case 'success':
			case 'done':
				return 'Terminé';
			case 'failed':
			case 'error':
				return 'Échec';
			default:
				return status || 'Inconnu';
		}
	}

	function machineStatusClass(status: string) {
		switch (machineCategory(status)) {
			case 'active':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300';
			case 'offline':
				return 'border-zinc-200 bg-zinc-100 text-zinc-700 dark:border-white/10 dark:bg-white/5 dark:text-zinc-300';
			case 'error':
				return 'border-red-200 bg-red-50 text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300';
			case 'revoked':
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300';
			default:
				return 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300';
		}
	}

	function jobStatusClass(status: string) {
		switch (status?.toLowerCase()) {
			case 'completed':
			case 'success':
			case 'done':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300';
			case 'running':
			case 'processing':
			case 'pending':
				return 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300';
			case 'failed':
			case 'error':
				return 'border-red-200 bg-red-50 text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300';
			default:
				return 'border-zinc-200 bg-zinc-100 text-zinc-700 dark:border-white/10 dark:bg-white/5 dark:text-zinc-300';
		}
	}

	function isMachineActive(status: string) {
		return machineCategory(status) === 'active';
	}

	function isMachineOffline(status: string) {
		return machineCategory(status) === 'offline';
	}

	function isMachineError(status: string) {
		return machineCategory(status) === 'error';
	}

	function isMachineRevoked(status: string) {
		return machineCategory(status) === 'revoked';
	}

	function isJobRunning(status: string) {
		return RUNNING_JOB_STATUSES.includes(status?.toLowerCase());
	}

	function isJobFailed(status: string) {
		return FAILED_JOB_STATUSES.includes(status?.toLowerCase());
	}

	function isJobSuccess(status: string) {
		return SUCCESS_JOB_STATUSES.includes(status?.toLowerCase());
	}

	const activeMachinesCount = machines.filter((m) => isMachineActive(m.status)).length;
	const offlineMachinesCount = machines.filter((m) => isMachineOffline(m.status)).length;
	const errorMachinesCount = machines.filter((m) => isMachineError(m.status)).length;
	const revokedMachinesCount = machines.filter((m) => isMachineRevoked(m.status)).length;

	const runningJobsCount = jobs.filter((j) => isJobRunning(j.status)).length;
	const failedJobsCount = jobs.filter((j) => isJobFailed(j.status)).length;
	const successJobsCount = jobs.filter((j) => isJobSuccess(j.status)).length;

	const machineItems = machines.map((machine) => {
		let priority = 4;

		if (isMachineError(machine.status)) priority = 0;
		else if (isMachineOffline(machine.status)) priority = 1;
		else if (isMachineRevoked(machine.status)) priority = 2;
		else if (isMachineActive(machine.status)) priority = 3;

		return {
			...machine,
			priority,
			lastSeenTs: toTimestamp(machine.last_seen_at),
			createdTs: toTimestamp(machine.created_at)
		};
	});

	const jobItems = jobs.map((job) => {
		let priority = 3;

		if (isJobFailed(job.status)) priority = 0;
		else if (isJobRunning(job.status)) priority = 1;
		else if (isJobSuccess(job.status)) priority = 2;

		return {
			...job,
			priority,
			createdTs: toTimestamp(job.created_at)
		};
	});

	const sortedMachines = [...machineItems].sort((a, b) => {
		if (a.priority !== b.priority) return a.priority - b.priority;
		return (b.lastSeenTs ?? 0) - (a.lastSeenTs ?? 0);
	});

	const sortedJobs = [...jobItems].sort((a, b) => {
		if (a.priority !== b.priority) return a.priority - b.priority;
		return (b.createdTs ?? 0) - (a.createdTs ?? 0);
	});

	const filteredMachines = $derived(
		sortedMachines.filter((machine) => {
			if (machineFilter === 'active') return isMachineActive(machine.status);
			if (machineFilter === 'offline') return isMachineOffline(machine.status);
			if (machineFilter === 'error') return isMachineError(machine.status);
			if (machineFilter === 'revoked') return isMachineRevoked(machine.status);
			return true;
		})
	);

	const filteredJobs = $derived(
		sortedJobs.filter((job) => {
			if (jobFilter === 'running') return isJobRunning(job.status);
			if (jobFilter === 'failed') return isJobFailed(job.status);
			if (jobFilter === 'success') return isJobSuccess(job.status);
			return true;
		})
	);

	const attentionMachines = sortedMachines
		.filter((machine) => isMachineError(machine.status) || isMachineOffline(machine.status))
		.slice(0, 4);

	const attentionJobs = sortedJobs.filter((job) => isJobFailed(job.status)).slice(0, 4);

	function cardClass(active: boolean) {
		return active
			? 'ring-2 ring-sky-400/70 border-sky-200 dark:border-sky-400/20'
			: 'border-black/5 dark:border-white/10';
	}

	function filterButtonClass(active: boolean) {
		return active
			? 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300'
			: 'border-black/8 bg-black/[0.03] text-zinc-700 hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]';
	}

	async function showMachines(filter: 'all' | 'active' | 'offline' | 'error' | 'revoked') {
		machineFilter = filter;
		await tick();
		machinesSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	async function showJobs(filter: 'all' | 'running' | 'failed' | 'success') {
		jobFilter = filter;
		await tick();
		jobsSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	function machineSectionTitle() {
		switch (machineFilter) {
			case 'active':
				return 'Machines en ligne';
			case 'offline':
				return 'Machines hors ligne';
			case 'error':
				return 'Machines en erreur';
			case 'revoked':
				return 'Machines révoquées';
			default:
				return 'Toutes les machines';
		}
	}

	function machineSectionDescription() {
		switch (machineFilter) {
			case 'active':
				return 'Machines actuellement disponibles côté plateforme.';
			case 'offline':
				return 'Machines déconnectées ou inactives à vérifier.';
			case 'error':
				return 'Machines nécessitant une attention prioritaire.';
			case 'revoked':
				return 'Machines explicitement coupées du backend.';
			default:
				return 'Inventaire complet, trié par priorité opérationnelle.';
		}
	}

	function jobSectionTitle() {
		switch (jobFilter) {
			case 'running':
				return 'Jobs en cours';
			case 'failed':
				return 'Jobs en échec';
			case 'success':
				return 'Jobs terminés';
			default:
				return 'Tous les jobs';
		}
	}

	function jobSectionDescription() {
		switch (jobFilter) {
			case 'running':
				return 'Tâches actuellement en attente ou d’exécution.';
			case 'failed':
				return 'Tâches à investiguer en priorité.';
			case 'success':
				return 'Tâches finalisées avec succès.';
			default:
				return 'Historique trié par criticité puis récence.';
		}
	}
</script>

<svelte:head>
	<title>Admin</title>
</svelte:head>

<section class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
		<div>
			<div
				class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300"
			>
				<span class="h-1.5 w-1.5 rounded-full bg-orange-400"></span>
				Administration
			</div>

			<h1
				class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]"
			>
				<span
					class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]"
				>
					Tableau de bord administration
				</span>
			</h1>

			<p class="mt-3 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
				Vue d’ensemble des machines et des jobs, triée pour repérer rapidement ce qui est
				normal, ce qui est en cours et ce qui demande une intervention.
			</p>
		</div>

		<div class="flex flex-wrap gap-3">
			<a
				href="/admin/security-audit"
				class="inline-flex items-center justify-center rounded-[16px] border border-amber-200 bg-[linear-gradient(90deg,#f59e0b,#ea580c)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(234,88,12,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(234,88,12,0.26)] dark:border-white/10"
			>
				Audit sécurité
			</a>

			<a
				href="/admin/users"
				class="inline-flex items-center justify-center rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
			>
				Gérer les utilisateurs
			</a>
		</div>
	</div>

	<div class="mb-3">
		<p class="text-xs font-medium uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
			Indicateurs clés
		</p>
	</div>

	<div class="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
		<button
			type="button"
			onclick={() => showMachines('active')}
			class={`rounded-[24px] border bg-white/70 p-5 text-left shadow-[0_20px_80px_rgba(15,23,42,0.08)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(15,23,42,0.12)] dark:bg-white/[0.035] ${cardClass(machineFilter === 'active')}`}
		>
			<div class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Machines en ligne
			</div>
			<div class="mt-3 text-3xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
				{activeMachinesCount}
			</div>
			<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
				Afficher les machines disponibles
			</p>
		</button>

		<button
			type="button"
			onclick={() => showMachines('offline')}
			class={`rounded-[24px] border bg-white/70 p-5 text-left shadow-[0_20px_80px_rgba(15,23,42,0.08)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(15,23,42,0.12)] dark:bg-white/[0.035] ${cardClass(machineFilter === 'offline')}`}
		>
			<div class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Machines hors ligne
			</div>
			<div class="mt-3 text-3xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
				{offlineMachinesCount}
			</div>
			<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
				Afficher les machines déconnectées
			</p>
		</button>

		<button
			type="button"
			onclick={() => showJobs('running')}
			class={`rounded-[24px] border bg-white/70 p-5 text-left shadow-[0_20px_80px_rgba(15,23,42,0.08)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(15,23,42,0.12)] dark:bg-white/[0.035] ${cardClass(jobFilter === 'running')}`}
		>
			<div class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Jobs en cours
			</div>
			<div class="mt-3 text-3xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
				{runningJobsCount}
			</div>
			<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
				Tâches en attente ou d’exécution
			</p>
		</button>

		<button
			type="button"
			onclick={() => showJobs('failed')}
			class={`rounded-[24px] border bg-white/70 p-5 text-left shadow-[0_20px_80px_rgba(15,23,42,0.08)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(15,23,42,0.12)] dark:bg-white/[0.035] ${cardClass(jobFilter === 'failed')}`}
		>
			<div class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
				Jobs en échec
			</div>
			<div class="mt-3 text-3xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
				{failedJobsCount}
			</div>
			<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
				Afficher les tâches à investiguer
			</p>
		</button>
	</div>

	<div class="mb-8 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
		<div
			class="overflow-hidden rounded-[30px] border border-red-200/60 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-red-400/15 dark:bg-white/[0.035]"
		>
			<div class="relative">
				<div
					class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
				></div>

				<div class="relative p-6 sm:p-8">
					<div class="mb-4">
						<div
							class="mb-2 inline-flex items-center gap-2 rounded-full border border-red-200 bg-red-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300"
						>
							À traiter maintenant
						</div>
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Éléments prioritaires
						</h2>
						<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
							Les incidents et anomalies les plus visibles du moment.
						</p>
					</div>

					<div class="grid gap-3">
						{#if attentionMachines.length === 0 && attentionJobs.length === 0}
							<div
								class="rounded-[20px] border border-dashed border-emerald-200 bg-emerald-50/70 px-4 py-4 text-sm text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300"
							>
								Aucun point critique détecté pour le moment.
							</div>
						{:else}
							{#each attentionMachines as machine}
								<button
									type="button"
									onclick={() =>
										showMachines(
											isMachineError(machine.status)
												? 'error'
												: isMachineOffline(machine.status)
													? 'offline'
													: isMachineRevoked(machine.status)
														? 'revoked'
														: 'all'
										)}
									class="flex items-start justify-between gap-4 rounded-[20px] border border-black/5 bg-black/[0.02] p-4 text-left transition hover:bg-black/[0.03] dark:border-white/10 dark:bg-white/[0.03] dark:hover:bg-white/[0.05]"
								>
									<div class="min-w-0">
										<div class="text-sm font-semibold text-zinc-950 dark:text-white">
											{machine.hostname ?? `Machine #${machine.id}`}
										</div>
										<div class="mt-1 text-sm text-zinc-600 dark:text-zinc-300">
											{normalizeMachineStatus(machine.status)}
										</div>
										<div class="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
											Dernier contact : {formatDateLabel(machine.last_seen_at)}
										</div>
									</div>

									<span
										class={`inline-flex shrink-0 items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${machineStatusClass(machine.status)}`}
									>
										{normalizeMachineStatus(machine.status)}
									</span>
								</button>
							{/each}

							{#each attentionJobs as job}
								<button
									type="button"
									onclick={() => showJobs('failed')}
									class="flex items-start justify-between gap-4 rounded-[20px] border border-black/5 bg-black/[0.02] p-4 text-left transition hover:bg-black/[0.03] dark:border-white/10 dark:bg-white/[0.03] dark:hover:bg-white/[0.05]"
								>
									<div class="min-w-0">
										<div class="text-sm font-semibold text-zinc-950 dark:text-white">
											{job.type}
										</div>
										<div class="mt-1 text-sm text-zinc-600 dark:text-zinc-300">
											Machine #{job.machine_id}
										</div>
										<div class="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
											Créé : {formatDateLabel(job.created_at)}
										</div>
									</div>

									<span
										class={`inline-flex shrink-0 items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${jobStatusClass(job.status)}`}
									>
										{normalizeJobStatus(job.status)}
									</span>
								</button>
							{/each}
						{/if}
					</div>
				</div>
			</div>
		</div>

		<div
			class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]"
		>
			<div class="relative">
				<div
					class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
				></div>

				<div class="relative p-6 sm:p-8">
					<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
						Accès rapides
					</h2>

					<div class="mt-4 grid gap-3">
						<a
							href="/admin/users"
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Ouvrir la gestion utilisateurs
						</a>

						<button
							type="button"
							onclick={() => showMachines('all')}
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Voir toutes les machines ({machines.length})
						</button>

						<button
							type="button"
							onclick={() => showMachines('error')}
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Voir les machines en erreur ({errorMachinesCount})
						</button>

						<button
							type="button"
							onclick={() => showMachines('revoked')}
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Voir les machines révoquées ({revokedMachinesCount})
						</button>

						<button
							type="button"
							onclick={() => showJobs('failed')}
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Voir les jobs en échec ({failedJobsCount})
						</button>

						<button
							type="button"
							onclick={() => showJobs('running')}
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Voir les jobs en cours ({runningJobsCount})
						</button>

						<a
							href="/admin/security-audit"
							class="rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-left text-sm font-medium text-zinc-700 transition hover:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:bg-white/[0.06]"
						>
							Ouvrir l’audit sécurité
						</a>
					</div>

					<div class="mt-6 rounded-[20px] border border-black/5 bg-black/[0.02] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
						<div class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
							Résumé
						</div>
						<div class="mt-3 grid gap-2 text-sm text-zinc-700 dark:text-zinc-300">
							<p>{machines.length} machine(s) au total</p>
							<p>{activeMachinesCount} machine(s) en ligne</p>
							<p>{offlineMachinesCount} machine(s) hors ligne</p>
							<p>{errorMachinesCount} machine(s) en erreur</p>
							<p>{jobs.length} job(s) au total</p>
							<p>{runningJobsCount} job(s) en cours</p>
							<p>{failedJobsCount} job(s) en échec</p>
							<p>{successJobsCount} job(s) terminé(s)</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
		<div
			bind:this={machinesSection}
			class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]"
		>
			<div class="relative">
				<div
					class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
				></div>

				<div class="relative p-6 sm:p-8">
					<div class="mb-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
						<div>
							<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
								{machineSectionTitle()}
							</h2>
							<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
								{machineSectionDescription()}
							</p>
						</div>

						<div class="flex flex-wrap gap-2">
							<button
								type="button"
								onclick={() => showMachines('all')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(machineFilter === 'all')}`}
							>
								Toutes
							</button>
							<button
								type="button"
								onclick={() => showMachines('active')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(machineFilter === 'active')}`}
							>
								En ligne
							</button>
							<button
								type="button"
								onclick={() => showMachines('offline')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(machineFilter === 'offline')}`}
							>
								Hors ligne
							</button>
							<button
								type="button"
								onclick={() => showMachines('error')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(machineFilter === 'error')}`}
							>
								En erreur
							</button>
							<button
								type="button"
								onclick={() => showMachines('revoked')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(machineFilter === 'revoked')}`}
							>
								Révoquées
							</button>
						</div>
					</div>

					{#if deleteMachineSuccess}
						<div class="mb-4 rounded-[18px] border border-emerald-200 bg-emerald-50/80 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-500/10 dark:text-emerald-200">
							{deleteMachineSuccess}
						</div>
					{/if}

					{#if deleteMachineError}
						<div class="mb-4 rounded-[18px] border border-rose-200 bg-rose-50/80 px-4 py-3 text-sm text-rose-700 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200">
							{deleteMachineError}
						</div>
					{/if}

					<div class="grid gap-3">
						{#if filteredMachines.length > 0}
							{#each filteredMachines as machine}
								<article class="relative overflow-hidden rounded-[20px] border border-black/5 bg-black/[0.02] transition hover:bg-black/[0.03] dark:border-white/10 dark:bg-white/[0.03] dark:hover:bg-white/[0.05]">
									<a
										href={`/admin/machines/${machine.id}`}
										aria-label={`Ouvrir ${machine.hostname ?? `Machine #${machine.id}`}`}
										class="absolute inset-0 rounded-[20px]"
									></a>

									<div class="relative z-10 pointer-events-none flex items-start justify-between gap-4 p-4">
										<div class="min-w-0">
											<div class="text-sm font-semibold text-zinc-950 dark:text-white">
												{machine.hostname ?? `Machine #${machine.id}`}
											</div>

											<div class="mt-1 text-sm text-zinc-600 dark:text-zinc-300">
												{normalizeMachineStatus(machine.status)}
											</div>

											<div class="mt-2 text-xs text-zinc-500 dark:text-zinc-400">
												UUID : {machine.machine_uuid}
											</div>

											<div class="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
												Agent : {machine.agent_version ?? '-'}
											</div>

											<div class="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
												Dernier contact : {formatDateLabel(machine.last_seen_at)}
											</div>
										</div>

										<div class="flex shrink-0 flex-col items-end gap-3">
											<span
												class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${machineStatusClass(machine.status)}`}
											>
												{normalizeMachineStatus(machine.status)}
											</span>

											<form
												method="POST"
												action="?/deleteMachine"
												class="pointer-events-auto relative z-20"
												onsubmit={(event) => {
													const label = machine.hostname ?? `Machine #${machine.id}`;
													if (
														!confirm(
															`Supprimer définitivement ${label} ?\n\nCette action supprime la machine, ses jobs et leurs logs associés.\nElle ne retire pas simplement la carte de la liste.`
														)
													) {
														event.preventDefault();
													}
												}}
											>
												<input type="hidden" name="_csrf" value={csrfToken} />
												<input type="hidden" name="machine_id" value={machine.id} />
												<button
													type="submit"
													class="inline-flex items-center justify-center rounded-[12px] border border-rose-300 bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-700 shadow-sm transition hover:border-rose-400 hover:bg-rose-100 dark:border-rose-400/25 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/40 dark:hover:bg-rose-500/15"
												>
													Supprimer
												</button>
											</form>
										</div>
									</div>

									<div class="relative z-10 border-t border-rose-200/70 bg-rose-50/70 px-4 py-3 dark:border-rose-400/15 dark:bg-rose-500/[0.06]">
										<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-rose-700 dark:text-rose-300">
											Portée : machine complète
										</p>
										<p class="mt-1 text-xs leading-6 text-rose-700/90 dark:text-rose-200/90">
											Supprime définitivement la machine, ses jobs et leurs logs. Ce n’est pas un simple retrait visuel de la liste.
										</p>
									</div>
								</article>
							{/each}
						{:else}
							<div
								class="rounded-[22px] border border-dashed border-black/10 bg-black/[0.02] px-5 py-8 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.02] dark:text-zinc-400"
							>
								Aucune machine pour ce filtre.
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>

		<div
			bind:this={jobsSection}
			class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]"
		>
			<div class="relative">
				<div
					class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
				></div>

				<div class="relative p-6 sm:p-8">
					<div class="mb-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
						<div>
							<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
								{jobSectionTitle()}
							</h2>
							<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
								{jobSectionDescription()}
							</p>
						</div>

						<div class="flex flex-wrap gap-2">
							<button
								type="button"
								onclick={() => showJobs('all')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(jobFilter === 'all')}`}
							>
								Tous
							</button>
							<button
								type="button"
								onclick={() => showJobs('running')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(jobFilter === 'running')}`}
							>
								En cours
							</button>
							<button
								type="button"
								onclick={() => showJobs('failed')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(jobFilter === 'failed')}`}
							>
								Échec
							</button>
							<button
								type="button"
								onclick={() => showJobs('success')}
								class={`rounded-[12px] border px-3 py-2 text-sm font-medium transition ${filterButtonClass(jobFilter === 'success')}`}
							>
								Terminés
							</button>
						</div>
					</div>

					<div class="grid gap-3">
						{#if filteredJobs.length > 0}
							{#each filteredJobs as job}
								<a
									href={`/admin/jobs/${job.id}`}
									class="flex items-start justify-between gap-4 rounded-[20px] border border-black/5 bg-black/[0.02] p-4 transition hover:bg-black/[0.03] dark:border-white/10 dark:bg-white/[0.03] dark:hover:bg-white/[0.05]"
								>
									<div class="min-w-0">
										<div class="text-sm font-semibold text-zinc-950 dark:text-white">
											{job.type}
										</div>

										<div class="mt-1 text-sm text-zinc-600 dark:text-zinc-300">
											Machine #{job.machine_id}
										</div>

										<div class="mt-2 text-xs text-zinc-500 dark:text-zinc-400">
											Statut : {normalizeJobStatus(job.status)}
										</div>

										<div class="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
											Créé : {formatDateLabel(job.created_at)}
										</div>
									</div>

									<div class="flex shrink-0 items-center gap-3">
										<span
											class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${jobStatusClass(job.status)}`}
										>
											{normalizeJobStatus(job.status)}
										</span>
										<span class="text-sm font-medium text-sky-600 dark:text-sky-300">Voir</span>
									</div>
								</a>
							{/each}
						{:else}
							<div
								class="rounded-[22px] border border-dashed border-black/10 bg-black/[0.02] px-5 py-8 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.02] dark:text-zinc-400"
							>
								Aucun job pour ce filtre.
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>