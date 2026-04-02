<script lang="ts">
	import { onMount } from 'svelte';
	import { getBrowserWsUrl } from '$lib/public-config';

	let { data } = $props();

	let job = $state(data.job);
	let logs = $state(data.logs ?? []);

	const isFinished = () => job.status === 'completed' || job.status === 'failed';

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
			return 'border border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-500/20 dark:bg-blue-500/10 dark:text-blue-300';
		}
		return 'border border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
	}

	onMount(() => {
		if (isFinished()) return;

		const ws = new WebSocket(getBrowserWsUrl(`/ws/jobs/${job.id}`));

		ws.onmessage = (event) => {
			const payload = JSON.parse(event.data);

			if (payload.type === 'job_log' && payload.log) {
				logs = [...logs, payload.log];
			}

			if (payload.type === 'job_status') {
				job = {
					...job,
					status: payload.status ?? job.status,
					claimed_at: payload.claimed_at ?? job.claimed_at,
					completed_at: payload.completed_at ?? job.completed_at,
					result: payload.result ?? job.result,
					error_message: payload.error_message ?? job.error_message
				};

				if (isFinished()) {
					ws.close();
				}
			}
		};

		return () => {
			ws.close();
		};
	});
</script>

<svelte:head>
	<title>Suivi d’installation</title>
</svelte:head>

<section class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/applications"
						class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						← Retour aux applications
					</a>
				</p>

				<h1 class="mb-2 text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
					Suivi d’installation
				</h1>

				<div class="mb-6 rounded-[18px] border border-black/5 bg-white/70 px-4 py-4 text-sm text-zinc-700 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
					<div class="grid gap-3 sm:grid-cols-2">
						<div>
							<strong class="text-zinc-900 dark:text-zinc-100">Application :</strong>
							<span class="ml-2">{job.payload?.app_slug ?? '-'}</span>
						</div>

						<div>
							<strong class="text-zinc-900 dark:text-zinc-100">Sous-domaine :</strong>
							<span class="ml-2">{job.payload?.subdomain ?? '-'}</span>
						</div>

						<div>
							<strong class="text-zinc-900 dark:text-zinc-100">Authentification :</strong>
							<span class="ml-2">{job.payload?.auth_type ?? '-'}</span>
						</div>

						<div class="flex items-center gap-3">
							<strong class="text-zinc-900 dark:text-zinc-100">Statut :</strong>
							<span class={`rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(job.status)}`}>
								{humanStatus(job.status)}
							</span>
						</div>
					</div>
				</div>

				{#if !isFinished()}
					<p class="mb-5 text-sm text-zinc-500 dark:text-zinc-400">
						Connexion temps réel active…
					</p>
				{/if}

				{#if job.status === 'completed'}
					<div class="mb-5 rounded-[18px] border border-emerald-200 bg-emerald-50 px-4 py-4 text-sm text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
						L’installation est terminée avec succès.
					</div>
				{/if}

				{#if job.status === 'failed'}
					<div class="mb-5 rounded-[18px] border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
						L’installation a échoué.
					</div>
				{/if}

				<h2 class="mb-4 text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
					Journal d’installation
				</h2>

				{#if logs.length > 0}
					<div class="max-h-[500px] overflow-auto rounded-[20px] border border-black/5 bg-black/[0.03] p-4 font-mono text-[0.92rem] text-zinc-800 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)] dark:text-zinc-100">
						{#each logs as log}
							<div class="border-b border-black/[0.04] py-2 last:border-b-0 dark:border-white/[0.04]">
								<span class="mr-2 text-zinc-500 dark:text-zinc-500">[{log.level}]</span>
								<span>{log.message}</span>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-sm text-zinc-500 dark:text-zinc-400">
						Aucun log pour le moment.
					</p>
				{/if}
			</div>
		</div>
	</div>
</section>