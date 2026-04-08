<script lang="ts">
	import { PUBLIC_BACKEND_URL_HTTPS } from '$env/static/public';

	let copied = $state(false);
	let copyTimeout: ReturnType<typeof setTimeout> | null = null;

	const backendUrl = (PUBLIC_BACKEND_URL_HTTPS || '').replace(/\/$/, '');
	const installScriptUrl = backendUrl ? `${backendUrl}/install-ssd-local.sh` : '';
	const installCommand = installScriptUrl ? `curl -fsSL ${installScriptUrl} | sudo bash` : '';

	async function copyInstallCommand() {
		if (!installCommand) return;

		try {
			await navigator.clipboard.writeText(installCommand);
			copied = true;

			if (copyTimeout) clearTimeout(copyTimeout);
			copyTimeout = setTimeout(() => {
				copied = false;
			}, 2200);
		} catch (error) {
			console.error('copy install command failed', error);
		}
	}
</script>

<svelte:head>
	<title>Installer SSD en local</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.18),transparent_28%),radial-gradient(circle_at_top_right,rgba(168,85,247,0.14),transparent_24%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.12),transparent_30%)]"></div>

	<div class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
		<div class="overflow-hidden rounded-[34px] border border-black/5 bg-white/75 shadow-[0_28px_100px_rgba(15,23,42,0.10)] backdrop-blur dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_100px_rgba(0,0,0,0.35)]">
			<div class="relative">
				<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(56,189,248,0.10),rgba(37,99,235,0.06)_34%,rgba(168,85,247,0.08)_66%,rgba(16,185,129,0.08))] dark:bg-[linear-gradient(135deg,rgba(56,189,248,0.10),rgba(37,99,235,0.07)_34%,rgba(168,85,247,0.08)_66%,rgba(16,185,129,0.08))]"></div>

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

					<div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr] lg:items-start">
						<div>
							<div class="mb-4 inline-flex items-center gap-2 rounded-full border border-sky-200 bg-sky-50/90 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300">
								<span class="h-2 w-2 rounded-full bg-sky-500"></span>
								Installation locale
							</div>

							<h1 class="max-w-3xl text-lg font-semibold tracking-[-0.02em] text-zinc-950 dark:text-white sm:text-xl xl:text-2xl">
								<span class="bg-[linear-gradient(90deg,#0ea5e9_0%,#2563eb_38%,#8b5cf6_72%,#10b981_100%)] bg-clip-text text-transparent">
									Installer SSD en local, sans passer par le dashboard
								</span>
							</h1>

							<p class="mt-4 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								Cette page sert uniquement à lancer l’installation locale de SSD sur ton serveur.
								L’appairage avec ton compte est séparé et reste optionnel.
							</p>

							<div class="mt-6 grid gap-3 sm:grid-cols-3">
								<div class="rounded-[22px] border border-sky-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(14,165,233,0.08)] dark:border-sky-400/15 dark:bg-sky-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-sky-700 dark:text-sky-300">
										Étape 1
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Copie la commande
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Exécute-la directement sur le serveur cible.
									</p>
								</div>

								<div class="rounded-[22px] border border-violet-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(139,92,246,0.08)] dark:border-violet-400/15 dark:bg-violet-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300">
										Étape 2
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Installe SSD
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Le suivi se fait localement dans le terminal.
									</p>
								</div>

								<div class="rounded-[22px] border border-emerald-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(16,185,129,0.08)] dark:border-emerald-400/15 dark:bg-emerald-400/[0.06] dark:shadow-none">
									<p class="text-[11px] font-semibold uppercase tracking-[0.15em] text-emerald-700 dark:text-emerald-300">
										Étape 3
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Appairage optionnel
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Connecte ensuite le serveur à ton compte si tu veux le piloter ici.
									</p>
								</div>
							</div>
						</div>

						<div class="rounded-[28px] border border-black/5 bg-white/80 p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_20px_60px_rgba(0,0,0,0.22)]">
							<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-200 bg-fuchsia-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-fuchsia-700 dark:border-fuchsia-400/20 dark:bg-fuchsia-400/10 dark:text-fuchsia-300">
								<span class="h-2 w-2 rounded-full bg-fuchsia-500"></span>
								Commande
							</div>

							<h2 class="text-lg font-semibold text-zinc-950 dark:text-white">
								Installation prête à lancer
							</h2>

							<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								Le script d’installation locale ne dépend pas du pairing.
							</p>

							{#if installCommand}
								<div class="mt-4 overflow-hidden rounded-[22px] border border-zinc-200 bg-zinc-950 dark:border-white/10">
									<div class="flex items-center justify-between border-b border-white/10 px-4 py-3">
										<div class="flex items-center gap-2">
											<span class="h-2.5 w-2.5 rounded-full bg-rose-400"></span>
											<span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
											<span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
										</div>

										<button
											type="button"
											onclick={copyInstallCommand}
											class="inline-flex items-center justify-center rounded-[12px] border border-white/10 bg-white/10 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-white/15"
										>
											{#if copied}
												Copiée
											{:else}
												Copier
											{/if}
										</button>
									</div>

									<pre class="m-0 whitespace-pre-wrap break-words px-4 py-4 font-mono text-sm leading-7 text-zinc-100">{installCommand}</pre>
								</div>

								<p class="mt-3 text-xs leading-6 text-zinc-500 dark:text-zinc-400">
									<span class="font-mono text-zinc-700 dark:text-zinc-300">{installScriptUrl}</span>
								</p>
							{:else}
								<div class="mt-4 rounded-[20px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300">
									La variable <span class="font-mono">PUBLIC_BACKEND_URL_HTTPS</span> n’est pas configurée.
								</div>
							{/if}
						</div>
					</div>

					<div class="mt-8 grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
						<div class="rounded-[24px] border border-black/5 bg-white/75 px-5 py-4 shadow-[0_14px_30px_rgba(15,23,42,0.05)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-none">
							<p class="text-sm font-semibold text-zinc-900 dark:text-white">
								Une fois SSD installé, tu peux laisser le serveur autonome ou le connecter à ton compte.
							</p>
							<p class="mt-1 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								L’appairage ne sert qu’au pilotage depuis l’interface.
							</p>
						</div>

						<div class="flex flex-col gap-3 sm:flex-row">
							<a
								href="/servers/add"
								class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
							>
								Connecter un serveur ensuite
							</a>

							<a
								href="/servers"
								class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
							>
								Retour à la liste
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>