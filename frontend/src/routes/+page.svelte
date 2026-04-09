<script lang="ts">
	let { data } = $props<{
		data: {
			user?: {
				email?: string;
			} | null;
		};
	}>();
</script>

<svelte:head>
	<title>SSD — Déploie et pilote tes applications Docker</title>
	<meta
		name="description"
		content="SSD centralise le déploiement, le pilotage et le suivi de tes applications sur tes serveurs avec un catalogue de plus de 180 applications."
	/>
</svelte:head>

<section class="relative overflow-hidden">
	<div
		class="absolute inset-0 -z-30 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.18),transparent_28%),radial-gradient(circle_at_top_right,rgba(168,85,247,0.16),transparent_24%),radial-gradient(circle_at_bottom,rgba(16,185,129,0.12),transparent_28%)]"
	></div>
	<div
		class="absolute inset-0 -z-20 bg-[linear-gradient(180deg,rgba(255,255,255,0.94),rgba(255,255,255,0.72),rgba(255,255,255,0.40),transparent)] dark:bg-[linear-gradient(180deg,rgba(7,17,31,0.92),rgba(7,17,31,0.72),rgba(7,17,31,0.36),transparent)]"
	></div>
	<div
		class="absolute inset-0 -z-10 opacity-[0.22] [background-image:linear-gradient(to_right,rgba(15,23,42,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(15,23,42,0.06)_1px,transparent_1px)] [background-size:36px_36px] dark:opacity-[0.08]"
	></div>

	<div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
		<div
			class="relative overflow-hidden rounded-[34px] border border-black/5 bg-white/72 shadow-[0_30px_120px_rgba(15,23,42,0.12)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_30px_120px_rgba(0,0,0,0.42)] sm:rounded-[40px]"
		>
			<div class="pointer-events-none absolute inset-0">
				<div
					class="absolute inset-0 bg-[linear-gradient(135deg,rgba(56,189,248,0.08),rgba(37,99,235,0.04)_34%,rgba(168,85,247,0.06)_68%,rgba(16,185,129,0.05))]"
				></div>
				<div class="absolute inset-x-0 top-0 h-px bg-white/70 dark:bg-white/10"></div>
				<div class="absolute -left-20 top-8 h-52 w-52 rounded-full bg-sky-300/20 blur-3xl dark:bg-sky-400/10"></div>
				<div class="absolute -right-16 top-24 h-56 w-56 rounded-full bg-violet-300/20 blur-3xl dark:bg-violet-400/10"></div>
				<div class="absolute bottom-0 left-1/3 h-44 w-44 rounded-full bg-emerald-300/20 blur-3xl dark:bg-emerald-400/10"></div>
			</div>

			<div class="relative p-5 sm:p-8 lg:p-10 xl:p-12">
				<div class="max-w-5xl">
					<div class="flex flex-wrap items-center gap-3">
						<div
							class="inline-flex items-center gap-2 rounded-full border border-sky-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-sky-700 shadow-[0_10px_24px_rgba(14,165,233,0.08)] dark:border-sky-400/20 dark:bg-sky-400/10 dark:text-sky-300 dark:shadow-none"
						>
							<span class="h-2 w-2 rounded-full bg-sky-500"></span>
							Plateforme SSD
						</div>

						<a
							href="https://discord.gg/87RV5DStEK"
							target="_blank"
							rel="noreferrer"
							class="group inline-flex items-center gap-2 rounded-full border border-violet-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-700 shadow-[0_10px_24px_rgba(139,92,246,0.10)] transition-all duration-300 hover:-translate-y-0.5 hover:border-violet-300 hover:bg-white hover:shadow-[0_14px_30px_rgba(139,92,246,0.16)] dark:border-violet-400/20 dark:bg-violet-400/[0.10] dark:text-violet-200 dark:shadow-none dark:hover:border-violet-400/30 dark:hover:bg-violet-400/[0.14]"
						>
							<svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor" aria-hidden="true">
								<path
									d="M20.317 4.369A19.791 19.791 0 0 0 15.885 3c-.191.328-.403.77-.554 1.116a18.27 18.27 0 0 0-5.487 0A12.64 12.64 0 0 0 9.29 3a19.736 19.736 0 0 0-4.438 1.372C2.05 8.554 1.288 12.633 1.67 16.656a19.9 19.9 0 0 0 5.993 3.03c.482-.662.91-1.361 1.279-2.092a12.96 12.96 0 0 1-2.013-.97c.168-.123.332-.252.49-.385 3.88 1.823 8.09 1.823 11.924 0 .16.133.324.262.492.385a12.9 12.9 0 0 1-2.017.972c.37.729.797 1.428 1.28 2.09a19.86 19.86 0 0 0 6-3.03c.447-4.663-.762-8.705-3.776-12.287ZM9.75 14.23c-1.165 0-2.124-1.06-2.124-2.362 0-1.303.94-2.364 2.124-2.364 1.193 0 2.143 1.07 2.124 2.364 0 1.302-.94 2.362-2.124 2.362Zm4.5 0c-1.165 0-2.124-1.06-2.124-2.362 0-1.303.94-2.364 2.124-2.364 1.193 0 2.143 1.07 2.124 2.364 0 1.302-.94 2.362-2.124 2.362Z"
								/>
							</svg>
							<span>Discord</span>
							<span class="transition-transform duration-300 group-hover:translate-x-0.5">↗</span>
						</a>

						{#if data.user}
							<a
								href="https://projetssd.github.io/ssdv2_docs/"
								target="_blank"
								rel="noreferrer"
								class="group inline-flex items-center gap-2 rounded-full border border-cyan-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-cyan-700 shadow-[0_10px_24px_rgba(34,211,238,0.10)] transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-300 hover:bg-white hover:shadow-[0_14px_30px_rgba(34,211,238,0.16)] dark:border-cyan-400/20 dark:bg-cyan-400/[0.10] dark:text-cyan-200 dark:shadow-none dark:hover:border-cyan-400/30 dark:hover:bg-cyan-400/[0.14]"
							>
								<svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" aria-hidden="true">
									<path
										d="M7.75 6.75H16.25C17.2165 6.75 18 7.5335 18 8.5V18.25L14.25 15.75L10.5 18.25L6.75 15.75V8.5C6.75 7.5335 7.5335 6.75 8.5 6.75"
										stroke="currentColor"
										stroke-width="1.7"
										stroke-linecap="round"
										stroke-linejoin="round"
									/>
									<path d="M9.5 10.25H14.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
									<path d="M9.5 13H13.25" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
								</svg>
								<span>Documentation</span>
								<span class="transition-transform duration-300 group-hover:translate-x-0.5">↗</span>
							</a>

							<a
								href="https://github.com/projetssd/ssdv2"
								target="_blank"
								rel="noreferrer"
								class="group inline-flex items-center gap-2 rounded-full border border-zinc-200 bg-white/88 px-3.5 py-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-zinc-700 shadow-[0_10px_24px_rgba(15,23,42,0.08)] transition-all duration-300 hover:-translate-y-0.5 hover:border-zinc-300 hover:bg-white hover:shadow-[0_14px_30px_rgba(15,23,42,0.12)] dark:border-white/15 dark:bg-white/[0.06] dark:text-zinc-200 dark:shadow-none dark:hover:border-white/25 dark:hover:bg-white/[0.10]"
							>
								<svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor" aria-hidden="true">
									<path
										d="M12 2C6.477 2 2 6.59 2 12.252c0 4.53 2.865 8.373 6.839 9.73.5.096.682-.222.682-.493 0-.243-.009-.888-.014-1.743-2.782.617-3.37-1.37-3.37-1.37-.455-1.183-1.11-1.498-1.11-1.498-.908-.636.069-.623.069-.623 1.004.072 1.532 1.055 1.532 1.055.892 1.565 2.341 1.113 2.91.851.091-.667.349-1.113.635-1.369-2.22-.261-4.555-1.14-4.555-5.073 0-1.12.39-2.036 1.03-2.753-.103-.262-.446-1.316.098-2.744 0 0 .84-.277 2.75 1.051A9.303 9.303 0 0 1 12 6.847c.85.004 1.705.117 2.504.344 1.909-1.328 2.748-1.051 2.748-1.051.546 1.428.203 2.482.1 2.744.64.717 1.028 1.633 1.028 2.753 0 3.943-2.339 4.809-4.566 5.065.359.32.679.95.679 1.915 0 1.383-.012 2.499-.012 2.839 0 .273.18.593.688.492A10.255 10.255 0 0 0 22 12.252C22 6.59 17.523 2 12 2Z"
									/>
								</svg>
								<span>GitHub</span>
								<span class="transition-transform duration-300 group-hover:translate-x-0.5">↗</span>
							</a>
						{/if}
					</div>

					<div class="mt-6 max-w-4xl">


                                                <h1
	                                                class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white sm:text-2xl lg:text-[2rem] lg:leading-[1.12]"
                                                >
	                                                         Déploie tes applications Docker avec
	                                                <span class="bg-[linear-gradient(90deg,#0ea5e9_0%,#2563eb_26%,#8b5cf6_62%,#10b981_100%)] bg-clip-text text-transparent">
		                                                 Traefik (serveur Web) et CrowdSec (sécurité)
	                                                </span>
	                                                         depuis une interface claire et moderne.
                                               </h1>

						<p class="mt-6 max-w-2xl text-base leading-8 text-zinc-600 dark:text-zinc-400">
							SSD t’aide à installer, suivre et gérer tes services sur un ou plusieurs serveurs,
							avec un catalogue de plus de 180 applications, de la documentation liée à chaque app
							et un vrai suivi des déploiements.
						</p>
					</div>

					<div class="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
						{#if data.user}
							<a
								href="/app-store/library"
								class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
							>
								Explorer le catalogue
							</a>

							<a
								href="/servers"
								class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
							>
								Gérer mes serveurs
							</a>
						{:else}
							<a
								href="/register"
								class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
							>
								Créer un compte
							</a>

							<a
								href="/app-store/library"
								class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
							>
								Voir les applications
							</a>
						{/if}
					</div>

					<div class="mt-10 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
						<div
							class="group relative overflow-hidden rounded-[24px] border border-sky-200/70 bg-white/84 px-4 py-4 shadow-[0_16px_34px_rgba(14,165,233,0.08)] transition-transform duration-300 hover:-translate-y-1 dark:border-sky-400/15 dark:bg-sky-400/[0.06] dark:shadow-none"
						>
							<div class="absolute inset-x-4 top-0 h-px bg-sky-300/70 dark:bg-sky-400/30"></div>
							<p
								class="text-[11px] font-semibold uppercase tracking-[0.15em] text-sky-700 dark:text-sky-300"
							>
								Catalogue
							</p>
							<p class="mt-2 text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
								180+
							</p>
							<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
								applications prêtes à déployer
							</p>
						</div>

						<div
							class="group relative overflow-hidden rounded-[24px] border border-emerald-200/70 bg-white/84 px-4 py-4 shadow-[0_16px_34px_rgba(16,185,129,0.08)] transition-transform duration-300 hover:-translate-y-1 dark:border-emerald-400/15 dark:bg-emerald-400/[0.06] dark:shadow-none"
						>
							<div class="absolute inset-x-4 top-0 h-px bg-emerald-300/70 dark:bg-emerald-400/30"></div>
							<p
								class="text-[11px] font-semibold uppercase tracking-[0.15em] text-emerald-700 dark:text-emerald-300"
							>
								Tarif
							</p>
							<p class="mt-2 text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
								Gratuit
							</p>
							<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
								pour installer et piloter
							</p>
						</div>

						<div
							class="group relative overflow-hidden rounded-[24px] border border-violet-200/70 bg-white/84 px-4 py-4 shadow-[0_16px_34px_rgba(139,92,246,0.08)] transition-transform duration-300 hover:-translate-y-1 dark:border-violet-400/15 dark:bg-violet-400/[0.06] dark:shadow-none"
						>
							<div class="absolute inset-x-4 top-0 h-px bg-violet-300/70 dark:bg-violet-400/30"></div>
							<p
								class="text-[11px] font-semibold uppercase tracking-[0.15em] text-violet-700 dark:text-violet-300"
							>
								Stack
							</p>
							<p class="mt-2 text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
								Docker
							</p>
							<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
								Traefik et CrowdSec intégrés
							</p>
						</div>

						<div
							class="group relative overflow-hidden rounded-[24px] border border-amber-200/70 bg-white/84 px-4 py-4 shadow-[0_16px_34px_rgba(245,158,11,0.08)] transition-transform duration-300 hover:-translate-y-1 dark:border-amber-400/15 dark:bg-amber-400/[0.06] dark:shadow-none"
						>
							<div class="absolute inset-x-4 top-0 h-px bg-amber-300/70 dark:bg-amber-400/30"></div>
							<p
								class="text-[11px] font-semibold uppercase tracking-[0.15em] text-amber-700 dark:text-amber-300"
							>
								Diagnostic
							</p>
							<p class="mt-2 text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white">
								Précis
							</p>
							<p class="mt-1 text-xs leading-6 text-zinc-600 dark:text-zinc-300">
								logs, erreurs et historique
							</p>
						</div>
					</div>
				</div>

				<div class="mt-12">
					<div class="grid gap-5 lg:grid-cols-3">
						<div
							class="group relative overflow-hidden rounded-[28px] border border-black/5 bg-white/80 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_24px_52px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-none"
						>
							<div
								class="absolute inset-x-0 top-0 h-1 bg-[linear-gradient(90deg,rgba(34,211,238,0.9),rgba(96,165,250,0.9),rgba(168,85,247,0.9))]"
							></div>
							<div
								class="mb-4 inline-flex items-center rounded-full border border-black/5 bg-black/[0.02] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400"
							>
								01 — Découvrir
							</div>
							<h3 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
								Catalogue et documentation
							</h3>
							<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								Explore plus de 180 applications, retrouve leur documentation et choisis rapidement
								le service adapté à ton besoin.
							</p>

							<div class="mt-5 grid gap-3">
								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Parcours centralisé
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										Le catalogue, la doc et les actions de déploiement restent réunis dans la
										même interface.
									</p>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Stack cohérente
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										SSD s’appuie sur Docker, Traefik et CrowdSec pour offrir une base claire et
										modulable.
									</p>
								</div>
							</div>
						</div>

						<div
							class="group relative overflow-hidden rounded-[28px] border border-black/5 bg-white/80 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_24px_52px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-none"
						>
							<div
								class="absolute inset-x-0 top-0 h-1 bg-[linear-gradient(90deg,rgba(16,185,129,0.9),rgba(34,211,238,0.9),rgba(59,130,246,0.9))]"
							></div>
							<div
								class="mb-4 inline-flex items-center rounded-full border border-black/5 bg-black/[0.02] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400"
							>
								02 — Déployer
							</div>
							<h3 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
								Local ou appairé, selon ton besoin
							</h3>
							<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								Tu peux utiliser SSD uniquement en local avec le script si tu veux garder un
								fonctionnement autonome.
							</p>

							<div class="mt-5 grid gap-3">
								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Appairage optionnel
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										Si tu appaires tes serveurs, tu peux ensuite déployer, installer et
										désinstaller tes applications directement depuis l’interface.
									</p>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Pilotage multi-serveurs
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										Ajoute et supervise plusieurs machines sans multiplier les outils ni les
										manipulations.
									</p>
								</div>
							</div>
						</div>

						<div
							class="group relative overflow-hidden rounded-[28px] border border-black/5 bg-white/80 p-6 shadow-[0_18px_40px_rgba(15,23,42,0.06)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_24px_52px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-none"
						>
							<div
								class="absolute inset-x-0 top-0 h-1 bg-[linear-gradient(90deg,rgba(245,158,11,0.9),rgba(168,85,247,0.9),rgba(34,211,238,0.9))]"
							></div>
							<div
								class="mb-4 inline-flex items-center rounded-full border border-black/5 bg-black/[0.02] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400"
							>
								03 — Exploiter
							</div>
							<h3 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
								Suivi, diagnostic et confiance
							</h3>
							<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
								SSD te fait gagner du temps tout en gardant une bonne visibilité sur l’état des
								déploiements et les erreurs.
							</p>

							<div class="mt-5 grid gap-3">
								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Logs exploitables
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										En cas d’échec, tu gardes un historique clair pour comprendre, corriger et
										accélérer le diagnostic.
									</p>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-white/76 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]"
								>
									<p class="text-sm font-semibold text-zinc-900 dark:text-white">
										Assistance plus précise
									</p>
									<p class="mt-1 text-sm leading-6 text-zinc-600 dark:text-zinc-400">
										L’appairage améliore le suivi, la remontée des erreurs et la qualité de
										l’accompagnement sans te retirer le contrôle de tes serveurs.
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="mt-12">
					<div
						class="relative overflow-hidden rounded-[32px] border border-black/5 bg-white/80 p-6 shadow-[0_22px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_18px_50px_rgba(0,0,0,0.24)] sm:p-8"
					>
						<div
							class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(34,211,238,0.05),rgba(59,130,246,0.04),rgba(168,85,247,0.05))]"
						></div>

						<div class="relative grid gap-6 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
							<div class="min-w-0">
								<p
									class="text-[11px] font-semibold uppercase tracking-[0.16em] text-zinc-500 dark:text-zinc-400"
								>
									Prêt à commencer
								</p>
								<h2
									class="mt-2 max-w-2xl text-2xl font-semibold tracking-[-0.04em] text-zinc-950 dark:text-white sm:text-3xl"
								>
									Un outil gratuit pour déployer vite et garder le contrôle
								</h2>
								<p class="mt-3 max-w-2xl text-sm leading-8 text-zinc-600 dark:text-zinc-400">
									Que tu veuilles héberger quelques services ou structurer une stack plus
									complète, SSD te donne une base claire, moderne et efficace.
								</p>
							</div>

							<div class="flex flex-col gap-3 sm:flex-row lg:flex-col lg:items-stretch">
								<a
									href="/app-store/library"
									class="inline-flex items-center justify-center rounded-[18px] border border-cyan-200 bg-[linear-gradient(90deg,#06b6d4,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_14px_34px_rgba(37,99,235,0.24)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(37,99,235,0.30)] dark:border-white/10"
								>
									Découvrir le catalogue
								</a>

								{#if data.user}
									<a
										href="/servers"
										class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
									>
										Ouvrir mes serveurs
									</a>
								{:else}
									<a
										href="/login"
										class="inline-flex items-center justify-center rounded-[18px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-900 shadow-[0_12px_24px_rgba(15,23,42,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18)]"
									>
										Se connecter
									</a>
								{/if}
							</div>
						</div>
					</div>
				</div>

				{#if data.user}
					<p class="mt-8 text-sm text-zinc-500 dark:text-zinc-400">
						Connecté en tant que
						<span class="font-medium text-zinc-800 dark:text-zinc-200">{data.user.email}</span>
					</p>
				{/if}
			</div>
		</div>
	</div>
</section>