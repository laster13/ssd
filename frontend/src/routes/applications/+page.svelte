<script lang="ts">
	let { data } = $props();

	type Job = {
		id: string;
		machine_id: string;
		status: string;
		created_at?: string;
		updated_at?: string;
		payload?: {
			app_slug?: string;
		};
	};

	type Machine = {
		id: string;
		hostname?: string;
		machine_uuid?: string;
		status?: string;
	};

	const jobs = $derived((data.jobs ?? []) as Job[]);
	const machines = $derived((data.machines ?? []) as Machine[]);
	const machineById = $derived(new Map(machines.map((machine) => [machine.id, machine])));

	function formatDate(value?: string) {
		if (!value) return '—';

		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return value;

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(date);
	}

	function humanStatus(status: string) {
		switch (status) {
			case 'pending':
				return 'En attente';
			case 'claimed':
				return 'Prise en charge';
			case 'running':
				return 'Déploiement';
			case 'completed':
				return 'En ligne';
			case 'failed':
				return 'Incident';
			default:
				return status;
		}
	}

	function machineStatusLabel(status?: string) {
		switch (status) {
			case 'online':
				return 'En ligne';
			case 'offline':
				return 'Hors ligne';
			case 'provisioning':
				return 'Provisionnement';
			case 'maintenance':
				return 'Maintenance';
			default:
				return status || 'Inconnu';
		}
	}

	function statusClass(status: string) {
		switch (status) {
			case 'completed':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/8 dark:text-emerald-300';
			case 'failed':
				return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/8 dark:text-rose-300';
			case 'running':
				return 'border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-400/15 dark:bg-cyan-500/8 dark:text-cyan-300';
			case 'claimed':
				return 'border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/15 dark:bg-indigo-500/8 dark:text-indigo-300';
			default:
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/15 dark:bg-amber-500/8 dark:text-amber-300';
		}
	}

	function statusDotClass(status: string) {
		switch (status) {
			case 'completed':
				return 'bg-emerald-500 dark:bg-emerald-400';
			case 'failed':
				return 'bg-rose-500 dark:bg-rose-400';
			case 'running':
				return 'bg-cyan-500 dark:bg-cyan-400';
			case 'claimed':
				return 'bg-indigo-500 dark:bg-indigo-400';
			default:
				return 'bg-amber-500 dark:bg-amber-400';
		}
	}

	function machinePillClass(status?: string) {
		switch (status) {
			case 'online':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/8 dark:text-emerald-300';
			case 'offline':
				return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/8 dark:text-rose-300';
			case 'maintenance':
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/15 dark:bg-amber-500/8 dark:text-amber-300';
			default:
				return 'border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300';
		}
	}

	const appItems = $derived.by(() => {
		const seen = new Set<string>();
		const items: Array<{
			key: string;
			jobId: string;
			appSlug: string;
			status: string;
			createdAt?: string;
			updatedAt?: string;
			machineName: string;
			machineStatus: string;
		}> = [];

		for (const job of jobs) {
			const payload = job.payload ?? {};
			const appSlug = payload.app_slug ?? 'unknown';
			const key = `${job.machine_id}:${appSlug}`;

			if (seen.has(key)) continue;
			seen.add(key);

			const machine = machineById.get(job.machine_id);

			items.push({
				key,
				jobId: job.id,
				appSlug,
				status: job.status,
				createdAt: job.created_at,
				updatedAt: job.updated_at,
				machineName: machine?.hostname || machine?.machine_uuid || 'Serveur inconnu',
				machineStatus: machine?.status || 'unknown'
			});
		}

		return items.sort((a, b) => {
			const aTime = a.updatedAt ? new Date(a.updatedAt).getTime() : 0;
			const bTime = b.updatedAt ? new Date(b.updatedAt).getTime() : 0;
			return bTime - aTime;
		});
	});

	const stats = $derived.by(() => ({
		total: appItems.length,
		running: appItems.filter((item) => ['pending', 'claimed', 'running'].includes(item.status)).length,
		failed: appItems.filter((item) => item.status === 'failed').length,
		completed: appItems.filter((item) => item.status === 'completed').length
	}));

	const spotlight = $derived.by(() => {
		return (
			appItems.find((item) => item.status === 'running') ||
			appItems.find((item) => item.status === 'claimed') ||
			appItems.find((item) => item.status === 'pending') ||
			appItems[0]
		);
	});
</script>

<svelte:head>
	<title>Mes applications</title>
</svelte:head>

<section class="relative isolate overflow-hidden">
	<div class="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.08),transparent_26%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.08),transparent_24%),linear-gradient(180deg,rgba(248,250,252,1)_0%,rgba(241,245,249,0.92)_100%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(16,185,129,0.12),transparent_26%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.10),transparent_22%),linear-gradient(180deg,#09090b_0%,#111827_100%)]"></div>
	<div class="pointer-events-none absolute inset-x-0 top-0 -z-10 h-px bg-gradient-to-r from-transparent via-black/10 to-transparent dark:via-white/12"></div>

	<div class="mx-auto max-w-7xl px-4 pb-8 pt-8 sm:px-6 lg:px-8 lg:pt-12">
		<div class="relative overflow-hidden rounded-[34px] border border-black/5 bg-white/80 p-6 shadow-[0_25px_80px_rgba(15,23,42,0.08)] backdrop-blur-2xl dark:border-white/8 dark:bg-white/[0.03] dark:shadow-[0_24px_70px_rgba(0,0,0,0.34)] sm:p-8 lg:p-10">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.84),rgba(255,255,255,0.56))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.04),rgba(255,255,255,0.015))]"></div>
			<div class="pointer-events-none absolute -left-24 top-0 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl dark:bg-emerald-400/10"></div>
			<div class="pointer-events-none absolute right-[-40px] top-[-30px] h-72 w-72 rounded-full bg-sky-400/10 blur-3xl dark:bg-sky-400/8"></div>

			<div class="relative grid gap-8 xl:grid-cols-[minmax(0,1.15fr)_420px] xl:items-center">
				<div>
					<div class="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3.5 py-2 text-[11px] font-semibold uppercase tracking-[0.24em] text-emerald-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/8 dark:bg-white/[0.05] dark:text-emerald-200">
						<span class="inline-block h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_14px_rgba(16,185,129,0.45)] dark:bg-emerald-400 dark:shadow-[0_0_12px_rgba(52,211,153,0.6)]"></span>
						Mes applications
					</div>

					<h1 class="max-w-4xl text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-2xl lg:text-3xl xl:text-[2.2rem]">						
						<span class="bg-[linear-gradient(90deg,#0f172a_0%,#059669_30%,#0284c7_65%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_25%,#93c5fd_58%,#d8b4fe_100%)]">
							Pilote tes applications
						</span>
					</h1>

					<p class="mt-5 max-w-3xl text-base leading-8 text-zinc-600 dark:text-zinc-300 sm:text-lg">
						Une vue élégante, claire et crédible pour suivre chaque application déployée par serveur, sans faux indicateurs ni éléments décoratifs trompeurs.
					</p>

					<div class="mt-8 grid gap-3 sm:grid-cols-4">
						<div class="rounded-[22px] border border-black/5 bg-white/75 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.75)] dark:border-white/8 dark:bg-white/[0.035]">
							<div class="text-xs uppercase tracking-[0.22em] text-zinc-500">Total</div>
							<div class="mt-3 text-3xl font-bold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">{stats.total}</div>
							<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Applications distinctes</div>
						</div>

						<div class="rounded-[22px] border border-cyan-200 bg-cyan-50/80 p-4 shadow-[0_12px_30px_rgba(14,165,233,0.08)] dark:border-cyan-400/12 dark:bg-cyan-500/[0.06] dark:shadow-none">
							<div class="text-xs uppercase tracking-[0.22em] text-cyan-700 dark:text-cyan-200/80">En cours</div>
							<div class="mt-3 text-3xl font-bold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">{stats.running}</div>
							<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">En attente ou déploiement</div>
						</div>

						<div class="rounded-[22px] border border-emerald-200 bg-emerald-50/80 p-4 shadow-[0_12px_30px_rgba(16,185,129,0.08)] dark:border-emerald-400/12 dark:bg-emerald-500/[0.06] dark:shadow-none">
							<div class="text-xs uppercase tracking-[0.22em] text-emerald-700 dark:text-emerald-200/80">En ligne</div>
							<div class="mt-3 text-3xl font-bold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">{stats.completed}</div>
							<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Terminées avec succès</div>
						</div>

						<div class="rounded-[22px] border border-rose-200 bg-rose-50/80 p-4 shadow-[0_12px_30px_rgba(244,63,94,0.08)] dark:border-rose-400/12 dark:bg-rose-500/[0.06] dark:shadow-none">
							<div class="text-xs uppercase tracking-[0.22em] text-rose-700 dark:text-rose-200/80">Incidents</div>
							<div class="mt-3 text-3xl font-bold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">{stats.failed}</div>
							<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Déploiements en échec</div>
						</div>
					</div>
				</div>

				<div class="relative overflow-hidden rounded-[28px] border border-black/5 bg-white/78 p-5 shadow-[0_20px_50px_rgba(15,23,42,0.08)] dark:border-white/8 dark:bg-zinc-950/72 dark:shadow-[0_20px_50px_rgba(0,0,0,0.30)]">
					<div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.72),transparent_56%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.04),transparent_50%)]"></div>
					<div class="relative">
						<div class="flex items-center justify-between gap-3">

							{#if spotlight}
								<div class={`rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.15em] ${statusClass(spotlight.status)}`}>
									{humanStatus(spotlight.status)}
								</div>
							{/if}
						</div>

						{#if spotlight}
							<div class="mt-5 space-y-4">
								<div class="rounded-[20px] border border-black/5 bg-white/82 p-4 dark:border-white/8 dark:bg-white/[0.03]">
									<div class="mb-3 flex items-center justify-between gap-3">
										<span class="text-sm text-zinc-500 dark:text-zinc-400">Serveur</span>
										<span class={`rounded-full border px-2.5 py-1 text-[11px] font-medium ${machinePillClass(spotlight.machineStatus)}`}>
											{machineStatusLabel(spotlight.machineStatus)}
										</span>
									</div>
									<div class="text-base font-semibold text-zinc-950 dark:text-zinc-100">{spotlight.machineName}</div>
								</div>

								<div class="grid grid-cols-2 gap-3">
									<div class="rounded-[20px] border border-black/5 bg-white/82 p-4 dark:border-white/8 dark:bg-white/[0.03]">
										<div class="text-xs uppercase tracking-[0.2em] text-zinc-500">Créée le</div>
										<div class="mt-2 text-sm font-semibold text-zinc-950 dark:text-zinc-100">{formatDate(spotlight.createdAt)}</div>
									</div>

									<div class="rounded-[20px] border border-black/5 bg-white/82 p-4 dark:border-white/8 dark:bg-white/[0.03]">
										<div class="text-xs uppercase tracking-[0.2em] text-zinc-500">Dernière activité</div>
										<div class="mt-2 text-sm font-semibold text-zinc-950 dark:text-zinc-100">{formatDate(spotlight.updatedAt)}</div>
									</div>
								</div>
							</div>
						{:else}
							<div class="mt-5 rounded-[22px] border border-dashed border-black/10 bg-white/70 p-6 text-sm text-zinc-500 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400">
								Aucune application n’est encore déployée.
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<section class="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
	{#if appItems.length > 0}
		<div class="mb-5 flex items-center justify-between gap-3">
			<div>
				<h2 class="text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50 sm:text-3xl">Inventaire des applications</h2>
				<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Des cartes lisibles, utiles et cohérentes, avec uniquement les informations qui comptent.</p>
			</div>
			<div class="hidden rounded-full border border-black/5 bg-white/80 px-4 py-2 text-xs uppercase tracking-[0.2em] text-zinc-500 dark:border-white/8 dark:bg-white/[0.04] dark:text-zinc-400 md:block">
				Triées par activité récente
			</div>
		</div>

		<div class="grid grid-cols-1 gap-5 md:grid-cols-2 2xl:grid-cols-3">
			{#each appItems as item}
				<article class="group relative overflow-hidden rounded-[28px] border border-black/5 bg-white/88 p-5 shadow-[0_18px_45px_rgba(15,23,42,0.08)] backdrop-blur-xl transition duration-300 hover:-translate-y-1 hover:border-black/10 hover:shadow-[0_24px_55px_rgba(15,23,42,0.12)] dark:border-white/8 dark:bg-zinc-950/78 dark:shadow-[0_20px_50px_rgba(0,0,0,0.32)] dark:hover:border-white/12 dark:hover:bg-zinc-950/84 dark:hover:shadow-[0_24px_60px_rgba(0,0,0,0.38)]">
					<div class="pointer-events-none absolute inset-0 opacity-0 transition duration-300 group-hover:opacity-100 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.06),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(16,185,129,0.06),transparent_30%)] dark:bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.035),transparent_24%)]"></div>

					<div class="relative">
						<div class="mb-5 flex items-start justify-between gap-4">
							<div class="min-w-0">
								<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-black/5 bg-zinc-50 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-500">
									<span class={`h-2 w-2 rounded-full ${statusDotClass(item.status)}`}></span>
									Statut
								</div>
								<h3 class="truncate text-[1.18rem] font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-[1.28rem]">
									{item.appSlug}
								</h3>
								<p class="mt-1 truncate text-sm text-zinc-500 dark:text-zinc-400">Déployée sur {item.machineName}</p>
							</div>

							<div class={`shrink-0 rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] ${statusClass(item.status)}`}>
								{humanStatus(item.status)}
							</div>
						</div>

						<div class="rounded-[20px] border border-black/5 bg-zinc-50/80 p-4 dark:border-white/10 dark:bg-white/[0.03]">
							<div class="mb-3 flex items-center justify-between gap-3">
								<span class="text-xs uppercase tracking-[0.2em] text-zinc-500 dark:text-zinc-500">Détails</span>
								<span class={`rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] ${machinePillClass(item.machineStatus)}`}>
									{machineStatusLabel(item.machineStatus)}
								</span>
							</div>

							<dl class="space-y-3">
								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Serveur</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">{item.machineName}</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">État machine</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">{machineStatusLabel(item.machineStatus)}</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Créée le</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">{formatDate(item.createdAt)}</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Dernière mise à jour</dt>
									<dd class="max-w-[60%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">{formatDate(item.updatedAt)}</dd>
								</div>
							</dl>
						</div>

						<div class="mt-5 flex items-center gap-3">
							<a
								href={`/installations/${item.jobId}`}
								class="inline-flex flex-1 items-center justify-center gap-2 rounded-[18px] border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.96),rgba(37,99,235,0.96))] px-4 py-3 text-sm font-semibold text-white shadow-[0_14px_30px_rgba(37,99,235,0.22)] transition duration-200 hover:scale-[1.01] hover:shadow-[0_18px_38px_rgba(37,99,235,0.28)] dark:border-cyan-400/12 dark:bg-[linear-gradient(135deg,rgba(8,145,178,0.95),rgba(37,99,235,0.92))] dark:shadow-[0_14px_28px_rgba(0,0,0,0.28)] dark:hover:shadow-[0_18px_36px_rgba(0,0,0,0.34)]"
							>
								Voir les logs
							</a>

							<a
								href={`/installations/new?app=${encodeURIComponent(item.appSlug)}`}
								class="inline-flex items-center justify-center rounded-[18px] border border-black/5 bg-white px-4 py-3 text-sm font-medium text-zinc-700 transition hover:border-black/10 hover:bg-zinc-50 hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.06] dark:hover:text-zinc-50"
							>
								Réinstaller
							</a>
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="relative overflow-hidden rounded-[30px] border border-black/5 bg-white/80 p-8 shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur-xl dark:border-white/8 dark:bg-white/[0.03] dark:shadow-[0_20px_60px_rgba(0,0,0,0.28)]">
			<div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(14,165,233,0.08),transparent_32%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.08),transparent_30%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.04),transparent_32%)]"></div>
			<div class="relative mx-auto max-w-xl text-center">
				<div class="mx-auto flex h-16 w-16 items-center justify-center rounded-[22px] border border-black/5 bg-white text-2xl shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/8 dark:bg-white/[0.04] dark:shadow-none">
					✦
				</div>
				<h2 class="mt-5 text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">Aucune application lancée</h2>
				<p class="mt-3 text-base leading-7 text-zinc-600 dark:text-zinc-400">
					Ton espace est prêt pour accueillir un premier déploiement. Lance une app depuis l’App Store pour remplir ce tableau de bord premium.
				</p>
				<a
					href="/app-store"
					class="mt-6 inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.95),rgba(59,130,246,0.95))] px-5 py-3 text-sm font-semibold text-white shadow-[0_16px_40px_rgba(37,99,235,0.20)] transition hover:scale-[1.01] dark:border-cyan-400/12 dark:shadow-[0_16px_32px_rgba(0,0,0,0.30)]"
				>
					Ouvrir l’App Store
				</a>
			</div>
		</div>
	{/if}
</section>