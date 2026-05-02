<script lang="ts">
	import { PUBLIC_AGENT_BACKEND_URL_HTTPS } from '$env/static/public';

	let { data, form } = $props();

	let copied = $state(false);
	let copyTimeout: ReturnType<typeof setTimeout> | null = null;

	const pairing = $derived(form?.pairing ?? null);
	const pairingCode = $derived(pairing?.pairing_code ?? '-');
	const machineUuid = $derived(pairing?.machine_uuid ?? '-');
	const expiresAt = $derived(pairing?.expires_at ?? null);
	const backendUrl = $derived((PUBLIC_AGENT_BACKEND_URL_HTTPS || '').replace(/\/$/, ''));

	const bootstrapCommand = $derived(
		pairing && backendUrl
			? `curl -4 -fsSL ${backendUrl}/bootstrap.sh | sudo bash -s -- --pairing-code ${pairing.pairing_code} --backend-url ${backendUrl} --force-ipv4`
			: ''
	);

	function formatDate(value: unknown) {
		if (!value) return '-';

		const date = new Date(String(value));
		if (Number.isNaN(date.getTime())) return String(value);

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'short',
			timeStyle: 'short'
		}).format(date);
	}

	async function copyBootstrapCommand() {
		if (!bootstrapCommand) return;

		try {
			await navigator.clipboard.writeText(bootstrapCommand);
			copied = true;

			if (copyTimeout) clearTimeout(copyTimeout);
			copyTimeout = setTimeout(() => {
				copied = false;
			}, 2200);
		} catch (error) {
			console.error('copy bootstrap command failed', error);
		}
	}
</script>

<svelte:head>
	<title>Connecter un serveur</title>
</svelte:head>

<section class="relative overflow-x-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.16),transparent_28%),radial-gradient(circle_at_top_right,rgba(59,130,246,0.14),transparent_22%),radial-gradient(circle_at_bottom,rgba(168,85,247,0.12),transparent_30%)]"></div>

	<div class="mx-auto max-w-6xl py-8 sm:px-6 lg:px-8">
		<div class="px-4 sm:px-0">
			<p class="mb-5">
				<a
					href="/servers"
					class="inline-flex items-center gap-2 text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
				>
					<span>←</span>
					<span>Retour aux serveurs</span>
				</a>
			</p>
		</div>

		<div class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
			<div class="border-y border-black/5 bg-white/75 backdrop-blur dark:border-white/10 dark:bg-white/[0.045] sm:overflow-hidden sm:rounded-[34px] sm:border sm:shadow-[0_28px_100px_rgba(15,23,42,0.10)] dark:sm:shadow-[0_28px_100px_rgba(0,0,0,0.35)]">
				<div class="relative">
					<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.10),rgba(37,99,235,0.08)_42%,rgba(168,85,247,0.08))]"></div>

					<div class="relative px-4 py-6 sm:p-8 lg:p-10">
						<div>
							<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-cyan-50/90 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-300">
								<span class="h-2 w-2 rounded-full bg-cyan-500"></span>
								Appairage
							</div>

							<h1 class="max-w-3xl break-words text-lg font-semibold tracking-[-0.02em] text-zinc-950 dark:text-white sm:text-xl xl:text-2xl">
								<span class="bg-[linear-gradient(90deg,#06b6d4_0%,#2563eb_42%,#8b5cf6_86%)] bg-clip-text text-transparent">
									Connecter un serveur à ton compte
								</span>
							</h1>

							<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								Après l’installation locale de SSD, génère ici un code d’appairage puis exécute
								la commande sur le serveur pour le relier au dashboard.
							</p>

                                                        <div class="mt-6 flex flex-col gap-3 sm:flex-row">
                                                                <a
                                                                        href="/install"
                                                                        class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
                                                                >
                                                                        Installer SSD en local d’abord
                                                                </a>

                                                                <form method="POST" action="?/generate" class="flex">
                                                                        <input type="hidden" name="_csrf" value={data.csrfToken} />
                                                                        <button
                                                                                type="submit"
                                                                                class="inline-flex w-full items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
                                                                        >
                                                                                Générer un code d’appairage
                                                                        </button>
                                                                </form>
                                                        </div>

							<div class="mt-6 grid gap-3 sm:grid-cols-3">
								<div class="rounded-[22px] border border-cyan-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(34,211,238,0.08)] dark:border-cyan-400/15 dark:bg-cyan-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-cyan-700 dark:text-cyan-300">
										Étape 1
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Génère le code
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Le code temporaire lie le prochain bootstrap à ton compte.
									</p>
								</div>

								<div class="rounded-[22px] border border-blue-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(59,130,246,0.08)] dark:border-blue-400/15 dark:bg-blue-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-blue-700 dark:text-blue-300">
										Étape 2
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Lance le bootstrap
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										L’agent est configuré et le serveur est appairé.
									</p>
								</div>

								<div class="rounded-[22px] border border-violet-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(168,85,247,0.08)] dark:border-violet-400/15 dark:bg-violet-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300">
										Étape 3
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Retrouve le serveur
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Il remonte ensuite automatiquement dans ta liste de serveurs.
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="border-y border-black/5 bg-white/80 px-4 py-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_20px_60px_rgba(0,0,0,0.22)] sm:rounded-[28px] sm:border sm:p-5">
				<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-200 bg-fuchsia-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-fuchsia-700 dark:border-fuchsia-400/20 dark:bg-fuchsia-400/10 dark:text-fuchsia-300">
					<span class="h-2 w-2 rounded-full bg-fuchsia-500"></span>
					Statut
				</div>

				{#if form?.success}
					<div class="rounded-[20px] border border-emerald-200 bg-emerald-50 px-4 py-4 text-sm text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300">
						Code d’appairage généré avec succès.
					</div>
				{:else}
					<div class="rounded-[20px] border border-zinc-200 bg-zinc-50 px-4 py-4 text-sm text-zinc-700 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-300">
						Génère un code pour afficher la commande complète d’appairage.
					</div>
				{/if}

				{#if form?.error}
					<div class="mt-4 rounded-[20px] border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300">
						{form.error}
					</div>
				{/if}

				<div class="mt-4 grid gap-3">
					<div class="rounded-[18px] border border-zinc-200 bg-zinc-50/80 px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
						<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:text-zinc-400">
							Code
						</p>
						<p class="mt-2 font-mono text-lg font-semibold text-zinc-900 dark:text-white">
							{pairingCode}
						</p>
					</div>

					<div class="rounded-[18px] border border-zinc-200 bg-zinc-50/80 px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
						<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:text-zinc-400">
							Machine UUID
						</p>
						<p class="mt-2 break-all font-mono text-sm text-zinc-900 dark:text-white">
							{machineUuid}
						</p>
					</div>

					<div class="rounded-[18px] border border-zinc-200 bg-zinc-50/80 px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]">
						<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:text-zinc-400">
							Expiration
						</p>
						<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
							{formatDate(expiresAt)}
						</p>
					</div>
				</div>
			</div>
		</div>

		{#if pairing}
			<div class="mt-8 border-y border-black/5 bg-white/80 px-4 py-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_20px_60px_rgba(0,0,0,0.22)] sm:rounded-[30px] sm:border sm:p-5">
				<div class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
					<div>
						<div class="mb-2 inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300">
							<span class="h-2 w-2 rounded-full bg-emerald-500"></span>
							Commande d’appairage
						</div>

						<h2 class="text-lg font-semibold text-zinc-950 dark:text-white">
							Commande prête à lancer
						</h2>

						<p class="mt-1 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
							Exécute cette commande sur le serveur déjà installé localement.
						</p>
					</div>

					{#if bootstrapCommand}
						<button
							type="button"
							onclick={copyBootstrapCommand}
							class="inline-flex items-center justify-center rounded-[14px] border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
						>
							{#if copied}
								Commande copiée
							{:else}
								Copier la commande
							{/if}
						</button>
					{/if}
				</div>

				{#if bootstrapCommand}
					<div class="overflow-hidden rounded-[22px] border border-zinc-200 bg-zinc-950 dark:border-white/10">
						<div class="flex items-center gap-2 border-b border-white/10 px-4 py-3">
							<span class="h-2.5 w-2.5 rounded-full bg-rose-400"></span>
							<span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
							<span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
						</div>

						<pre class="m-0 whitespace-pre-wrap break-words px-4 py-4 font-mono text-sm leading-7 text-zinc-100">{bootstrapCommand}</pre>
					</div>
				{:else}
					<div class="rounded-[20px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300">
						La variable <span class="font-mono">PUBLIC_BACKEND_URL_HTTPS</span> n’est pas configurée.
					</div>
				{/if}
			</div>
		{/if}
	</div>
</section>