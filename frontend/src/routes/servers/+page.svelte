<script lang="ts">
	let { data, form } = $props();

	const servers = Array.isArray(data.machines) ? data.machines : [];

	function shortUuid(value: unknown) {
		const str = String(value ?? '');
		return str ? `${str.slice(0, 8)}…` : '-';
	}

	function badgeFor(server: any) {
		const status = String(server?.status ?? '').trim().toLowerCase();

		if (status === 'revoked') {
			return {
				label: 'Révoquée',
				dot: 'bg-red-500',
				className:
					'border-red-200 bg-red-50 text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300'
			};
		}

		if (
			status === 'paired' ||
			status === 'online' ||
			status === 'connected' ||
			status === 'active'
		) {
			return {
				label: 'Connecté',
				dot: 'bg-emerald-500',
				className:
					'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300'
			};
		}

		if (status === 'offline' || status === 'disconnected' || status === 'inactive') {
			return {
				label: 'Hors ligne',
				dot: 'bg-zinc-400',
				className:
					'border-zinc-200 bg-zinc-100 text-zinc-700 dark:border-zinc-500/20 dark:bg-zinc-500/10 dark:text-zinc-300'
			};
		}

		if (status === 'error' || status === 'failed') {
			return {
				label: 'Erreur',
				dot: 'bg-rose-500',
				className:
					'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300'
			};
		}

		return {
			label: server?.status ?? 'Inconnu',
			dot: 'bg-amber-500',
			className:
				'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300'
		};
	}

	function formatDate(value: unknown) {
		if (!value) return '-';

		const date = new Date(String(value));
		if (Number.isNaN(date.getTime())) return String(value);

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'short',
			timeStyle: 'short'
		}).format(date);
	}
</script>

<svelte:head>
	<title>Mes serveurs</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.14),transparent_24%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.12),transparent_22%),radial-gradient(circle_at_bottom,rgba(168,85,247,0.10),transparent_28%)]"></div>

	<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
		<header class="mb-6 overflow-hidden rounded-[34px] border border-black/5 bg-white/75 shadow-[0_28px_100px_rgba(15,23,42,0.10)] backdrop-blur dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_100px_rgba(0,0,0,0.34)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.10),rgba(37,99,235,0.08)_36%,rgba(168,85,247,0.08)_72%,rgba(16,185,129,0.06))]"></div>

				<div class="relative flex flex-col gap-6 p-6 sm:p-8 lg:flex-row lg:items-end lg:justify-between">
					<div class="max-w-3xl">
						<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-300">
							<span class="h-2 w-2 rounded-full bg-cyan-500"></span>
							Servers
						</div>

						<h1 class="text-lg font-semibold tracking-[-0.02em] text-zinc-950 dark:text-white sm:text-xl xl:text-2xl">
							<span class="bg-[linear-gradient(90deg,#06b6d4_0%,#2563eb_42%,#8b5cf6_86%)] bg-clip-text text-transparent">
								Gestion des serveurs
							</span>
						</h1>

						<p class="mt-4 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
							Installe SSD en local sur un serveur, puis connecte-le à ton compte uniquement si
							tu veux le piloter depuis le dashboard.
						</p>
					</div>

					<div class="flex flex-col gap-3 sm:flex-row">
						<a
							href="/install"
							class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
						>
							Installer SSD en local
						</a>

						<a
							href="/servers/add"
							class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
						>
							Connecter un serveur
						</a>
					</div>
				</div>
			</div>
		</header>

		{#if form?.success}
			<div class="mb-6 rounded-[22px] border border-emerald-200 bg-emerald-50 px-4 py-4 text-sm font-medium text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
				L'appairage du serveur a bien été supprimé.
			</div>
		{/if}

		{#if form?.error}
			<div class="mb-6 rounded-[22px] border border-red-200 bg-red-50 px-4 py-4 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
				{form.error}
			</div>
		{/if}

		{#if servers.length > 0}
			<div class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
				{#each servers as server}
					{@const badge = badgeFor(server)}

					<article class="group overflow-hidden rounded-[30px] border border-black/5 bg-white/75 shadow-[0_18px_48px_rgba(15,23,42,0.08)] ring-1 ring-inset ring-black/[0.03] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(15,23,42,0.12)] dark:border-white/10 dark:bg-white/[0.045] dark:ring-white/[0.04] dark:shadow-[0_18px_48px_rgba(0,0,0,0.24)] dark:hover:shadow-[0_24px_60px_rgba(0,0,0,0.32)]">
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
									<span class="font-medium text-zinc-500 dark:text-zinc-400">ID</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">{server.id}</span>
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">Agent</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">
										{server.agent_version ?? '-'}
									</span>
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">SSD</span>

									{#if server.ssdv2_installed}
										<span class="font-semibold text-emerald-600 dark:text-emerald-400">
											Installé
										</span>
									{:else}
										<span class="font-semibold text-amber-600 dark:text-amber-400">
											Non installé
										</span>
									{/if}
								</div>

								<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<span class="font-medium text-zinc-500 dark:text-zinc-400">Dernier contact</span>
									<span class="text-right text-zinc-900 dark:text-zinc-100">
										{formatDate(server.last_seen_at)}
									</span>
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
										if (
											!confirm(
												`Supprimer l'appairage du serveur "${server.hostname ?? server.machine_uuid}" ?`
											)
										) {
											event.preventDefault();
										}
									}}
								>
									<input type="hidden" name="_csrf" value={data.csrfToken} />
									<input type="hidden" name="machine_id" value={server.id} />
									<button
										type="submit"
										class="inline-flex items-center justify-center rounded-[16px] border border-rose-200 bg-[linear-gradient(90deg,#f43f5e,#e11d48)] px-4 py-2.5 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(225,29,72,0.18)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(225,29,72,0.24)] dark:border-rose-500/20"
									>
										Supprimer
									</button>
								</form>
							</div>
						</div>
					</article>
				{/each}
			</div>
		{:else}
			<div class="rounded-[28px] border border-black/5 bg-white/70 p-6 text-sm shadow-[0_18px_48px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_18px_48px_rgba(0,0,0,0.24)]">
				<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:border-violet-400/20 dark:bg-violet-400/10 dark:text-violet-300">
					<span class="h-2 w-2 rounded-full bg-violet-500"></span>
					Aucun serveur
				</div>

				<p class="text-sm font-semibold text-zinc-900 dark:text-white">
					Aucun serveur pairé pour le moment.
				</p>
				<p class="mt-1 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
					Commence par installer SSD en local, puis connecte le serveur si tu veux le retrouver ici.
				</p>
			</div>
		{/if}
	</div>
</section>