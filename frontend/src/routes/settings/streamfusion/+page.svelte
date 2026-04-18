<script lang="ts">
	let { data, form } = $props();

	let copied = $state('');

	const latestAccess = $derived(form?.created ?? null);

	async function copyText(value: string) {
		try {
			await navigator.clipboard.writeText(value);
			copied = value;
			setTimeout(() => {
				if (copied === value) copied = '';
			}, 1800);
		} catch {
			copied = '';
		}
	}
</script>

<svelte:head>
	<title>StreamFusion</title>
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
				<div class="mb-6">
					<div
						class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300"
					>
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						StreamFusion
					</div>

					<h1
						class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]"
					>
						<span
							class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]"
						>
							Instance Publique StreamFusion
						</span>
					</h1>

					<p class="mt-3 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						SSD crée un lien privé vers la page de configuration de StreamFusion.
						Ce lien te permet d’ouvrir l’interface de configuration et de générer ton manifest.
					</p>
				</div>

				<div
					class="mb-6 rounded-[18px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm leading-7 text-amber-800 dark:border-amber-500/28 dark:bg-amber-500/[0.08] dark:text-amber-200"
				>
					<strong>Important :</strong> Ce lien de configuration est à usage unique.
				</div>

				<section
					class="mb-8 rounded-[22px] border border-black/5 bg-white/60 p-5 dark:border-white/10 dark:bg-[rgba(15,23,42,0.45)]"
				>
					<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
						Créer un lien de configuration
					</h2>

					<form method="POST" action="?/create" class="mt-5 grid gap-4">
						<input type="hidden" name="_csrf" value={data.csrfToken} />

						<div>
							<button
								type="submit"
								class="inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#a855f7)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(59,130,246,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(59,130,246,0.26)] dark:border-white/10"
							>
								Créer le lien de configuration
							</button>
						</div>
					</form>
				</section>

				{#if latestAccess}
					<section
						class="mb-8 rounded-[22px] border border-emerald-200 bg-emerald-50 p-5 dark:border-emerald-500/30 dark:bg-emerald-500/[0.08]"
					>
						<h2
							class="text-xl font-semibold tracking-[-0.03em] text-emerald-900 dark:text-emerald-100"
						>
							Lien prêt
						</h2>

						<p class="mt-3 text-sm leading-7 text-emerald-800 dark:text-emerald-200">
							Ouvre cette page pour configurer ton addon StreamFusion.
							Pour une nouvelle configuration, tu devras en générer un nouveau.
						</p>

						<div
							class="mt-4 rounded-[16px] border border-emerald-200 bg-white/80 p-4 font-mono text-sm break-all text-zinc-900 dark:border-emerald-500/20 dark:bg-black/20 dark:text-zinc-100"
						>
							{latestAccess.configure_url}
						</div>

						<div class="mt-4 flex flex-wrap gap-3">
							<button
								type="button"
								onclick={() => copyText(latestAccess.configure_url)}
								class="inline-flex items-center justify-center rounded-[14px] border border-black/10 bg-white px-4 py-2.5 text-sm font-medium text-zinc-900 transition hover:-translate-y-0.5 dark:border-white/10 dark:bg-white/[0.06] dark:text-white"
							>
								Copier le lien
							</button>

							<a
								href={latestAccess.configure_url}
								target="_blank"
								rel="noreferrer"
								class="inline-flex items-center justify-center rounded-[14px] border border-black/10 bg-black px-4 py-2.5 text-sm font-medium text-white transition hover:-translate-y-0.5 dark:border-white/10"
							>
								Ouvrir StreamFusion
							</a>
						</div>

						{#if copied === latestAccess.configure_url}
							<p class="mt-3 text-sm font-medium text-emerald-700 dark:text-emerald-300">
								Lien copié.
							</p>
						{/if}
					</section>
				{/if}

				{#if form?.error}
					<p class="mt-5 text-sm font-medium text-red-600 dark:text-red-300">{form.error}</p>
				{/if}
			</div>
		</div>
	</div>
</section>