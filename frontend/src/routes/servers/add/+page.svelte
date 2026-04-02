<script lang="ts">
	import { PUBLIC_BACKEND_URL_HTTPS } from '$env/static/public';

	let { data, form } = $props();

	let copied = $state(false);
	let copyTimeout: ReturnType<typeof setTimeout> | null = null;

	const pairing = $derived(form?.pairing ?? null);
	const pairingCode = $derived(pairing?.pairing_code ?? '-');
	const machineUuid = $derived(pairing?.machine_uuid ?? '-');

	const backendUrl = $derived((PUBLIC_BACKEND_URL_HTTPS || '').replace(/\/$/, ''));

	const bootstrapCommand = $derived(
		pairing && backendUrl
			? `curl -fsSL ${backendUrl}/bootstrap.sh | sudo bash -s -- --pairing-code ${pairing.pairing_code} --backend-url ${backendUrl}`
			: ''
	);

	async function copyBootstrapCommand() {
		if (!bootstrapCommand) return;

		try {
			await navigator.clipboard.writeText(bootstrapCommand);
			copied = true;

			if (copyTimeout) clearTimeout(copyTimeout);
			copyTimeout = setTimeout(() => {
				copied = false;
			}, 2000);
		} catch (error) {
			console.error('copy bootstrap command failed', error);
		}
	}
</script>

<svelte:head>
	<title>Ajouter un serveur</title>
</svelte:head>

<section class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
	<div
		class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
	>
		<div class="relative">
			<div
				class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
			></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/servers"
						class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						← Retour aux serveurs
					</a>
				</p>

				<h1
					class="mb-2 text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl"
				>
					Ajouter un serveur
				</h1>

				<p class="max-w-4xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
					Génère un code de connexion puis lance le bootstrap ci-dessous sur le serveur
					distant.
				</p>

				<form method="POST" action="?/generate" class="mt-6">
					<input type="hidden" name="_csrf" value={data.csrfToken} />
					<button
						type="submit"
						class="inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#a855f7)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(59,130,246,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(59,130,246,0.26)] dark:border-white/10"
					>
						Générer un code
					</button>
				</form>

				{#if pairing}
					<div class="my-6 grid gap-4 md:grid-cols-2">
						<div
							class="rounded-[20px] border border-black/5 bg-white/70 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]"
						>
							<div class="text-sm text-zinc-500 dark:text-zinc-400">Code de connexion</div>
							<div
								class="mt-2 text-3xl font-extrabold tracking-[0.08em] text-zinc-950 dark:text-white"
							>
								{pairingCode}
							</div>
						</div>

						<div
							class="rounded-[20px] border border-black/5 bg-white/70 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]"
						>
							<div class="text-sm text-zinc-500 dark:text-zinc-400">
								Machine UUID pré-enregistrée
							</div>
							<div class="mt-2 break-all text-base font-semibold text-zinc-950 dark:text-white">
								{machineUuid}
							</div>
						</div>
					</div>

					<div
						class="mb-5 rounded-[20px] border border-black/5 bg-black/[0.03] p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)]"
					>
						<div class="mb-3 flex items-center justify-between gap-3">
							<div class="text-sm text-zinc-500 dark:text-zinc-400">Commande bootstrap</div>

							<button
								type="button"
								onclick={copyBootstrapCommand}
								class="inline-flex h-10 w-10 items-center justify-center rounded-[14px] border border-black/8 bg-white/80 text-zinc-700 transition hover:border-black/12 hover:bg-white dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.08]"
								aria-label="Copier la commande bootstrap"
								title={copied ? 'Copié' : 'Copier'}
							>
								{#if copied}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
										class="h-5 w-5"
									>
										<path d="M20 6 9 17l-5-5" />
									</svg>
								{:else}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
										class="h-5 w-5"
									>
										<rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
										<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
									</svg>
								{/if}
							</button>
						</div>

						<pre class="m-0 whitespace-pre-wrap break-words font-mono text-sm leading-7 text-zinc-900 dark:text-zinc-100">{bootstrapCommand}</pre>

						{#if copied}
							<p class="mt-3 text-xs font-medium text-emerald-600 dark:text-emerald-300">
								Commande copiée dans le presse-papiers.
							</p>
						{/if}
					</div>
				{/if}

				{#if form?.success}
					<p class="mt-5 text-sm font-medium text-emerald-600 dark:text-emerald-300">
						Code généré avec succès.
					</p>
				{/if}

				{#if form?.error}
					<p class="mt-5 text-sm font-medium text-red-600 dark:text-red-300">{form.error}</p>
				{/if}
			</div>
		</div>
	</div>
</section>