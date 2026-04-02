<script lang="ts">
	let { data, form } = $props();

	const app = data.app;
	const machines = data.machines ?? [];
</script>

<svelte:head>
	<title>Installer {app.name}</title>
</svelte:head>

<section class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/app-store"
						class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						← Retour à l’App Store
					</a>
				</p>

				<div class="mb-5 flex items-start gap-4">
					<div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-[20px] border border-black/5 bg-black/[0.03] dark:border-white/10 dark:bg-white/[0.06]">
						<img src={app.icon} alt={app.name} class="h-9 w-9 object-contain" />
					</div>

					<div class="min-w-0">
						<h1 class="mb-1 text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
							Installer {app.name}
						</h1>

						<p class="m-0 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
							{app.description}
						</p>
					</div>
				</div>

				<div class="mb-6 rounded-[18px] border border-sky-200 bg-sky-50 px-4 py-4 text-sky-900 dark:border-sky-500/20 dark:bg-sky-500/[0.08] dark:text-sky-100">
					Application sélectionnée : <strong>{app.name}</strong>
					<span class="ml-1 text-sky-700 dark:text-sky-300">({app.slug})</span>
				</div>

				<form method="POST" action="?/install" class="grid gap-4">
					<input type="hidden" name="_csrf" value={data.csrfToken} />

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">Serveur cible</span>
						<select
							name="machine_id"
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						>
							<option value="">Choisir un serveur</option>
							{#each machines as machine}
								<option value={machine.id} selected={form?.machine_id === machine.id}>
									{machine.hostname ?? machine.id} — {machine.status}
								</option>
							{/each}
						</select>
					</label>

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">Sous-domaine</span>
						<input
							name="subdomain"
							value={form?.subdomain ?? app.slug}
							placeholder={app.slug}
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						/>
					</label>

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">Authentification</span>
						<select
							name="auth_type"
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						>
							<option value="basique" selected={!form?.auth_type || form?.auth_type === 'basique'}>
								basique
							</option>
							<option value="oauth" selected={form?.auth_type === 'oauth'}>oauth</option>
							<option value="authelia" selected={form?.auth_type === 'authelia'}>authelia</option>
							<option value="aucune" selected={form?.auth_type === 'aucune'}>aucune</option>
							<option value="oauth2-proxy" selected={form?.auth_type === 'oauth2-proxy'}>
								oauth2-proxy
							</option>
						</select>
					</label>

					<button
						type="submit"
						class="mt-2 inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#a855f7)] px-4 py-4 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(59,130,246,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(59,130,246,0.26)] dark:border-white/10"
					>
						Lancer l’installation de {app.name}
					</button>
				</form>

				{#if form?.error}
					<p class="mt-5 text-sm font-medium text-red-600 dark:text-red-300">{form.error}</p>
				{/if}
			</div>
		</div>
	</div>
</section>