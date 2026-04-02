<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let { data } = $props();

	const job = data.job;
	const logs = data.logs ?? [];

	const isFinished = job.status === 'completed' || job.status === 'failed';

	function formatDate(value: string | null | undefined) {
		if (!value) return '-';

		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return value;

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(date);
	}

	function statusLabel(status: string) {
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

	function statusClass(status: string) {
		switch (status?.toLowerCase()) {
			case 'completed':
			case 'success':
			case 'done':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/10 dark:text-emerald-300';
			case 'running':
			case 'processing':
			case 'pending':
				return 'border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-400/15 dark:bg-cyan-500/10 dark:text-cyan-300';
			case 'failed':
			case 'error':
				return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/10 dark:text-rose-300';
			default:
				return 'border-zinc-200 bg-zinc-100 text-zinc-700 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-300';
		}
	}

	function logLevelClass(level: string) {
		switch (level?.toLowerCase()) {
			case 'error':
			case 'critical':
				return 'text-rose-700 dark:text-rose-300';
			case 'warning':
			case 'warn':
				return 'text-amber-700 dark:text-amber-300';
			case 'info':
				return 'text-cyan-700 dark:text-cyan-300';
			case 'debug':
				return 'text-zinc-600 dark:text-zinc-400';
			default:
				return 'text-zinc-700 dark:text-zinc-300';
		}
	}

	onMount(() => {
		if (!browser || isFinished) return;

		const interval = setInterval(async () => {
			await goto(window.location.pathname, {
				invalidateAll: true,
				noScroll: true,
				replaceState: true,
				keepFocus: true
			});
		}, 5000);

		return () => clearInterval(interval);
	});
</script>

<svelte:head>
	<title>Admin — Détail job</title>
</svelte:head>

<section class="relative isolate overflow-hidden">
	<div class="pointer-events-none absolute inset-0 -z-30 bg-[linear-gradient(180deg,#f8fafc_0%,#eef2ff_24%,#f8fafc_52%,#ecfeff_100%)] dark:bg-[linear-gradient(180deg,#050816_0%,#0b1020_38%,#0a1120_68%,#07111f_100%)]"></div>

	<div class="pointer-events-none absolute inset-0 -z-20 opacity-90">
		<div class="absolute left-[-8rem] top-[-7rem] h-[28rem] w-[28rem] rounded-full bg-cyan-400/18 blur-3xl dark:bg-cyan-400/14"></div>
		<div class="absolute right-[-10rem] top-[-5rem] h-[32rem] w-[32rem] rounded-full bg-fuchsia-400/14 blur-3xl dark:bg-fuchsia-500/12"></div>
		<div class="absolute bottom-[-12rem] left-[12%] h-[26rem] w-[26rem] rounded-full bg-emerald-400/14 blur-3xl dark:bg-emerald-400/10"></div>
	</div>

	<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<div class="relative overflow-hidden rounded-[34px] border border-black/5 bg-white/78 shadow-[0_28px_90px_rgba(15,23,42,0.10)] backdrop-blur-3xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_90px_rgba(0,0,0,0.36)]">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.88),rgba(255,255,255,0.62)_44%,rgba(255,255,255,0.50)_100%)] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.03)_44%,rgba(255,255,255,0.02)_100%)]"></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/admin"
						class="inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-2 text-sm font-medium text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.82)] transition hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.06]"
					>
						← Retour admin
					</a>
				</p>

				<div class="flex flex-col gap-6 xl:flex-row xl:items-start xl:justify-between">
					<div class="max-w-4xl">
						<div class="mb-4 flex flex-wrap items-center gap-3">
							<div class="inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/72 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
								<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
								Job admin
							</div>

							<span
								class={`inline-flex rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] ${statusClass(job.status)}`}
							>
								{statusLabel(job.status)}
							</span>
						</div>

						<h1 class="max-w-3xl text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50 sm:text-3xl xl:text-4xl">
							Détail du job
						</h1>

						<p class="mt-3 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
							Vue d’exploitation détaillée pour suivre l’exécution, analyser le résultat et
							inspecter les logs techniques.
						</p>
					</div>

					{#if !isFinished}
						<div class="w-full max-w-xl">
							<div class="rounded-[22px] border border-cyan-200 bg-cyan-50/80 px-4 py-4 text-sm text-cyan-700 shadow-[0_16px_40px_rgba(14,165,233,0.10)] dark:border-cyan-400/15 dark:bg-cyan-500/10 dark:text-cyan-300">
								Rafraîchissement automatique toutes les 5 secondes…
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<div class="mt-8 grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
			<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/72 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]">
				<div class="relative p-6 sm:p-8">
					<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
						Informations
					</h2>

					<div class="mt-5 grid gap-3">
						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">ID</span>
							<span class="max-w-[65%] break-all text-right text-sm font-semibold text-zinc-950 dark:text-white">{job.id}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Machine ID</span>
							<span class="max-w-[65%] break-all text-right text-sm font-semibold text-zinc-950 dark:text-white">{job.machine_id}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Type</span>
							<span class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-white">{job.type}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Statut</span>
							<span class={`inline-flex rounded-full border px-2.5 py-1 text-xs font-semibold ${statusClass(job.status)}`}>
								{statusLabel(job.status)}
							</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Claimed at</span>
							<span class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-white">{formatDate(job.claimed_at)}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Completed at</span>
							<span class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-white">{formatDate(job.completed_at)}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Created at</span>
							<span class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-white">{formatDate(job.created_at)}</span>
						</div>

						<div class="flex items-start justify-between gap-4 rounded-[18px] border border-black/5 bg-black/[0.02] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-sm text-zinc-500">Updated at</span>
							<span class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-white">{formatDate(job.updated_at)}</span>
						</div>
					</div>
				</div>
			</div>

			<div class="grid gap-6">
				<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/72 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]">
					<div class="relative p-6 sm:p-8">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Erreur
						</h2>

						<div class="mt-4 rounded-[20px] border border-black/5 bg-black/[0.03] p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)]">
							<pre class="m-0 whitespace-pre-wrap break-words font-mono text-sm leading-7 text-zinc-900 dark:text-zinc-100">{job.error_message ?? '-'}</pre>
						</div>
					</div>
				</div>

				<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/72 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]">
					<div class="relative p-6 sm:p-8">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Payload
						</h2>

						<div class="mt-4 rounded-[20px] border border-black/5 bg-black/[0.03] p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)]">
							<pre class="m-0 overflow-x-auto whitespace-pre-wrap break-words font-mono text-sm leading-7 text-zinc-900 dark:text-zinc-100">{JSON.stringify(job.payload, null, 2)}</pre>
						</div>
					</div>
				</div>

				<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/72 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]">
					<div class="relative p-6 sm:p-8">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Résultat
						</h2>

						<div class="mt-4 rounded-[20px] border border-black/5 bg-black/[0.03] p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)]">
							<pre class="m-0 overflow-x-auto whitespace-pre-wrap break-words font-mono text-sm leading-7 text-zinc-900 dark:text-zinc-100">{JSON.stringify(job.result, null, 2)}</pre>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="mt-8 overflow-hidden rounded-[30px] border border-black/5 bg-white/72 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035]">
			<div class="relative p-6 sm:p-8">
				<div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
					<div>
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
							Logs
						</h2>
						<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
							{logs.length} entrée(s) enregistrée(s) pour ce job.
						</p>
					</div>
				</div>

				{#if logs.length > 0}
					<div class="overflow-hidden rounded-[22px] border border-black/5 bg-black/[0.02] dark:border-white/10 dark:bg-white/[0.03]">
						<div class="overflow-x-auto">
							<table class="min-w-full border-collapse">
								<thead>
									<tr class="border-b border-black/5 dark:border-white/10">
										<th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Seq</th>
										<th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Level</th>
										<th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Message</th>
										<th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Created at</th>
									</tr>
								</thead>

								<tbody>
									{#each logs as log}
										<tr class="border-b border-black/5 align-top last:border-b-0 dark:border-white/10">
											<td class="px-4 py-3 text-sm font-semibold text-zinc-950 dark:text-white">
												{log.seq}
											</td>
											<td class="px-4 py-3">
												<span class={`text-sm font-semibold ${logLevelClass(log.level)}`}>
													{log.level}
												</span>
											</td>
											<td class="px-4 py-3 text-sm text-zinc-700 dark:text-zinc-200">
												{log.message}
											</td>
											<td class="px-4 py-3 text-sm text-zinc-500 dark:text-zinc-400">
												{formatDate(log.created_at)}
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{:else}
					<div class="rounded-[22px] border border-dashed border-black/10 bg-black/[0.02] px-5 py-8 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.02] dark:text-zinc-400">
						Aucun log pour ce job.
					</div>
				{/if}
			</div>
		</div>
	</div>
</section>