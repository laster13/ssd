<script lang="ts">
	let { data, form } = $props();

	const savedSettings = form?.settings ?? data.settings;
	const isInstalled = Boolean(data.machine.ssdv2_installed);

	let settings = $state({
		username: savedSettings.username ?? '',
		email: savedSettings.email ?? '',
		domain: savedSettings.domain ?? '',
		password: savedSettings.password ?? '',
		cloudflare_login: savedSettings.cloudflare_login ?? '',
		cloudflare_api_key: savedSettings.cloudflare_api_key ?? '',
		oauth_enabled: Boolean(savedSettings.oauth_enabled),
		oauth_client: savedSettings.oauth_client ?? '',
		oauth_secret: savedSettings.oauth_secret ?? '',
		oauth_mail: savedSettings.oauth_mail ?? ''
	});

	function normalizeString(value: unknown) {
		return String(value ?? '').trim();
	}

	function normalizeBoolean(value: unknown) {
		return value === true || value === 'true' || value === '1' || value === 'on';
	}

	function isSettingsReady(values: Record<string, unknown>) {
		const baseReady =
			normalizeString(values.username).length > 0 &&
			normalizeString(values.email).length > 0 &&
			normalizeString(values.domain).length > 0 &&
			normalizeString(values.password).length > 0 &&
			normalizeString(values.cloudflare_login).length > 0 &&
			normalizeString(values.cloudflare_api_key).length > 0;

		if (!baseReady) return false;

		if (normalizeBoolean(values.oauth_enabled)) {
			return (
				normalizeString(values.oauth_client).length > 0 &&
				normalizeString(values.oauth_secret).length > 0 &&
				normalizeString(values.oauth_mail).length > 0
			);
		}

		return true;
	}

	function hasUnsavedChanges(
		current: Record<string, unknown>,
		saved: Record<string, unknown>
	) {
		return (
			normalizeString(current.username) !== normalizeString(saved.username) ||
			normalizeString(current.email) !== normalizeString(saved.email) ||
			normalizeString(current.domain) !== normalizeString(saved.domain) ||
			normalizeString(current.password) !== normalizeString(saved.password) ||
			normalizeString(current.cloudflare_login) !== normalizeString(saved.cloudflare_login) ||
			normalizeString(current.cloudflare_api_key) !==
				normalizeString(saved.cloudflare_api_key) ||
			normalizeBoolean(current.oauth_enabled) !== normalizeBoolean(saved.oauth_enabled) ||
			normalizeString(current.oauth_client) !== normalizeString(saved.oauth_client) ||
			normalizeString(current.oauth_secret) !== normalizeString(saved.oauth_secret) ||
			normalizeString(current.oauth_mail) !== normalizeString(saved.oauth_mail)
		);
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

	const savedConfigReady = isSettingsReady(savedSettings);
</script>

<svelte:head>
	<title>Configuration serveur</title>
</svelte:head>

<section class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<p class="mb-5">
					<a
						href="/servers"
						class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						← Retour aux serveurs
					</a>
				</p>

				{#if form?.success}
					<div class="mb-6 rounded-[20px] border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
						Configuration sauvegardée avec succès.
					</div>
				{/if}

				{#if form?.error}
					<div class="mb-6 rounded-[20px] border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
						{form.error}
					</div>
				{/if}

				<div class="mb-6 rounded-[22px] border border-black/5 bg-white/70 p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
					<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
						<div>
							<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
								Configuration serveur
							</h1>

							<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
								{data.machine.hostname ?? 'Serveur sans nom'}
							</p>
						</div>

						<div class={`inline-flex w-fit items-center gap-2 rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] ${
							isInstalled
								? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300'
								: 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300'
						}`}>
							<span class={`h-2 w-2 rounded-full ${isInstalled ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
							{isInstalled ? 'SSDv2 installé' : 'Non installé'}
						</div>
					</div>

					<div class="mt-5 grid gap-3 md:grid-cols-3">
						<div class={`rounded-[18px] border px-4 py-4 ${
							savedConfigReady
								? 'border-emerald-200 bg-emerald-50/80 dark:border-emerald-500/20 dark:bg-emerald-500/10'
								: 'border-amber-200 bg-amber-50/80 dark:border-amber-500/20 dark:bg-amber-500/10'
						}`}>
							<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
								Étape 1
							</p>
							<p class={`mt-1 text-sm font-semibold ${
								savedConfigReady
									? 'text-emerald-700 dark:text-emerald-300'
									: 'text-amber-700 dark:text-amber-300'
							}`}>
								{savedConfigReady ? 'Configuration prête' : 'Configuration à compléter'}
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								Renseigne puis sauvegarde les champs nécessaires avant installation.
							</p>
						</div>

						<div class={`rounded-[18px] border px-4 py-4 ${
							isInstalled
								? 'border-emerald-200 bg-emerald-50/80 dark:border-emerald-500/20 dark:bg-emerald-500/10'
								: savedConfigReady
									? 'border-sky-200 bg-sky-50/80 dark:border-sky-500/20 dark:bg-sky-500/10'
									: 'border-zinc-200 bg-zinc-50/80 dark:border-white/10 dark:bg-white/[0.03]'
						}`}>
							<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
								Étape 2
							</p>
							<p class={`mt-1 text-sm font-semibold ${
								isInstalled
									? 'text-emerald-700 dark:text-emerald-300'
									: savedConfigReady
										? 'text-sky-700 dark:text-sky-300'
										: 'text-zinc-700 dark:text-zinc-200'
							}`}>
								{#if isInstalled}
									Installation déjà présente
								{:else if savedConfigReady}
									Prêt pour l’installation
								{:else}
									Installation bloquée
								{/if}
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								{#if isInstalled}
									SSDv2 est déjà détecté sur ce serveur.
								{:else if savedConfigReady}
									Le serveur peut maintenant recevoir SSDv2.
								{:else}
									Le bouton d’installation restera désactivé tant que la config n’est pas sauvegardée.
								{/if}
							</p>
						</div>

						<div class={`rounded-[18px] border px-4 py-4 ${
							hasUnsavedChanges(settings, savedSettings)
								? 'border-amber-200 bg-amber-50/80 dark:border-amber-500/20 dark:bg-amber-500/10'
								: 'border-emerald-200 bg-emerald-50/80 dark:border-emerald-500/20 dark:bg-emerald-500/10'
						}`}>
							<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
								État du formulaire
							</p>
							<p class={`mt-1 text-sm font-semibold ${
								hasUnsavedChanges(settings, savedSettings)
									? 'text-amber-700 dark:text-amber-300'
									: 'text-emerald-700 dark:text-emerald-300'
							}`}>
								{hasUnsavedChanges(settings, savedSettings)
									? 'Modifications non sauvegardées'
									: 'Synchronisé avec le serveur'}
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								{#if hasUnsavedChanges(settings, savedSettings)}
									Sauvegarde tes changements avant de pouvoir poursuivre.
								{:else}
									Les valeurs affichées correspondent à la configuration enregistrée.
								{/if}
							</p>
						</div>
					</div>

					<div class="mt-5 grid gap-3 sm:grid-cols-2">
						<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.03] px-4 py-3 text-sm dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-zinc-500 dark:text-zinc-400">ID</span>
							<strong class="text-right font-medium text-zinc-900 dark:text-zinc-100">
								{data.machine.id}
							</strong>
						</div>

						<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.03] px-4 py-3 text-sm dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-zinc-500 dark:text-zinc-400">UUID machine</span>
							<strong class="text-right font-medium text-zinc-900 dark:text-zinc-100">
								{data.machine.machine_uuid}
							</strong>
						</div>

						<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.03] px-4 py-3 text-sm dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-zinc-500 dark:text-zinc-400">Statut</span>
							<strong class="text-right font-medium text-zinc-900 dark:text-zinc-100">
								{data.machine.status ?? '-'}
							</strong>
						</div>

						<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.03] px-4 py-3 text-sm dark:border-white/10 dark:bg-white/[0.03]">
							<span class="text-zinc-500 dark:text-zinc-400">Agent</span>
							<strong class="text-right font-medium text-zinc-900 dark:text-zinc-100">
								{data.machine.agent_version ?? '-'}
							</strong>
						</div>

						<div class="flex items-start justify-between gap-3 rounded-[16px] border border-black/5 bg-black/[0.03] px-4 py-3 text-sm dark:border-white/10 dark:bg-white/[0.03] sm:col-span-2">
							<span class="text-zinc-500 dark:text-zinc-400">Dernier contact</span>
							<strong class="text-right font-medium text-zinc-900 dark:text-zinc-100">
								{formatDate(data.machine.last_seen_at)}
							</strong>
						</div>
					</div>
				</div>

				<form id="configuration" method="POST" action="?/save" class="grid gap-4 sm:grid-cols-2">
					<input type="hidden" name="_csrf" value={data.csrfToken} />

					<div class="sm:col-span-2">
						<div class="mb-2 inline-flex items-center rounded-full border border-black/5 bg-black/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
							Étape 1 · Configuration
						</div>
						<p class="text-sm text-zinc-600 dark:text-zinc-400">
							Complète d’abord ces champs, puis sauvegarde-les. L’installation ne sera proposée qu’après enregistrement.
						</p>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="username"
							name="username"
							bind:value={settings.username}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="username"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Username
						</label>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="email"
							name="email"
							type="email"
							bind:value={settings.email}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="email"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Email
						</label>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="domain"
							name="domain"
							bind:value={settings.domain}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="domain"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Domaine
						</label>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="password"
							name="password"
							type="password"
							bind:value={settings.password}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="password"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Password
						</label>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="cloudflare_login"
							name="cloudflare_login"
							bind:value={settings.cloudflare_login}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="cloudflare_login"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Cloudflare Mail
						</label>
					</div>

					<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="cloudflare_api_key"
							name="cloudflare_api_key"
							type="password"
							bind:value={settings.cloudflare_api_key}
							placeholder=" "
							class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
						/>
						<label
							for="cloudflare_api_key"
							class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
						>
							Cloudflare API Key
						</label>
					</div>

					<div
						role="switch"
						tabindex="0"
						aria-checked={settings.oauth_enabled}
						class="cursor-pointer select-none rounded-[22px] border border-white/10 bg-white/60 p-5 shadow-inner transition-all hover:bg-white/80 dark:bg-gray-800/60 dark:hover:bg-gray-700/70 sm:col-span-2"
						onclick={() => (settings.oauth_enabled = !settings.oauth_enabled)}
						onkeydown={(e) => {
							if (e.key === 'Enter' || e.key === ' ') {
								e.preventDefault();
								settings.oauth_enabled = !settings.oauth_enabled;
							}
						}}
					>
						<input
							type="hidden"
							name="oauth_enabled"
							value={settings.oauth_enabled ? 'true' : 'false'}
						/>

						<div class="flex items-center justify-between">
							<div>
								<div class="text-sm font-medium text-gray-700 dark:text-gray-200">OAuth</div>
								<p class="mt-1 text-xs text-gray-500">
									Activez OAuth si vous utilisez une authentification externe.
								</p>
							</div>

							<button
								type="button"
								aria-pressed={settings.oauth_enabled}
								class={`h-6 w-12 rounded-full p-1 transition ${settings.oauth_enabled ? 'bg-[linear-gradient(90deg,#f59e0b,#f97316,#ec4899)]' : 'bg-gray-300 dark:bg-gray-600'}`}
								onclick={(e) => {
									e.stopPropagation();
									settings.oauth_enabled = !settings.oauth_enabled;
								}}
							>
								<div class={`h-4 w-4 rounded-full bg-white shadow-md transition ${settings.oauth_enabled ? 'translate-x-6' : ''}`}></div>
							</button>
						</div>
					</div>

					{#if settings.oauth_enabled}
						<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
							<input
								id="oauth_client"
								name="oauth_client"
								bind:value={settings.oauth_client}
								placeholder=" "
								class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
							/>
							<label
								for="oauth_client"
								class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
							>
								OAuth Client
							</label>
						</div>

						<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
							<input
								id="oauth_secret"
								name="oauth_secret"
								type="password"
								bind:value={settings.oauth_secret}
								placeholder=" "
								class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
							/>
							<label
								for="oauth_secret"
								class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
							>
								OAuth Secret
							</label>
						</div>

						<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60 sm:col-span-2">
							<input
								id="oauth_mail"
								name="oauth_mail"
								bind:value={settings.oauth_mail}
								placeholder=" "
								class="peer w-full bg-transparent text-sm text-gray-800 outline-none placeholder-transparent dark:text-gray-100"
							/>
							<label
								for="oauth_mail"
								class="pointer-events-none absolute left-4 top-2 text-[11px] uppercase tracking-[0.12em] text-gray-400 transition-all duration-200 peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2 peer-focus:text-[11px] peer-focus:uppercase peer-focus:tracking-[0.12em] peer-focus:text-cyan-500 peer-not-placeholder-shown:top-2 peer-not-placeholder-shown:text-[11px] peer-not-placeholder-shown:uppercase peer-not-placeholder-shown:tracking-[0.12em] peer-not-placeholder-shown:text-cyan-500"
							>
								OAuth Mail
							</label>
						</div>
					{/if}

					<div class="mt-4 flex items-center justify-between gap-4 border-t border-black/5 pt-5 dark:border-white/10 sm:col-span-2">
						<p class="text-xs text-zinc-500 dark:text-zinc-400">
							Enregistre d’abord cette configuration. L’installation ne sera possible qu’à partir des valeurs sauvegardées.
						</p>

						<button
							type="submit"
							class="inline-flex items-center justify-center rounded-[16px] bg-[linear-gradient(90deg,#38bdf8,#2563eb)] px-5 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.28)]"
						>
							Sauvegarder la configuration
						</button>
					</div>
				</form>

				<div
					id="installation"
					class="mt-8 rounded-[24px] border border-black/5 bg-white/60 p-5 shadow-[0_10px_30px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[0_10px_30px_rgba(0,0,0,0.20)]"
				>
					<div class="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
						<div class="max-w-2xl">
							<div class="mb-2 inline-flex items-center rounded-full border border-black/5 bg-black/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
								Étape 2 · Installation
							</div>

							<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
								Installation SSDv2
							</h2>

							{#if isInstalled}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									SSDv2 est déjà présent sur ce serveur. Tu peux continuer à gérer la configuration sans relancer l’installation.
								</p>
							{:else if !savedConfigReady}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Complète et sauvegarde d’abord la configuration avant de pouvoir lancer SSDv2.
								</p>
							{:else if hasUnsavedChanges(settings, savedSettings)}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Tu as modifié des champs. Sauvegarde-les avant de lancer l’installation pour garantir que le serveur utilisera la bonne configuration.
								</p>
							{:else}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Le serveur est prêt. La configuration requise est enregistrée et SSDv2 n’est pas encore détecté.
								</p>
							{/if}
						</div>

						<div class="flex flex-col gap-3 sm:flex-row">
							<a
								href="#configuration"
								class="inline-flex items-center justify-center rounded-[16px] border border-zinc-200 bg-white px-5 py-3 text-sm font-semibold text-zinc-800 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_12px_30px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.05] dark:text-white"
							>
								Revoir la configuration
							</a>

							<button
								type="button"
								disabled={isInstalled || !savedConfigReady || hasUnsavedChanges(settings, savedSettings)}
								class={`inline-flex items-center justify-center rounded-[16px] px-5 py-3 text-sm font-semibold text-white transition-all duration-200 ${
									isInstalled || !savedConfigReady || hasUnsavedChanges(settings, savedSettings)
										? 'cursor-not-allowed bg-zinc-300 text-zinc-600 opacity-70 dark:bg-zinc-700 dark:text-zinc-300'
										: 'bg-[linear-gradient(90deg,#f59e0b,#f97316)] shadow-[0_12px_30px_rgba(249,115,22,0.20)] hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(249,115,22,0.28)]'
								}`}
							>
								{#if isInstalled}
									Déjà installé
								{:else if !savedConfigReady}
									Compléter puis sauvegarder
								{:else if hasUnsavedChanges(settings, savedSettings)}
									Sauvegarder avant installation
								{:else}
									Installer SSDv2
								{/if}
							</button>
						</div>
					</div>

					<div class="mt-4 rounded-[18px] border px-4 py-4 ${
						isInstalled
							? 'border-emerald-200 bg-emerald-50/80 dark:border-emerald-500/20 dark:bg-emerald-500/10'
							: !savedConfigReady || hasUnsavedChanges(settings, savedSettings)
								? 'border-amber-200 bg-amber-50/80 dark:border-amber-500/20 dark:bg-amber-500/10'
								: 'border-sky-200 bg-sky-50/80 dark:border-sky-500/20 dark:bg-sky-500/10'
					}">
						{#if isInstalled}
							<p class="text-sm font-semibold text-emerald-700 dark:text-emerald-300">
								SSDv2 est déjà installé sur ce serveur.
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								L’installation n’est pas proposée dans cet état.
							</p>
						{:else if !savedConfigReady}
							<p class="text-sm font-semibold text-amber-700 dark:text-amber-300">
								Configuration incomplète.
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								Renseigne tous les champs requis, puis clique sur “Sauvegarder la configuration”.
							</p>
						{:else if hasUnsavedChanges(settings, savedSettings)}
							<p class="text-sm font-semibold text-amber-700 dark:text-amber-300">
								Des changements ne sont pas encore sauvegardés.
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								L’installation utilisera uniquement la configuration enregistrée côté serveur.
							</p>
						{:else}
							<p class="text-sm font-semibold text-sky-700 dark:text-sky-300">
								Le serveur est prêt pour l’installation.
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								Le bouton est maintenant disponible. Tu pourras brancher ensuite l’action backend réelle sur ce CTA.
							</p>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>