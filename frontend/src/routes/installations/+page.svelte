<script lang="ts">
	let { data } = $props();

	const jobs = data.jobs ?? [];

	function humanStatus(status: string) {
		if (status === 'pending') return 'En attente';
		if (status === 'claimed') return 'Préparation';
		if (status === 'running') return 'En cours';
		if (status === 'completed') return 'Terminée';
		if (status === 'failed') return 'Échec';
		return status;
	}

	function statusClass(status: string) {
		if (status === 'completed') {
			return 'border border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
		}

		if (status === 'failed') {
			return 'border border-red-200 bg-red-50 text-red-600 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300';
		}

		if (status === 'running') {
			return 'border border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-500/20 dark:bg-cyan-500/10 dark:text-cyan-300';
		}

		if (status === 'claimed') {
			return 'border border-violet-200 bg-violet-50 text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300';
		}

		return 'border border-zinc-200 bg-zinc-100 text-zinc-600 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-300';
	}

	function appName(job: any) {
		return job?.payload?.app_name ?? job?.payload?.app_slug ?? 'Application';
	}

	function formatFrenchDate(value: string | null | undefined) {
		if (!value) return '-';

		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return value;

		return new Intl.DateTimeFormat('fr-FR', {
			day: '2-digit',
			month: 'long',
			year: 'numeric'
		}).format(date);
	}
</script>

<svelte:head>
	<title>Installations</title>
</svelte:head>

<section class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<div class="mb-6">
					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						Installations
					</div>

					<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Installations
					</h1>

					<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Suis l’avancement des installations lancées depuis l’App Store.
					</p>
				</div>

				{#if jobs.length > 0}
					<div class="grid gap-4">
						{#each jobs as job}
							<a
								href={`/installations/${job.id}`}
								class="group flex items-center justify-between gap-4 rounded-[22px] border border-black/5 bg-white/70 px-5 py-4 text-zinc-900 shadow-[0_10px_24px_rgba(15,23,42,0.05)] transition-all duration-200 hover:-translate-y-0.5 hover:border-black/10 hover:bg-white/80 hover:shadow-[0_14px_32px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-[rgba(15,23,42,0.55)] dark:text-white dark:shadow-none dark:hover:border-white/15 dark:hover:bg-[rgba(15,23,42,0.68)]"
							>
								<div class="min-w-0">
									<div class="truncate text-[15px] font-semibold tracking-[-0.02em] text-zinc-950 dark:text-white">
										{appName(job)}
									</div>

									<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
										{formatFrenchDate(job.created_at)}
									</div>
								</div>

								<div
									class={`shrink-0 rounded-full px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(job.status)}`}
								>
									{humanStatus(job.status)}
								</div>
							</a>
						{/each}
					</div>
				{:else}
					<div class="rounded-[22px] border border-black/5 bg-white/60 p-5 text-sm text-zinc-600 shadow-[0_10px_24px_rgba(15,23,42,0.05)] dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-none">
						Aucune installation pour le moment.
					</div>
				{/if}
			</div>
		</div>
	</div>
</section>