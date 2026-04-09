<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import type { Machine } from '$lib/utils/jobs';
	import {
		formatFrenchDateTime,
		machinePillClass,
		machineStatusLabel,
		resolveMachineConnectionStatus
	} from '$lib/utils/jobs';

	let { data } = $props();
	let machine = $state(data.machine as Machine);
	const machineSocketUrl = $derived((data.machineSocketUrl ?? '') as string);
	const isInstalled = $derived(Boolean(machine.ssdv2_installed));
	const connectionStatus = $derived(resolveMachineConnectionStatus(machine));

	function applyMachineSocketPayload(payload: any) {
		if (!payload || typeof payload !== 'object') return;
		if (payload.type === 'machine_removed' && payload.machine_id === machine.id) {
			goto('/servers');
			return;
		}
		if (payload.type === 'machine_presence' && payload.machine && payload.machine.id === machine.id) {
			machine = { ...machine, ...payload.machine };
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
			socket?.close();
		};
	});
</script>

<svelte:head>
	<title>Serveur</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.14),transparent_24%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.10),transparent_24%),radial-gradient(circle_at_bottom,rgba(168,85,247,0.10),transparent_30%)]"></div>
	<div class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
		<div class="overflow-hidden rounded-[34px] border border-black/5 bg-white/75 shadow-[0_28px_100px_rgba(15,23,42,0.10)] backdrop-blur dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_100px_rgba(0,0,0,0.34)]">
			<div class="relative p-6 sm:p-8 lg:p-10">
				<p class="mb-5">
					<a href="/servers" class="inline-flex items-center gap-2 text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200">
						<span>←</span>
						<span>Retour aux serveurs</span>
					</a>
				</p>

				<div class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
					<div>
						<div class={`mb-4 inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] ${machinePillClass(connectionStatus)}`}>
							<span class={`h-2 w-2 rounded-full ${connectionStatus === 'online' ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
							Serveur {machineStatusLabel(connectionStatus).toLowerCase()}
						</div>

						<h1 class="max-w-3xl text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl xl:text-5xl">{machine.hostname ?? 'Serveur sans nom'}</h1>
						<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">Cette page affiche l’état du serveur appairé à ton compte. Le statut de connexion est maintenant mis à jour en temps réel via websocket.</p>

						<div class="mt-6 grid gap-3 sm:grid-cols-3">
							<div class={`rounded-[22px] border px-4 py-4 shadow-[0_14px_30px_rgba(15,23,42,0.05)] dark:shadow-none ${isInstalled ? 'border-emerald-200 bg-emerald-50/90 dark:border-emerald-400/20 dark:bg-emerald-400/10' : 'border-amber-200 bg-amber-50/90 dark:border-amber-400/20 dark:bg-amber-400/10'}`}>
								<p class={`text-[11px] font-semibold uppercase tracking-[0.15em] ${isInstalled ? 'text-emerald-700 dark:text-emerald-300' : 'text-amber-700 dark:text-amber-300'}`}>SSD</p>
								<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">{isInstalled ? 'Installé' : 'Non détecté'}</p>
							</div>
							<div class={`rounded-[22px] border px-4 py-4 shadow-[0_14px_30px_rgba(14,165,233,0.08)] dark:shadow-none ${connectionStatus === 'online' ? 'border-sky-200 bg-sky-50/90 dark:border-sky-400/20 dark:bg-sky-400/10' : 'border-rose-200 bg-rose-50/90 dark:border-rose-400/20 dark:bg-rose-400/10'}`}>
								<p class={`text-[11px] font-semibold uppercase tracking-[0.15em] ${connectionStatus === 'online' ? 'text-sky-700 dark:text-sky-300' : 'text-rose-700 dark:text-rose-300'}`}>Connexion</p>
								<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">{machineStatusLabel(connectionStatus)}</p>
								<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">Le serveur reste appairé à ton compte tant qu’il n’est pas désappairé.</p>
							</div>
							<div class="rounded-[22px] border border-violet-200 bg-violet-50/90 px-4 py-4 shadow-[0_14px_30px_rgba(168,85,247,0.08)] dark:border-violet-400/20 dark:bg-violet-400/10 dark:shadow-none">
								<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300">Dernier contact</p>
								<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">{formatFrenchDateTime(machine.last_seen_at)}</p>
								<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">Version agent : {machine.agent_version ?? '-'}</p>
							</div>
						</div>
					</div>

					<div class="rounded-[28px] border border-black/5 bg-white/80 p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_20px_60px_rgba(0,0,0,0.22)]">
						<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-200 bg-fuchsia-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-fuchsia-700 dark:border-fuchsia-400/20 dark:bg-fuchsia-400/10 dark:text-fuchsia-300"><span class="h-2 w-2 rounded-full bg-fuchsia-500"></span>Informations</div>
						<div class="grid gap-3 text-sm text-zinc-700 dark:text-zinc-300">
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]"><p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">ID</p><p class="mt-2 break-all font-medium text-zinc-900 dark:text-zinc-100">{machine.id}</p></div>
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]"><p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">UUID machine</p><p class="mt-2 break-all font-mono text-zinc-900 dark:text-zinc-100">{machine.machine_uuid}</p></div>
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]"><p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Appairage</p><p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">{machine.status ?? '-'}</p></div>
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]"><p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Connexion</p><p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">{machineStatusLabel(connectionStatus)}</p></div>
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]"><p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Dernier contact</p><p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">{formatFrenchDateTime(machine.last_seen_at)}</p></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>
