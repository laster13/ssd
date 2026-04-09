<script lang="ts">
	import { onMount } from 'svelte';

	let { data, form } = $props();

	type AdminMachine = {
		id: string;
		machine_uuid: string;
		status: string;
		connection_status?: string | null;
		hostname?: string | null;
		agent_version?: string | null;
		auth_token_created_at?: string | null;
		last_seen_at?: string | null;
		created_at?: string | null;
		updated_at?: string | null;
	};

	let machine = $state(normalizeMachine(data.machine));
	let jobs = $state(Array.isArray(data.jobs) ? data.jobs : []);
	const authOptions = ['basique', 'oauth', 'authelia', 'aucune', 'oauth2-proxy'];
	const machineSocketUrl = (data.machineSocketUrl ?? '') as string;
	let machineDeleted = $state(false);

	$effect(() => {
		machine = normalizeMachine(data.machine);
		jobs = Array.isArray(data.jobs) ? data.jobs : [];
		machineDeleted = false;
	});

	function resolveMachineStatus(status: unknown, connectionStatus?: unknown) {
		const normalizedStatus = String(status ?? '').trim().toLowerCase();
		const normalizedConnection = String(connectionStatus ?? '').trim().toLowerCase();
		if (normalizedStatus === 'revoked') return 'revoked';
		if (normalizedStatus === 'error' || normalizedStatus === 'failed') return 'error';
		if (normalizedConnection === 'online') return 'online';
		if (normalizedStatus === 'online' || normalizedStatus === 'connected' || normalizedStatus === 'active') return 'online';
		if (normalizedStatus === 'offline' || normalizedStatus === 'disconnected' || normalizedStatus === 'inactive') return 'offline';
		if (normalizedStatus === 'paired') return normalizedConnection === 'online' ? 'online' : 'offline';
		return normalizedStatus || 'unknown';
	}

	function normalizeMachine(value: any): AdminMachine {
		const normalizedConnection = String(value?.connection_status ?? '').trim().toLowerCase();
		return {
			...value,
			status: resolveMachineStatus(value?.status, value?.connection_status),
			connection_status: normalizedConnection || null
		};
	}

	const effectiveStatus = $derived(form?.revoked ? 'revoked' : machine.status);

	function machineStatusClass(status: string) {
		switch (status?.toLowerCase()) {
			case 'online':
			case 'connected':
			case 'active':
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300';
			case 'offline':
			case 'disconnected':
			case 'inactive':
				return 'border-zinc-200 bg-zinc-100 text-zinc-700 dark:border-white/10 dark:bg-white/5 dark:text-zinc-300';
			case 'revoked':
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300';
			case 'error':
			case 'failed':
				return 'border-red-200 bg-red-50 text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300';
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

	function applyMachineSocketPayload(payload: any) {
		if (!payload || typeof payload !== 'object') return;
		if (payload.type === 'machine_snapshot' && Array.isArray(payload.machines)) {
			const match = payload.machines.find((item: any) => item?.id === machine.id);
			if (match) {
				machine = { ...machine, ...normalizeMachine(match) };
				machineDeleted = false;
			}
			return;
		}
		if (payload.type === 'machine_presence' && payload.machine?.id === machine.id) {
			machine = { ...machine, ...normalizeMachine(payload.machine) };
			machineDeleted = false;
			return;
		}
		if (payload.type === 'machine_removed' && payload.machine_id === machine.id) {
			machineDeleted = true;
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
	<title>Détail machine</title>
</svelte:head>

<section class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<a
		href="/admin"
		class="mb-4 inline-flex items-center gap-2 text-sm font-medium text-sky-600 transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
	>
		<span>←</span>
		<span>Retour admin</span>
	</a>

	{#if form?.error}
		<div
			class="mb-4 rounded-[20px] border border-red-200 bg-red-50 px-4 py-4 text-sm font-medium text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300"
		>
			{form.error}
		</div>
	{/if}

	{#if form?.rotated}
		<div
			class="mb-4 rounded-[20px] border border-emerald-200 bg-emerald-50 px-4 py-4 text-emerald-800 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300"
		>
			<div class="mb-2 text-sm font-semibold">Nouveau token machine généré</div>
			<div class="mb-3 text-sm leading-6">
				Copie-le maintenant. Il ne sera plus réaffiché ensuite.
			</div>
			<div
				class="rounded-[16px] border border-black/5 bg-white/70 px-4 py-3 font-mono text-sm break-all text-zinc-800 dark:border-white/10 dark:bg-[rgba(2,6,23,0.55)] dark:text-zinc-200"
			>
				{form.rotatedToken}
			</div>
		</div>
	{/if}

	{#if form?.revoked}
		<div
			class="mb-4 rounded-[20px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm leading-6 text-amber-800 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300"
		>
			La machine a été révoquée. Elle ne pourra plus communiquer avec le backend tant qu’elle
			n’est pas re-pairée.
		</div>
	{/if}

	{#if machineDeleted}
		<div
			class="mb-4 rounded-[20px] border border-red-200 bg-red-50 px-4 py-4 text-sm leading-6 text-red-800 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300"
		>
			Cette machine a été supprimée du backend. Recharge la page ou retourne au tableau de bord admin.
		</div>
	{/if}

	<div class="grid items-start gap-6 lg:grid-cols-[380px_minmax(0,1fr)]">
		<div class="grid gap-6">
			<div
				class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
			>
				<div class="relative">
					<div
						class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
					></div>

					<div class="relative p-6">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Actions sécurité machine
						</h2>

						<div class="mt-5 grid gap-4">
							<form method="POST" action="?/rotateToken">
								<input type="hidden" name="_csrf" value={data.csrfToken} />
								<button
									type="submit"
									disabled={effectiveStatus === 'revoked'}
									class="inline-flex w-full items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#2563eb)] px-4 py-4 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.26)] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10"
								>
									Rotate machine token
								</button>
							</form>

							<form method="POST" action="?/revokeMachine">
								<input type="hidden" name="_csrf" value={data.csrfToken} />
								<button
									type="submit"
									disabled={effectiveStatus === 'revoked'}
									class="inline-flex w-full items-center justify-center rounded-[16px] border border-red-200 bg-[linear-gradient(90deg,#ef4444,#dc2626)] px-4 py-4 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(220,38,38,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(220,38,38,0.26)] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10"
								>
									Revoke machine
								</button>
							</form>

							<p class="text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								<strong>Rotate</strong> génère un nouveau token machine.
								<strong>Revoke</strong> coupe immédiatement la relation entre cette machine
								et le backend.
							</p>
						</div>
					</div>
				</div>
			</div>

			<div
				class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
			>
				<div class="relative">
					<div
						class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
					></div>

					<div class="relative p-6">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Installer une app
						</h2>

						<form method="POST" action="?/createJob" class="mt-5 grid gap-4">
							<input type="hidden" name="_csrf" value={data.csrfToken} />

							<label class="grid gap-2">
								<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
									App slug
								</span>
								<input
									name="app_slug"
									value={form?.app_slug ?? ''}
									placeholder="n8n"
									disabled={effectiveStatus === 'revoked'}
									class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
								/>
							</label>

							<label class="grid gap-2">
								<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
									Sous-domaine
								</span>
								<input
									name="subdomain"
									value={form?.subdomain ?? ''}
									placeholder="demo"
									disabled={effectiveStatus === 'revoked'}
									class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
								/>
							</label>

							<label class="grid gap-2">
								<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
									Type d'auth
								</span>
								<select
									name="auth_type"
									disabled={effectiveStatus === 'revoked'}
									class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
								>
									{#each authOptions as option}
										<option value={option} selected={(form?.auth_type ?? 'aucune') === option}>
											{option}
										</option>
									{/each}
								</select>
							</label>

							<button
								type="submit"
								disabled={effectiveStatus === 'revoked'}
								class="mt-2 inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#2563eb)] px-4 py-4 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.26)] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10"
							>
								Créer le job
							</button>
						</form>
					</div>
				</div>
			</div>
		</div>

		<div class="grid gap-6">
			<div
				class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
			>
				<div class="relative">
					<div
						class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
					></div>

					<div class="relative p-6 sm:p-8">
						<div class="mb-5 flex flex-wrap items-start justify-between gap-3">
							<div>
								<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
									Informations
								</h2>
								<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
									État actuel et métadonnées de la machine.
								</p>
							</div>

							<span
								class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${machineStatusClass(effectiveStatus)}`}
							>
								{effectiveStatus}
							</span>
						</div>

						<div class="grid gap-3 sm:grid-cols-2">
							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">ID</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.id}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">UUID</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200 break-all">{machine.machine_uuid}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Hostname</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.hostname ?? '-'}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Agent version</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.agent_version ?? '-'}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Auth token créé le</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.auth_token_created_at ?? '-'}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Last seen</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.last_seen_at ?? '-'}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Created at</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.created_at}</div>
							</div>

							<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
								<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">Updated at</div>
								<div class="text-sm text-zinc-800 dark:text-zinc-200">{machine.updated_at}</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div
				class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
			>
				<div class="relative">
					<div
						class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
					></div>

					<div class="relative p-6 sm:p-8">
						<div class="mb-5">
							<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl">
								Jobs de cette machine
							</h2>
							<p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
								Historique des tâches associées à cette machine.
							</p>
						</div>

						{#if jobs.length > 0}
							<div
								class="overflow-x-auto rounded-[22px] border border-black/5 bg-white/50 dark:border-white/10 dark:bg-white/[0.03]"
							>
								<table class="min-w-full divide-y divide-black/5 dark:divide-white/10">
									<thead>
										<tr class="text-left">
											<th class="px-4 py-4 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
												ID
											</th>
											<th class="px-4 py-4 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
												Type
											</th>
											<th class="px-4 py-4 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
												Status
											</th>
											<th class="px-4 py-4 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
												Créé le
											</th>
											<th class="px-4 py-4 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
												Action
											</th>
										</tr>
									</thead>

									<tbody class="divide-y divide-black/5 dark:divide-white/10">
										{#each jobs as job}
											<tr class="transition-colors duration-200 hover:bg-black/[0.025] dark:hover:bg-white/[0.03]">
												<td class="whitespace-nowrap px-4 py-4 text-sm font-medium text-zinc-900 dark:text-zinc-100">
													{job.id}
												</td>
												<td class="whitespace-nowrap px-4 py-4 text-sm text-zinc-600 dark:text-zinc-300">
													{job.type}
												</td>
												<td class="whitespace-nowrap px-4 py-4 text-sm">
													<span
														class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${jobStatusClass(job.status)}`}
													>
														{job.status}
													</span>
												</td>
												<td class="whitespace-nowrap px-4 py-4 text-sm text-zinc-600 dark:text-zinc-300">
													{job.created_at}
												</td>
												<td class="whitespace-nowrap px-4 py-4 text-sm">
													<a
														href={`/admin/jobs/${job.id}`}
														class="font-medium text-sky-600 transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
													>
														Voir
													</a>
												</td>
											</tr>
										{/each}
									</tbody>
								</table>
							</div>
						{:else}
							<div
								class="rounded-[22px] border border-dashed border-black/10 bg-black/[0.02] px-5 py-8 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.02] dark:text-zinc-400"
							>
								Aucun job pour cette machine.
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>