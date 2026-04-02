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
				className:
					'border border-red-200 bg-red-50 text-red-600 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300'
			};
		}

		if (
			status === 'paired' ||
			status === 'online' ||
			status === 'connected' ||
			status === 'active'
		) {
			return {
				label: 'En ligne',
				className:
					'border border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300'
			};
		}

		if (status === 'offline' || status === 'disconnected' || status === 'inactive') {
			return {
				label: 'Hors ligne',
				className:
					'border border-zinc-200 bg-zinc-100 text-zinc-600 dark:border-zinc-500/20 dark:bg-zinc-500/10 dark:text-zinc-300'
			};
		}

		if (status === 'error' || status === 'failed') {
			return {
				label: 'En erreur',
				className:
					'border border-red-200 bg-red-50 text-red-600 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300'
			};
		}

		return {
			label: server?.status ?? 'Inconnu',
			className:
				'border border-zinc-200 bg-zinc-100 text-zinc-600 dark:border-zinc-500/20 dark:bg-zinc-500/10 dark:text-zinc-300'
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

<section class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<header class="mb-6 overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.34)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.75),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.035),rgba(255,255,255,0.01))]"></div>

			<div class="relative flex flex-col gap-6 p-5 sm:p-6 lg:flex-row lg:items-end lg:justify-between">
				<div class="max-w-3xl">
					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						Servers
					</div>

					<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Mes serveurs
					</h1>

					<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Retrouve ici les serveurs pairés à ton compte et ajoute-en un nouveau si besoin.
					</p>
				</div>

				<a
					href="/servers/add"
					class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.22)] transition-all duration-200 hover:translate-y-[-1px] hover:shadow-[0_16px_36px_rgba(37,99,235,0.28)] dark:border-white/10"
				>
					Ajouter un serveur
				</a>
			</div>
		</div>
	</header>

	{#if form?.success}
		<div class="mb-6 rounded-[20px] border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
			L'appairage du serveur a bien été supprimé.
		</div>
	{/if}

	{#if form?.error}
		<div class="mb-6 rounded-[20px] border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
			{form.error}
		</div>
	{/if}

	{#if servers.length > 0}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
			{#each servers as server}
				{@const badge = badgeFor(server)}

				<article
					class="overflow-hidden rounded-[26px] border border-black/5 bg-white/70 p-5 shadow-[0_12px_34px_rgba(15,23,42,0.06)] ring-1 ring-inset ring-black/[0.03] transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_18px_42px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.035] dark:ring-white/[0.04] dark:shadow-[0_12px_34px_rgba(0,0,0,0.20)] dark:hover:shadow-[0_18px_42px_rgba(0,0,0,0.28)]"
				>
					<div class="mb-5 flex items-start justify-between gap-3">
						<div class="min-w-0">
							<h2 class="truncate text-[1.05rem] font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
								{server.hostname ?? 'Serveur sans nom'}
							</h2>

							<div class="mt-1 flex flex-wrap items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400">
								<span class="truncate">{server.machine_uuid}</span>
								<span class="rounded-full border border-black/8 bg-black/[0.03] px-2 py-0.5 text-[11px] font-medium text-zinc-600 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
									{shortUuid(server.machine_uuid)}
								</span>
							</div>
						</div>

						<div
							class={`shrink-0 rounded-full px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.12em] ${badge.className}`}
						>
							{badge.label}
						</div>
					</div>

					<div class="grid gap-3 text-sm text-zinc-700 dark:text-zinc-300">
						<div class="flex items-start justify-between gap-3 border-b border-black/5 pb-3 dark:border-white/5">
							<span class="font-medium text-zinc-500 dark:text-zinc-500">ID</span>
							<span class="text-right text-zinc-900 dark:text-zinc-100">{server.id}</span>
						</div>

						<div class="flex items-start justify-between gap-3 border-b border-black/5 pb-3 dark:border-white/5">
							<span class="font-medium text-zinc-500 dark:text-zinc-500">UUID court</span>
							<span class="text-right font-mono text-zinc-900 dark:text-zinc-100">
								{shortUuid(server.machine_uuid)}
							</span>
						</div>

						<div class="flex items-start justify-between gap-3 border-b border-black/5 pb-3 dark:border-white/5">
							<span class="font-medium text-zinc-500 dark:text-zinc-500">Agent</span>
							<span class="text-right text-zinc-900 dark:text-zinc-100">
								{server.agent_version ?? '-'}
							</span>
						</div>

						<div class="flex items-start justify-between gap-3 border-b border-black/5 pb-3 dark:border-white/5">
							<span class="font-medium text-zinc-500 dark:text-zinc-500">Dernier contact</span>
							<span class="text-right text-zinc-900 dark:text-zinc-100">
								{formatDate(server.last_seen_at)}
							</span>
						</div>

						<div class="flex items-start justify-between gap-3">
							<span class="font-medium text-zinc-500 dark:text-zinc-500">Statut brut</span>
							<span class="text-right text-zinc-900 dark:text-zinc-100">
								{server.status ?? '-'}
							</span>
						</div>
					</div>

					<div class="mt-5 flex justify-end border-t border-black/5 pt-4 dark:border-white/5">
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
								class="inline-flex items-center justify-center rounded-[14px] border border-red-200 bg-[linear-gradient(90deg,#ef4444,#dc2626)] px-4 py-2.5 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(220,38,38,0.18)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(220,38,38,0.24)] dark:border-red-500/20"
							>
								Supprimer
							</button>
						</form>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="rounded-[24px] border border-black/5 bg-white/60 p-6 text-sm text-zinc-600 shadow-[0_10px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-400 dark:shadow-[0_10px_30px_rgba(0,0,0,0.2)]">
			Aucun serveur pairé pour le moment.
		</div>
	{/if}
</section>