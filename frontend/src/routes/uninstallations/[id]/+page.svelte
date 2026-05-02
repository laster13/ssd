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
		if (status === 'running') return 'Suppression en cours';
		if (status === 'completed') return 'Suppression terminée';
		if (status === 'failed') return 'Échec';
		return status;
	}

	function statusClass(status: string) {
		if (status === 'completed') {
			return 'border border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
		}
		if (status === 'failed') {
			return 'border border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300';
		}
		if (status === 'running') {
			return 'border border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
		}
		if (status === 'claimed') {
			return 'border border-orange-200 bg-orange-50 text-orange-700 dark:border-orange-500/20 dark:bg-orange-500/10 dark:text-orange-300';
		}
		return 'border border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300';
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
	<title>Suivi de désinstallation</title>
</svelte:head>

<section class="relative isolate min-h-screen overflow-x-hidden bg-[linear-gradient(180deg,#f8fafc_0%,#eef6ff_38%,#f8fafc_100%)] dark:bg-[linear-gradient(180deg,#07111f_0%,#0a1324_38%,#07111f_100%)]">
	<div class="pointer-events-none absolute inset-0">
		<div class="absolute left-[-6rem] top-[-4rem] h-72 w-72 rounded-full bg-cyan-300/18 blur-3xl dark:bg-cyan-400/10"></div>
		<div class="absolute right-[-5rem] top-[-2rem] h-80 w-80 rounded-full bg-emerald-300/16 blur-3xl dark:bg-emerald-400/10"></div>
	</div>

	<section class="mx-auto max-w-5xl py-8 sm:px-6 lg:px-8">
		<div class="border-y border-black/5 bg-white/78 backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.035] sm:overflow-hidden sm:rounded-[30px] sm:border sm:shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:sm:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.84),rgba(255,255,255,0.58))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"></div>

				<div class="relative px-4 py-6 sm:p-8">
					<p class="mb-5">
						<a
							href="/applications"
							class="text-sm font-medium text-orange-600 no-underline transition hover:text-orange-700 dark:text-orange-300 dark:hover:text-orange-200"
						>
							← Retour aux applications
						</a>
					</p>

					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-orange-200 bg-orange-50/90 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.18em] text-orange-700 dark:border-orange-400/20 dark:bg-orange-500/10 dark:text-orange-200">
						<span class="h-1.5 w-1.5 rounded-full bg-orange-500 dark:bg-orange-400"></span>
						Désinstallation
					</div>

					<h1 class="mb-2 break-words text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Suivi de désinstallation
					</h1>

					<p class="mb-6 text-sm text-zinc-600 dark:text-zinc-400">
						Suivi en temps réel de la suppression de ton application.
					</p>

					<div class="mb-6 border-y border-black/5 bg-white/78 px-4 py-5 text-sm text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300 sm:rounded-[22px] sm:border">
						<div class="grid gap-4 sm:grid-cols-2">
							<div>
								<strong class="text-zinc-900 dark:text-zinc-100">Application :</strong>
								<span class="ml-2">{job.payload?.app_name ?? job.payload?.app_slug ?? '-'}</span>
							</div>

							<div>
								<strong class="text-zinc-900 dark:text-zinc-100">Slug :</strong>
								<span class="ml-2">{job.payload?.app_slug ?? '-'}</span>
							</div>

							<div class="flex items-center gap-3 sm:col-span-2">
								<strong class="text-zinc-900 dark:text-zinc-100">Statut :</strong>
								<span class={`rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(job.status)}`}>
									{humanStatus(job.status)}
								</span>
							</div>
						</div>
					</div>

					{#if !isFinished()}
						<div class="mb-5 border-y border-orange-200 bg-orange-50/80 px-4 py-4 text-sm text-orange-700 dark:border-orange-500/20 dark:bg-orange-500/10 dark:text-orange-300 sm:rounded-[18px] sm:border">
							Connexion temps réel active…
						</div>
					{/if}

					{#if job.status === 'completed'}
						<div class="mb-5 border-y border-emerald-200 bg-emerald-50 px-4 py-4 text-sm text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300 sm:rounded-[18px] sm:border">
							La désinstallation est terminée avec succès.
						</div>
					{/if}

					{#if job.status === 'failed'}
						<div class="mb-5 border-y border-rose-200 bg-rose-50 px-4 py-4 text-sm text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300 sm:rounded-[18px] sm:border">
							La désinstallation a échoué.
						</div>
					{/if}

					<h2 class="mb-4 text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
						Journal de désinstallation
					</h2>

					{#if logs.length > 0}
						<div class="max-h-[500px] overflow-auto border-y border-zinc-200 bg-zinc-50 p-4 font-mono text-[0.92rem] text-zinc-800 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-100 sm:rounded-[22px] sm:border">
							{#each logs as log}
								<div class="border-b border-zinc-200 py-2 last:border-b-0 dark:border-zinc-800">
									<span class="mr-2 text-zinc-500 dark:text-zinc-400">[{log.level}]</span>
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
</section>