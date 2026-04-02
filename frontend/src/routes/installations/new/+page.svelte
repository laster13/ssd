<script lang="ts">
	let { data, form } = $props();

	const app = data.app;
	const machines = data.machines ?? [];
	const authOptions = ['aucune', 'basique', 'oauth', 'authelia', 'oauth2-proxy'];
</script>

<svelte:head>
	<title>Nouvelle installation</title>
</svelte:head>

<section class="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="mb-6">
		<a
			class="inline-flex items-center text-sm font-medium text-sky-600 transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
			href="/app-store"
		>
			← Retour à l’App Store
		</a>
	</div>

	<div class="mb-6">
                <h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
                        <span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
                               Installer {app.name}
                        </span>
               </h1>

		<p class="mt-3 text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
			{app.tagline}
		</p>
	</div>

	{#if form?.error}
		<div class="mb-4 rounded-[18px] border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700 dark:border-red-500/35 dark:bg-red-500/10 dark:text-red-200">
			{form.error}
		</div>
	{/if}

	{#if machines.length === 0}
		<div class="mb-4 rounded-[18px] border border-amber-200 bg-amber-50 px-4 py-4 text-sm text-amber-800 dark:border-amber-500/35 dark:bg-amber-500/10 dark:text-amber-200">
			Aucun serveur pairé trouvé. Va d’abord dans
			<a
				href="/servers"
				class="font-medium text-sky-600 underline-offset-2 hover:underline dark:text-sky-300"
			>
				Mes serveurs
			</a>.
		</div>
	{/if}

	<div class="overflow-hidden rounded-[24px] border border-black/5 bg-white/70 shadow-[0_20px_60px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-[rgba(15,23,42,0.7)] dark:shadow-[0_20px_60px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.04),rgba(255,255,255,0.02))]"></div>

			<form
				method="POST"
				action={`?/createInstallation&app=${encodeURIComponent(app.slug)}`}
				class="relative grid gap-4 p-5 sm:p-6"
			>
				<input type="hidden" name="_csrf" value={data.csrfToken} />
				<input type="hidden" name="app_slug" value={app.slug} />

				<div class="grid gap-2">
					<label for="app" class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Application
					</label>
					<input
						id="app"
						value={app.name}
						disabled
						class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none disabled:cursor-not-allowed disabled:opacity-80 dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white"
					/>
				</div>

				<div class="grid gap-2">
					<label for="machine_id" class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Serveur
					</label>
					<select
						id="machine_id"
						name="machine_id"
						required
						disabled={machines.length === 0}
						class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10 dark:bg-[rgba(15,23,42,0.85)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.95)]"
					>
						<option value="">Sélectionne un serveur</option>
						{#each machines as machine}
							<option value={machine.id} selected={form?.machine_id === machine.id}>
								{machine.hostname || machine.machine_uuid} — {machine.status}
							</option>
						{/each}
					</select>
				</div>

				<div class="grid gap-2">
					<label for="subdomain" class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Sous-domaine
					</label>
					<input
						id="subdomain"
						name="subdomain"
						required
						placeholder={app.slug}
						value={form?.subdomain ?? app.slug}
						class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.85)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.95)]"
					/>
				</div>

				<div class="grid gap-2">
					<label for="auth_type" class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
						Auth
					</label>
					<select
						id="auth_type"
						name="auth_type"
						required
						class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.85)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.95)]"
					>
						{#each authOptions as option}
							<option value={option} selected={(form?.auth_type ?? 'aucune') === option}>
								{option}
							</option>
						{/each}
					</select>
				</div>

				<div class="mt-2 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
					<a
						class="inline-flex items-center justify-center rounded-[16px] border border-black/8 bg-black/[0.04] px-4 py-3 text-sm font-medium text-zinc-700 transition-all duration-200 hover:border-black/12 hover:bg-black/[0.06] hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300 dark:hover:border-white/20 dark:hover:bg-white/[0.07] dark:hover:text-white"
						href="/app-store"
					>
						Annuler
					</a>

					<button
						type="submit"
						disabled={machines.length === 0}
						class="inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(135deg,rgba(14,165,233,0.95),rgba(59,130,246,0.95))] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.26)] disabled:cursor-not-allowed disabled:opacity-60 dark:border-white/10"
					>
						Lancer l’installation
					</button>
				</div>
			</form>
		</div>
	</div>
</section>