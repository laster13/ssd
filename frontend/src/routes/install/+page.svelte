<script lang="ts">
  import { onDestroy } from 'svelte';
  import { getAgentBackendUrl } from '$lib/public-config';

  let copied = $state(false);
  let copyTimeout: ReturnType<typeof setTimeout> | null = null;

  let agentBackendUrl = '';

  try {
    agentBackendUrl = getAgentBackendUrl();
  } catch {
    agentBackendUrl = '';
  }

  const installScriptUrl = agentBackendUrl ? `${agentBackendUrl}/install-ssd-local.sh` : '';

  const installCommand = installScriptUrl
    ? `curl -4 -fsSL ${installScriptUrl} -o /tmp/install-ssd-local.sh && sudo TARGET_USER="$USER" bash /tmp/install-ssd-local.sh`
    : '';

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

  onDestroy(() => {
    if (copyTimeout) clearTimeout(copyTimeout);
  });
</script>

<svelte:head>
	<title>Installer SSD en local</title>
</svelte:head>

<section class="relative overflow-hidden">
	<div
		class="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.18),transparent_28%),radial-gradient(circle_at_top_right,rgba(168,85,247,0.14),transparent_24%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.12),transparent_30%)]"
	></div>

	<div class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
		<div
			class="overflow-hidden rounded-[28px] border border-black/5 bg-white/75 shadow-[0_28px_100px_rgba(15,23,42,0.10)] backdrop-blur dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_28px_100px_rgba(0,0,0,0.35)] sm:rounded-[34px]"
		>
			<div class="relative">
				<div
					class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(56,189,248,0.10),rgba(37,99,235,0.06)_34%,rgba(168,85,247,0.08)_66%,rgba(16,185,129,0.08))] dark:bg-[linear-gradient(135deg,rgba(56,189,248,0.10),rgba(37,99,235,0.07)_34%,rgba(168,85,247,0.08)_66%,rgba(16,185,129,0.08))]"
				></div>

				<div class="relative p-5 sm:p-8 lg:p-10">
					<p class="mb-6">
						<a
							href="/servers"
							class="inline-flex items-center gap-2 text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
						>
							<span>←</span>
							<span>Retour aux serveurs</span>
						</a>
					</p>

					<div class="grid gap-10 xl:grid-cols-[minmax(0,1.08fr)_minmax(420px,0.92fr)] xl:items-start">
						<div class="min-w-0">
							<div
								class="mb-5 inline-flex items-center gap-2 rounded-full border border-sky-200 bg-sky-50/90 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300"
							>
								<span class="h-2 w-2 rounded-full bg-sky-500"></span>
								Installation locale
							</div>

							<h1
								class="max-w-2xl text-2xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-3xl lg:text-[2.35rem] lg:leading-[1.08]"
							>
								<span
									class="bg-[linear-gradient(90deg,#0ea5e9_0%,#2563eb_38%,#8b5cf6_72%,#10b981_100%)] bg-clip-text text-transparent"
								>
									Installer SSD en local, sans passer par le dashboard
								</span>
							</h1>

							<p class="mt-5 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								Cette page sert uniquement à lancer l’installation locale de SSD sur ton serveur.
								L’appairage avec ton compte est séparé et reste optionnel.
							</p>

							<div class="mt-8 grid gap-3 md:grid-cols-3 md:auto-rows-fr">
								<div
									class="h-full rounded-[24px] border border-sky-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(14,165,233,0.08)] dark:border-sky-400/15 dark:bg-sky-400/[0.06] dark:shadow-none"
								>
									<p
										class="text-[11px] font-semibold uppercase tracking-[0.15em] text-sky-700 dark:text-sky-300"
									>
										Étape 1
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Copie la commande
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Exécute-la directement sur le serveur cible.
									</p>
								</div>

								<div
									class="h-full rounded-[24px] border border-violet-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(139,92,246,0.08)] dark:border-violet-400/15 dark:bg-violet-400/[0.06] dark:shadow-none"
								>
									<p
										class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300"
									>
										Étape 2
									</p>
									<p class="mt-2 text-sm font-semibold text-zinc-900 dark:text-white">
										Installe SSD
									</p>
									<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
										Le suivi se fait localement dans le terminal.
									</p>
								</div>

								<div
									class="h-full rounded-[24px] border border-emerald-200/70 bg-white/80 px-4 py-4 shadow-[0_14px_30px_rgba(16,185,129,0.08)] dark:border-emerald-400/15 dark:bg-emerald-400/[0.06] dark:shadow-none"
								>
									<p
										class="text-[11px] font-semibold uppercase tracking-[0.15em] text-emerald-700 dark:text-emerald-300"
									>
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

						<div class="min-w-0 xl:sticky xl:top-6">
							<div class="xl:mx-auto xl:max-w-[500px]">
								<div
									class="rounded-[28px] border border-black/5 bg-white/82 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_24px_70px_rgba(0,0,0,0.24)] sm:p-6"
								>
									<div
										class="mb-3 inline-flex items-center gap-2 rounded-full border border-fuchsia-200 bg-fuchsia-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-fuchsia-700 dark:border-fuchsia-400/20 dark:bg-fuchsia-400/10 dark:text-fuchsia-300"
									>
										<span class="h-2 w-2 rounded-full bg-fuchsia-500"></span>
										Commande
									</div>

									<h2 class="text-lg font-semibold text-zinc-950 dark:text-white sm:text-xl">
										Installation prête à lancer
									</h2>

									<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
										Le script d’installation locale ne dépend pas du pairing.
									</p>

									{#if installCommand}
										<div
											class="mt-5 overflow-hidden rounded-[22px] border border-zinc-200 bg-zinc-950 dark:border-white/10"
										>
											<div
												class="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-4 py-3"
											>
												<div class="flex items-center gap-2">
													<span class="h-2.5 w-2.5 rounded-full bg-rose-400"></span>
													<span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
													<span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
												</div>

												<button
													type="button"
													onclick={copyInstallCommand}
													class="inline-flex w-full items-center justify-center rounded-[12px] border border-white/10 bg-white/10 px-3 py-2 text-xs font-semibold text-white transition hover:bg-white/15 sm:w-auto sm:px-3 sm:py-1.5"
												>
													{#if copied}
														Copiée
													{:else}
														Copier
													{/if}
												</button>
											</div>

											<div class="overflow-x-auto">
												<pre
													class="m-0 min-w-0 whitespace-pre-wrap break-all px-4 py-4 font-mono text-sm leading-7 text-zinc-100"
												>{installCommand}</pre>
											</div>
										</div>
									{:else}
										<div
											class="mt-5 rounded-[20px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300"
										>
											La variable PUBLIC_AGENT_BACKEND_URL_HTTPS n’est pas configurée.
										</div>
									{/if}
								</div>
							</div>
						</div>
					</div>

					<div class="mt-10 grid gap-4 xl:grid-cols-[minmax(0,1fr)_auto] xl:items-center">
						<div
							class="rounded-[26px] border border-black/5 bg-white/75 px-5 py-5 shadow-[0_14px_30px_rgba(15,23,42,0.05)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-none sm:px-6"
						>
							<p class="text-sm font-semibold text-zinc-900 dark:text-white">
								Une fois SSD installé, tu peux laisser le serveur autonome ou le connecter à ton
								compte.
							</p>
							<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								L’appairage ne sert pas seulement au pilotage depuis l’interface : il permet aussi
								un suivi précis des installations, une remontée claire des erreurs et une assistance
								beaucoup plus efficace en cas d’échec ou de dysfonctionnement.
							</p>
						</div>

						<div class="flex flex-col gap-3 sm:flex-row xl:justify-end">
							<a
								href="/servers/add"
								class="inline-flex w-full items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10 sm:w-auto"
							>
								Connecter un serveur ensuite
							</a>

							<a
								href="/servers"
								class="inline-flex w-full items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)] sm:w-auto"
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