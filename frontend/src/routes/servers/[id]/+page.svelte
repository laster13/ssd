<script lang="ts">
	let { data } = $props();

	const machine = data.machine;
	const isInstalled = Boolean(machine.ssdv2_installed);

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
	<title>Serveur</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.14),transparent_24%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.10),transparent_24%),radial-gradient(circle_at_bottom,rgba(168,85,247,0.10),transparent_30%)]"></div>

	<div class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
		<div class="overflow-hidden rounded-[34px] border border-black/5 bg-white/75 shadow-[0_28px_100px_rgba(15,23,42,0.10)] backdrop-blur dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_100px_rgba(0,0,0,0.34)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.10),rgba(37,99,235,0.07)_38%,rgba(168,85,247,0.08)_72%)]"></div>

				<div class="relative p-6 sm:p-8 lg:p-10">
					<p class="mb-5">
						<a
							href="/servers"
							class="inline-flex items-center gap-2 text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
						>
							<span>←</span>
							<span>Retour aux serveurs</span>
						</a>
					</p>

					<div class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
						<div>
							<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-300">
								<span class="h-2 w-2 rounded-full bg-cyan-500"></span>
								Serveur connecté
							</div>

							<h1 class="max-w-3xl text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl xl:text-5xl">
								{machine.hostname ?? 'Serveur sans nom'}
							</h1>

							<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								Cette page affiche l’état du serveur connecté à ton compte. L’installation de SSD
								se fait désormais localement, hors dashboard.
							</p>

							<div class="mt-6 grid gap-3 sm:grid-cols-3">
								<div class={`rounded-[22px] border px-4 py-4 shadow-[0_14px_30px_rgba(15,23,42,0.05)] dark:shadow-none ${
									isInstalled
										? 'border-emerald-200 bg-emerald-50/90 dark:border-emerald-400/20 dark:bg-emerald-400/10'
										: 'border-amber-200 bg-amber-50/90 dark:border-amber-400/20 dark:bg-amber-400/10'
								}`}>
									<p class={`text-[11px] font-semibold uppercase tracking-[0.15em] ${
										isInstalled
											? 'text-emerald-700 dark:text-emerald-300'
											: 'text-amber-700 dark:text-amber-300'
									}`}>
										SSD
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										{isInstalled ? 'Installé' : 'Non détecté'}
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										{#if isInstalled}
											SSDv2 est déjà présent sur ce serveur.
										{:else}
											L’installation passe maintenant par la page “Installer SSD en local”.
										{/if}
									</p>
								</div>

								<div class="rounded-[22px] border border-sky-200 bg-sky-50/90 px-4 py-4 shadow-[0_14px_30px_rgba(14,165,233,0.08)] dark:border-sky-400/20 dark:bg-sky-400/10 dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-sky-700 dark:text-sky-300">
										Connexion
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Active dans le dashboard
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Le serveur reste appairé à ton compte.
									</p>
								</div>

								<div class="rounded-[22px] border border-violet-200 bg-violet-50/90 px-4 py-4 shadow-[0_14px_30px_rgba(168,85,247,0.08)] dark:border-violet-400/20 dark:bg-violet-400/10 dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300">
										Dernier contact
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										{formatDate(machine.last_seen_at)}
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Version agent : {machine.agent_version ?? '-'}
									</p>
								</div>
							</div>

							<div class="mt-6 flex flex-col gap-3 sm:flex-row">
								<a
									href="/install"
									class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
								>
									Installer SSD en local
								</a>

								<a
									href="/servers"
									class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
								>
									Retour à la liste
								</a>
							</div>
						</div>

						<div class="rounded-[28px] border border-black/5 bg-white/80 p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_20px_60px_rgba(0,0,0,0.22)]">
							<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-200 bg-fuchsia-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-fuchsia-700 dark:border-fuchsia-400/20 dark:bg-fuchsia-400/10 dark:text-fuchsia-300">
								<span class="h-2 w-2 rounded-full bg-fuchsia-500"></span>
								Informations
							</div>

							<div class="grid gap-3 text-sm text-zinc-700 dark:text-zinc-300">
								<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										ID
									</p>
									<p class="mt-2 break-all font-medium text-zinc-900 dark:text-zinc-100">
										{machine.id}
									</p>
								</div>

								<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										UUID machine
									</p>
									<p class="mt-2 break-all font-mono text-zinc-900 dark:text-zinc-100">
										{machine.machine_uuid}
									</p>
								</div>

								<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Statut
									</p>
									<p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">
										{machine.status ?? '-'}
									</p>
								</div>

								<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Agent
									</p>
									<p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">
										{machine.agent_version ?? '-'}
									</p>
								</div>

								<div class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-3 dark:border-white/10 dark:bg-white/[0.03]">
									<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Dernier contact
									</p>
									<p class="mt-2 font-medium text-zinc-900 dark:text-zinc-100">
										{formatDate(machine.last_seen_at)}
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>