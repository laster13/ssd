<script lang="ts">
	import { onMount } from 'svelte';
	import type { Machine } from '$lib/utils/jobs';
	import {
		formatFrenchDateTime,
		machinePillClass,
		machineStatusLabel,
		resolveMachineConnectionStatus
	} from '$lib/utils/jobs';

	let { data, form } = $props();

	function isPairedMachine(machine: unknown): machine is Machine {
		return String((machine as Machine | undefined)?.status ?? '')
			.trim()
			.toLowerCase() === 'paired';
	}

	let servers = $state(
		((Array.isArray(data.machines) ? data.machines : []) as Machine[]).filter(isPairedMachine)
	);

	const machineSocketUrl = $derived((data.machineSocketUrl ?? '') as string);

	const AGENT_PURGE_COMMAND =
		"sudo bash -lc 'systemctl stop ssd-agent 2>/dev/null || true; systemctl disable ssd-agent 2>/dev/null || true; rm -f /etc/systemd/system/ssd-agent.service; systemctl daemon-reload; systemctl reset-failed; rm -rf /opt/ssd-agent'";

	let copyState = $state<'idle' | 'success' | 'error'>('idle');
	let copyTimer: ReturnType<typeof setTimeout> | null = null;

	function shortUuid(value: unknown) {
		const str = String(value ?? '');
		return str ? `${str.slice(0, 8)}…` : '-';
	}

	async function copyPurgeCommand() {
		try {
			await navigator.clipboard.writeText(AGENT_PURGE_COMMAND);
			copyState = 'success';
		} catch {
			copyState = 'error';
		}

		if (copyTimer) clearTimeout(copyTimer);
		copyTimer = setTimeout(() => {
			copyState = 'idle';
		}, 2200);
	}

	function applyMachineSocketPayload(payload: any) {
		if (!payload || typeof payload !== 'object') return;

		if (payload.type === 'machine_snapshot' && Array.isArray(payload.machines)) {
			servers = (payload.machines as Machine[]).filter(isPairedMachine);
			return;
		}

		if (payload.type === 'machine_presence' && payload.machine) {
			const incoming = payload.machine as Machine;

			if (!isPairedMachine(incoming)) {
				servers = servers.filter((item) => item.id !== incoming.id);
				return;
			}

			const index = servers.findIndex((item) => item.id === incoming.id);

			if (index === -1) {
				servers = [incoming, ...servers];
				return;
			}

			servers = servers.map((item) => (item.id === incoming.id ? { ...item, ...incoming } : item));
			return;
		}

		if (payload.type === 'machine_removed' && payload.machine_id) {
			servers = servers.filter((item) => item.id !== payload.machine_id);
		}
	}

	onMount(() => {
		if (!machineSocketUrl) return;

		let socket: WebSocket | null = null;
		let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
		let disposed = false;

		function scheduleReconnect() {
			if (disposed || reconnectTimer) return;
			reconnectTimer = setTimeout(() => {
				reconnectTimer = null;
				connectMachineSocket();
			}, 2000);
		}

		function connectMachineSocket() {
			if (disposed) return;

			socket = new WebSocket(machineSocketUrl);

			socket.onmessage = (event) => {
				try {
					applyMachineSocketPayload(JSON.parse(event.data));
				} catch {
					// noop
				}
			};

			socket.onclose = () => {
				socket = null;
				scheduleReconnect();
			};

			socket.onerror = () => {
				socket?.close();
			};
		}

		connectMachineSocket();

		return () => {
			disposed = true;
			if (reconnectTimer) clearTimeout(reconnectTimer);
			if (copyTimer) clearTimeout(copyTimer);
			socket?.close();
		};
	});

	function connectionBadgeFor(server: Machine) {
		const status = resolveMachineConnectionStatus(server);
		return {
			status,
			label: machineStatusLabel(status),
			className: machinePillClass(status),
			dot: status === 'online' ? 'bg-emerald-500' : 'bg-rose-500'
		};
	}
</script>

<svelte:head>
	<title>Mes serveurs</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_22%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.16),transparent_20%),radial-gradient(circle_at_bottom,rgba(168,85,247,0.12),transparent_26%)]"></div>
	<div class="absolute left-[-12rem] top-[-10rem] -z-10 h-[26rem] w-[26rem] rounded-full bg-cyan-400/10 blur-3xl"></div>
	<div class="absolute right-[-10rem] top-[4rem] -z-10 h-[24rem] w-[24rem] rounded-full bg-blue-500/10 blur-3xl"></div>
	<div class="absolute bottom-[-10rem] left-1/2 -z-10 h-[22rem] w-[22rem] -translate-x-1/2 rounded-full bg-fuchsia-500/10 blur-3xl"></div>

	<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<header class="mb-8 overflow-hidden rounded-[36px] border border-black/5 bg-white/80 shadow-[0_35px_120px_rgba(15,23,42,0.12)] backdrop-blur dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_35px_120px_rgba(0,0,0,0.36)]">
			<div class="relative p-6 sm:p-8 lg:p-10">
				<div class="absolute inset-0 bg-[linear-gradient(135deg,rgba(6,182,212,0.08),rgba(37,99,235,0.06),rgba(139,92,246,0.08))]"></div>

				<div class="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
					<div class="max-w-3xl">
						<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50/90 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.18em] text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-300">
							<span class="h-2 w-2 rounded-full bg-cyan-500"></span>
							Servers
						</div>

						<h1 class="text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white sm:text-3xl xl:text-[2.4rem]">
							Gestion des serveurs
						</h1>

						<p class="mt-4 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
							Connecte, surveille et administre tes serveurs depuis le dashboard avec une vue claire de leur état, de l’agent installé et du dernier contact remonté en temps réel.
						</p>
					</div>

					<div class="flex flex-col gap-3 sm:flex-row">
						<a
							href="/install"
							class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_28px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white"
						>
							Installer SSD en local
						</a>

						<a
							href="/servers/add"
							class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_16px_38px_rgba(37,99,235,0.28)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_22px_48px_rgba(37,99,235,0.34)] dark:border-white/10"
						>
							Connecter un serveur
						</a>
					</div>
				</div>
			</div>
		</header>

		{#if form?.success}
			<div class="mb-6 rounded-[22px] border border-emerald-200 bg-emerald-50 px-4 py-4 text-sm font-medium text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
				Le serveur a bien été désappairé du dashboard.
			</div>
		{/if}

		{#if form?.error}
			<div class="mb-6 rounded-[22px] border border-red-200 bg-red-50 px-4 py-4 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
				{form.error}
			</div>
		{/if}

		<div class="mb-8 grid grid-cols-1 gap-6 xl:grid-cols-2">
			<div class="group relative overflow-hidden rounded-[34px] border border-black/5 bg-white/80 p-6 shadow-[0_24px_70px_rgba(15,23,42,0.10)] backdrop-blur transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_32px_90px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_24px_70px_rgba(0,0,0,0.28)]">
				<div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(6,182,212,0.18),transparent_40%),linear-gradient(135deg,rgba(255,255,255,0.40),transparent_55%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(6,182,212,0.18),transparent_40%),linear-gradient(135deg,rgba(255,255,255,0.03),transparent_55%)]"></div>
				<div class="absolute right-[-2rem] top-[-2rem] h-28 w-28 rounded-full bg-cyan-400/15 blur-2xl"></div>

				<div class="relative">
					<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-300">
						<span class="h-2 w-2 rounded-full bg-cyan-500"></span>
						Dashboard
					</div>

					<h2 class="text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
						Désappairer un serveur
					</h2>

					<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
						Le bouton <span class="font-semibold text-zinc-900 dark:text-zinc-100">Désappairer</span> retire le serveur de cette interface et coupe son association avec ton compte, sans forcément supprimer les fichiers présents sur la machine.
					</p>

					<div class="mt-5 rounded-[24px] border border-cyan-200/60 bg-cyan-50/80 p-4 dark:border-cyan-400/15 dark:bg-cyan-400/10">
						<div class="flex items-start gap-3">
							<div class="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-white text-cyan-600 shadow-[0_10px_24px_rgba(6,182,212,0.18)] dark:bg-white/10 dark:text-cyan-300">
								✦
							</div>
							<div>
								<p class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
									À retenir
								</p>
								<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
									Désappairer agit sur le lien entre le dashboard et le serveur. Cela ne constitue pas une désinstallation complète de l’agent côté machine.
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="group relative overflow-hidden rounded-[34px] border border-black/5 bg-white/80 p-6 shadow-[0_24px_70px_rgba(15,23,42,0.10)] backdrop-blur transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_32px_90px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_24px_70px_rgba(0,0,0,0.28)]">
				<div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(249,115,22,0.18),transparent_38%),linear-gradient(135deg,rgba(255,255,255,0.40),transparent_55%)] dark:bg-[radial-gradient(circle_at_top_right,rgba(249,115,22,0.16),transparent_38%),linear-gradient(135deg,rgba(255,255,255,0.03),transparent_55%)]"></div>
				<div class="absolute left-[-1rem] bottom-[-2rem] h-28 w-28 rounded-full bg-orange-400/15 blur-2xl"></div>

				<div class="relative">
					<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300">
						<span class="h-2 w-2 rounded-full bg-amber-500"></span>
						Suppression complète
					</div>

					<h2 class="text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
						Retirer totalement l’agent du serveur
					</h2>

					<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
						Si tu veux supprimer le service systemd, les fichiers de l’agent et le dossier d’installation sur le serveur cible, exécute cette commande directement sur la machine concernée.
					</p>

					<div class="mt-5 overflow-hidden rounded-[24px] border border-black/5 bg-zinc-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] dark:border-white/10">
						<div class="flex items-center justify-between border-b border-white/10 px-4 py-3">
							<div class="flex items-center gap-2">
								<span class="h-2.5 w-2.5 rounded-full bg-red-400"></span>
								<span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
								<span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
							</div>
							<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Shell</span>
						</div>

						<div class="overflow-x-auto px-4 py-4">
							<pre class="whitespace-pre-wrap break-all font-mono text-[13px] leading-6 text-zinc-100">{AGENT_PURGE_COMMAND}</pre>
						</div>
					</div>

					<div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
						<p class="text-xs leading-6 text-zinc-500 dark:text-zinc-400">
							Cette commande supprime complètement l’agent SSD du serveur cible.
						</p>

						<button
							type="button"
							onclick={copyPurgeCommand}
							class="inline-flex items-center justify-center rounded-[16px] border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-900 shadow-[0_10px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_14px_30px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white"
						>
							{#if copyState === 'success'}
								Commande copiée
							{:else if copyState === 'error'}
								Copie impossible
							{:else}
								Copier la commande
							{/if}
						</button>
					</div>
				</div>
			</div>
		</div>

		{#if servers.length > 0}
			<div class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
				{#each servers as server}
					{@const badge = connectionBadgeFor(server)}

					<article class="group overflow-hidden rounded-[30px] border border-black/5 bg-white/75 shadow-[0_18px_48px_rgba(15,23,42,0.08)] ring-1 ring-inset ring-black/[0.03] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(15,23,42,0.12)] dark:border-white/10 dark:bg-white/[0.045] dark:ring-white/[0.04] dark:shadow-[0_18px_48px_rgba(0,0,0,0.24)]">
						<div class="h-1.5 bg-[linear-gradient(90deg,#06b6d4,#2563eb,#8b5cf6)]"></div>

						<div class="p-5">
							<div class="mb-5 flex items-start justify-between gap-3">
								<div class="min-w-0">
									<h2 class="truncate text-[1.1rem] font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
										{server.hostname ?? 'Serveur sans nom'}
									</h2>

									<div class="mt-1 flex flex-wrap items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400">
										<span class="truncate">{server.machine_uuid}</span>
										<span class="rounded-full border border-black/8 bg-black/[0.03] px-2 py-0.5 text-[11px] font-medium text-zinc-600 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
											{shortUuid(server.machine_uuid)}
										</span>
									</div>
								</div>

								<div class={`inline-flex shrink-0 items-center gap-2 rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.12em] ${badge.className}`}>
									<span class={`h-2 w-2 rounded-full ${badge.dot}`}></span>
									{badge.label}
								</div>
							</div>

							<div class="grid gap-3 text-sm text-zinc-700 dark:text-zinc-300">
								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">Appairage</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">{server.status ?? '-'}</span>
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">Agent</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">{server.agent_version ?? '-'}</span>
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">SSD</span>
									<span class={server.ssdv2_installed ? 'font-semibold text-emerald-600 dark:text-emerald-400' : 'font-semibold text-amber-600 dark:text-amber-400'}>
										{server.ssdv2_installed ? 'Installé' : 'Non installé'}
									</span>
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">Dernier contact</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">{formatFrenchDateTime(server.last_seen_at)}</span>
								</div>
							</div>

							<div class="mt-5 flex items-center justify-between gap-3 border-t border-black/5 pt-4 dark:border-white/5">
								<a
									href={`/servers/${server.id}`}
									class="inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-4 py-2.5 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.18)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.24)] dark:border-white/10"
								>
									Voir le serveur
								</a>

								<form
									method="POST"
									action="?/delete"
									onsubmit={(event) => {
										if (!confirm(`Désappairer le serveur "${server.hostname ?? server.machine_uuid}" ?`)) {
											event.preventDefault();
										}
									}}
								>
									<input type="hidden" name="_csrf" value={data.csrfToken} />
									<input type="hidden" name="machine_id" value={server.id} />
									<button
										type="submit"
										class="inline-flex items-center justify-center rounded-[16px] border border-rose-200 bg-rose-50 px-4 py-2.5 text-sm font-semibold text-rose-700 transition hover:border-rose-300 hover:bg-rose-100 dark:border-rose-400/20 dark:bg-rose-500/10 dark:text-rose-200 dark:hover:border-rose-400/30 dark:hover:bg-rose-500/15"
									>
										Désappairer
									</button>
								</form>
							</div>
						</div>
					</article>
				{/each}
			</div>
		{:else}
			<div class="rounded-[30px] border border-dashed border-black/10 bg-white/70 px-6 py-14 text-center dark:border-white/10 dark:bg-white/[0.03]">
				<h3 class="text-xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50">
					Aucun serveur
				</h3>
				<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
					Commence par installer SSD en local, puis connecte le serveur si tu veux le retrouver ici.
				</p>
			</div>
		{/if}
	</div>
</section>