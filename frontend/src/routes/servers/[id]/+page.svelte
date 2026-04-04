<script lang="ts">
	let { data, form } = $props();

	function computeSavedSettings() {
		return {
			username: form?.values?.username ?? data.settings.username ?? '',
			email: form?.values?.email ?? data.settings.email ?? '',
			domain: form?.values?.domain ?? data.settings.domain ?? '',
			oauth_enabled:
				typeof form?.values?.oauth_enabled === 'boolean'
					? form.values.oauth_enabled
					: Boolean(data.settings.oauth_enabled),
			oauth_mail: form?.values?.oauth_mail ?? data.settings.oauth_mail ?? '',

			password_configured: Boolean(data.settings.password_configured),
			cloudflare_login_configured: Boolean(data.settings.cloudflare_login_configured),
			cloudflare_api_key_configured: Boolean(data.settings.cloudflare_api_key_configured),
			oauth_client_configured: Boolean(data.settings.oauth_client_configured),
			oauth_secret_configured: Boolean(data.settings.oauth_secret_configured),

			updated_at: data.settings.updated_at ?? null
		};
	}

	let savedSettings = $derived(computeSavedSettings());

	const isInstalled = Boolean(data.machine.ssdv2_installed);
	const latestSsdv2Job = data.latestSsdv2Job ?? null;

	let settings = $state({
		username: '',
		email: '',
		domain: '',

		password: '',
		cloudflare_login: '',
		cloudflare_api_key: '',

		oauth_enabled: false,
		oauth_client: '',
		oauth_secret: '',
		oauth_mail: ''
	});

	let secretTouched = $state({
		password: false,
		cloudflare_login: false,
		cloudflare_api_key: false,
		oauth_client: false,
		oauth_secret: false
	});

	let lastHydrationKey = '';

	$effect(() => {
		const key = JSON.stringify({
			updated_at: savedSettings.updated_at,
			saveSuccess: data.saveSuccess,
			error: form?.error ?? null,
			username: savedSettings.username,
			email: savedSettings.email,
			domain: savedSettings.domain,
			oauth_enabled: savedSettings.oauth_enabled,
			oauth_mail: savedSettings.oauth_mail,
			password_configured: savedSettings.password_configured,
			cloudflare_login_configured: savedSettings.cloudflare_login_configured,
			cloudflare_api_key_configured: savedSettings.cloudflare_api_key_configured,
			oauth_client_configured: savedSettings.oauth_client_configured,
			oauth_secret_configured: savedSettings.oauth_secret_configured
		});

		if (key === lastHydrationKey) return;
		lastHydrationKey = key;

		settings.username = savedSettings.username;
		settings.email = savedSettings.email;
		settings.domain = savedSettings.domain;

		settings.password = '';
		settings.cloudflare_login = '';
		settings.cloudflare_api_key = '';

		settings.oauth_enabled = savedSettings.oauth_enabled;
		settings.oauth_client = '';
		settings.oauth_secret = '';
		settings.oauth_mail = savedSettings.oauth_mail;

		secretTouched.password = false;
		secretTouched.cloudflare_login = false;
		secretTouched.cloudflare_api_key = false;
		secretTouched.oauth_client = false;
		secretTouched.oauth_secret = false;
	});

	function normalizeString(value: unknown) {
		return String(value ?? '').trim();
	}

	function normalizeBoolean(value: unknown) {
		return value === true || value === 'true' || value === '1' || value === 'on';
	}

	function hasTypedSecret(value: unknown) {
		return normalizeString(value).length > 0;
	}

	function configuredOrTyped(configured: boolean, typedValue: unknown, touched = false) {
		return configured || (touched && hasTypedSecret(typedValue));
	}

	function humanJobStatus(status: unknown) {
		switch (String(status ?? '').toLowerCase()) {
			case 'pending':
				return 'En attente';
			case 'claimed':
				return 'Préparation';
			case 'running':
				return 'Installation en cours';
			case 'completed':
				return 'Terminée';
			case 'failed':
				return 'Échec';
			default:
				return String(status ?? 'Inconnu');
		}
	}

	function isCurrentSettingsReady(values: Record<string, unknown>) {
		const baseReady =
			normalizeString(values.username).length > 0 &&
			normalizeString(values.email).length > 0 &&
			normalizeString(values.domain).length > 0 &&
			configuredOrTyped(savedSettings.password_configured, values.password, secretTouched.password) &&
			configuredOrTyped(
				savedSettings.cloudflare_login_configured,
				values.cloudflare_login,
				secretTouched.cloudflare_login
			) &&
			configuredOrTyped(
				savedSettings.cloudflare_api_key_configured,
				values.cloudflare_api_key,
				secretTouched.cloudflare_api_key
			);

		if (!baseReady) return false;

		if (normalizeBoolean(values.oauth_enabled)) {
			return (
				normalizeString(values.oauth_mail).length > 0 &&
				configuredOrTyped(
					savedSettings.oauth_client_configured,
					values.oauth_client,
					secretTouched.oauth_client
				) &&
				configuredOrTyped(
					savedSettings.oauth_secret_configured,
					values.oauth_secret,
					secretTouched.oauth_secret
				)
			);
		}

		return true;
	}

	function isSavedSettingsReady(saved: typeof savedSettings) {
		const baseReady =
			normalizeString(saved.username).length > 0 &&
			normalizeString(saved.email).length > 0 &&
			normalizeString(saved.domain).length > 0 &&
			Boolean(saved.password_configured) &&
			Boolean(saved.cloudflare_login_configured) &&
			Boolean(saved.cloudflare_api_key_configured);

		if (!baseReady) return false;

		if (normalizeBoolean(saved.oauth_enabled)) {
			return (
				normalizeString(saved.oauth_mail).length > 0 &&
				Boolean(saved.oauth_client_configured) &&
				Boolean(saved.oauth_secret_configured)
			);
		}

		return true;
	}

	function hasUnsavedChanges(current: typeof settings, saved: typeof savedSettings) {
		return (
			normalizeString(current.username) !== normalizeString(saved.username) ||
			normalizeString(current.email) !== normalizeString(saved.email) ||
			normalizeString(current.domain) !== normalizeString(saved.domain) ||
			normalizeBoolean(current.oauth_enabled) !== normalizeBoolean(saved.oauth_enabled) ||
			normalizeString(current.oauth_mail) !== normalizeString(saved.oauth_mail) ||
			(secretTouched.password && hasTypedSecret(current.password)) ||
			(secretTouched.cloudflare_login && hasTypedSecret(current.cloudflare_login)) ||
			(secretTouched.cloudflare_api_key && hasTypedSecret(current.cloudflare_api_key)) ||
			(secretTouched.oauth_client && hasTypedSecret(current.oauth_client)) ||
			(secretTouched.oauth_secret && hasTypedSecret(current.oauth_secret))
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

	function statusText(configured: boolean, typedValue: unknown, touched = false) {
		if (touched && hasTypedSecret(typedValue)) return 'Nouvelle valeur saisie';
		return configured ? 'Déjà configuré' : 'Non configuré';
	}

	function statusClass(configured: boolean, typedValue: unknown, touched = false) {
		if (touched && hasTypedSecret(typedValue)) {
			return 'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300';
		}

		if (configured) {
			return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
		}

		return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
	}

	const savedConfigReady = $derived(isSavedSettingsReady(savedSettings));
	const currentConfigReady = $derived(isCurrentSettingsReady(settings));
	const unsavedChanges = $derived(hasUnsavedChanges(settings, savedSettings));
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

				{#if data.saveSuccess}
					<div class="mb-6 rounded-[20px] border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300">
						Configuration sauvegardée avec succès.
					</div>
				{/if}

				{#if form?.error}
					<div class="mb-6 rounded-[20px] border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
						{form.error}
					</div>
				{/if}

				{#if form?.installError}
					<div class="mb-6 rounded-[20px] border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 dark:border-red-500/20 dark:bg-red-500/10 dark:text-red-300">
						{form.installError}
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
								{#if latestSsdv2Job}
									Dernier suivi disponible : {humanJobStatus(latestSsdv2Job.status)}.
								{:else if isInstalled}
									SSDv2 est déjà détecté sur ce serveur.
								{:else if savedConfigReady}
									Le serveur peut maintenant recevoir SSDv2.
								{:else}
									Le bouton d’installation restera désactivé tant que la config n’est pas sauvegardée.
								{/if}
							</p>
						</div>

						<div class={`rounded-[18px] border px-4 py-4 ${
							unsavedChanges
								? 'border-amber-200 bg-amber-50/80 dark:border-amber-500/20 dark:bg-amber-500/10'
								: 'border-emerald-200 bg-emerald-50/80 dark:border-emerald-500/20 dark:bg-emerald-500/10'
						}`}>
							<p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
								État du formulaire
							</p>
							<p class={`mt-1 text-sm font-semibold ${
								unsavedChanges
									? 'text-amber-700 dark:text-amber-300'
									: 'text-emerald-700 dark:text-emerald-300'
							}`}>
								{unsavedChanges ? 'Modifications non sauvegardées' : 'Synchronisé avec le serveur'}
							</p>
							<p class="mt-1 text-xs text-zinc-600 dark:text-zinc-300">
								{#if unsavedChanges}
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

				<form id="configuration" method="POST" action="?/save" class="grid gap-4 sm:grid-cols-2" autocomplete="off">
					<input type="hidden" name="_csrf" value={data.csrfToken} />

					<div class="sm:col-span-2">
						<div class="mb-2 inline-flex items-center rounded-full border border-black/5 bg-black/[0.03] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300">
							Étape 1 · Configuration
						</div>
						<p class="text-sm text-zinc-600 dark:text-zinc-400">
							Complète d’abord ces champs, puis sauvegarde-les. Les secrets existants ne sont plus affichés en clair.
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

					<div class="rounded-[22px] border border-white/20 bg-white/60 p-4 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="password"
							name="password"
							type="password"
							bind:value={settings.password}
							autocomplete="new-password"
							data-1p-ignore
							data-lpignore="true"
							placeholder="Nouveau mot de passe"
							class="w-full bg-transparent text-sm text-gray-800 outline-none dark:text-gray-100"
							oninput={() => (secretTouched.password = true)}
						/>
						<div class="mt-3 flex items-center justify-between gap-3">
							<span class={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(savedSettings.password_configured, settings.password, secretTouched.password)}`}>
								{statusText(savedSettings.password_configured, settings.password, secretTouched.password)}
							</span>
							<span class="text-xs text-zinc-500 dark:text-zinc-400">
								Laisse vide pour conserver l’existant
							</span>
						</div>
					</div>

					<div class="rounded-[22px] border border-white/20 bg-white/60 p-4 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
						<input
							id="cloudflare_login"
							name="cloudflare_login"
							type="email"
							bind:value={settings.cloudflare_login}
							autocomplete="off"
							data-1p-ignore
							data-lpignore="true"
							placeholder="Nouveau Cloudflare Mail"
							class="w-full bg-transparent text-sm text-gray-800 outline-none dark:text-gray-100"
							oninput={() => (secretTouched.cloudflare_login = true)}
						/>
						<div class="mt-3 flex items-center justify-between gap-3">
							<span class={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(savedSettings.cloudflare_login_configured, settings.cloudflare_login, secretTouched.cloudflare_login)}`}>
								{statusText(savedSettings.cloudflare_login_configured, settings.cloudflare_login, secretTouched.cloudflare_login)}
							</span>
							<span class="text-xs text-zinc-500 dark:text-zinc-400">
								Laisse vide pour conserver l’existant
							</span>
						</div>
					</div>

					<div class="rounded-[22px] border border-white/20 bg-white/60 p-4 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60 sm:col-span-2">
						<input
							id="cloudflare_api_key"
							name="cloudflare_api_key"
							type="password"
							bind:value={settings.cloudflare_api_key}
							autocomplete="new-password"
							data-1p-ignore
							data-lpignore="true"
							placeholder="Nouvelle Cloudflare API Key"
							class="w-full bg-transparent text-sm text-gray-800 outline-none dark:text-gray-100"
							oninput={() => (secretTouched.cloudflare_api_key = true)}
						/>
						<div class="mt-3 flex items-center justify-between gap-3">
							<span class={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(savedSettings.cloudflare_api_key_configured, settings.cloudflare_api_key, secretTouched.cloudflare_api_key)}`}>
								{statusText(savedSettings.cloudflare_api_key_configured, settings.cloudflare_api_key, secretTouched.cloudflare_api_key)}
							</span>
							<span class="text-xs text-zinc-500 dark:text-zinc-400">
								Laisse vide pour conserver l’existant
							</span>
						</div>
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
						<div class="rounded-[22px] border border-white/20 bg-white/60 p-4 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
							<input
								id="oauth_client"
								name="oauth_client"
								bind:value={settings.oauth_client}
								autocomplete="off"
								data-1p-ignore
								data-lpignore="true"
								placeholder="Nouveau OAuth Client"
								class="w-full bg-transparent text-sm text-gray-800 outline-none dark:text-gray-100"
								oninput={() => (secretTouched.oauth_client = true)}
							/>
							<div class="mt-3 flex items-center justify-between gap-3">
								<span class={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(savedSettings.oauth_client_configured, settings.oauth_client, secretTouched.oauth_client)}`}>
									{statusText(savedSettings.oauth_client_configured, settings.oauth_client, secretTouched.oauth_client)}
								</span>
								<span class="text-xs text-zinc-500 dark:text-zinc-400">
									Laisse vide pour conserver l’existant
								</span>
							</div>
						</div>

						<div class="rounded-[22px] border border-white/20 bg-white/60 p-4 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60">
							<input
								id="oauth_secret"
								name="oauth_secret"
								type="password"
								bind:value={settings.oauth_secret}
								autocomplete="new-password"
								data-1p-ignore
								data-lpignore="true"
								placeholder="Nouveau OAuth Secret"
								class="w-full bg-transparent text-sm text-gray-800 outline-none dark:text-gray-100"
								oninput={() => (secretTouched.oauth_secret = true)}
							/>
							<div class="mt-3 flex items-center justify-between gap-3">
								<span class={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] ${statusClass(savedSettings.oauth_secret_configured, settings.oauth_secret, secretTouched.oauth_secret)}`}>
									{statusText(savedSettings.oauth_secret_configured, settings.oauth_secret, secretTouched.oauth_secret)}
								</span>
								<span class="text-xs text-zinc-500 dark:text-zinc-400">
									Laisse vide pour conserver l’existant
								</span>
							</div>
						</div>

						<div class="relative rounded-[22px] border border-white/20 bg-white/60 px-4 pb-3 pt-6 shadow-inner backdrop-blur-md transition-all dark:bg-gray-800/60 sm:col-span-2">
							<input
								id="oauth_mail"
								name="oauth_mail"
								type="email"
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
							Les secrets existants sont conservés tant que tu laisses les champs sensibles vides.
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
									SSDv2 est déjà présent sur ce serveur.
								</p>
							{:else if !savedConfigReady}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Complète et sauvegarde d’abord la configuration avant de pouvoir lancer SSDv2.
								</p>
							{:else if unsavedChanges}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Tu as modifié des champs. Sauvegarde-les avant de lancer l’installation pour garantir que le serveur utilisera la bonne configuration.
								</p>
							{:else}
								<p class="mt-2 text-sm leading-7 text-zinc-600 dark:text-zinc-400">
									Le serveur est prêt. La configuration requise est enregistrée et SSDv2 n’est pas encore détecté.
								</p>
							{/if}
						</div>

						<div class="flex flex-col gap-3 lg:items-end">
							{#if latestSsdv2Job}
								<a
									href={`/ssdv2-installations/${latestSsdv2Job.id}`}
									class="text-sm font-medium text-sky-600 no-underline transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
								>
									Voir le suivi SSDv2
								</a>
							{/if}

							<form method="POST" action="?/install">
								<input type="hidden" name="_csrf" value={data.csrfToken} />
								<button
									type="submit"
									disabled={isInstalled || !savedConfigReady || unsavedChanges}
									class="inline-flex items-center justify-center rounded-[16px] px-5 py-3 text-sm font-semibold text-white transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-60
									{isInstalled || !savedConfigReady || unsavedChanges
										? 'bg-zinc-400 shadow-none dark:bg-zinc-700'
										: 'bg-[linear-gradient(90deg,#22c55e,#16a34a)] shadow-[0_12px_30px_rgba(34,197,94,0.18)] hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(34,197,94,0.24)]'}"
								>
									{#if isInstalled}
										Déjà installé
									{:else if !savedConfigReady}
										Compléter puis sauvegarder
									{:else if unsavedChanges}
										Sauvegarder avant installation
									{:else}
										Installer SSDv2
									{/if}
								</button>
							</form>
						</div>
					</div>

					<div class="mt-5 rounded-[18px] border border-black/5 bg-black/[0.03] px-4 py-4 text-sm dark:border-white/10 dark:bg-white/[0.03]">
						{#if isInstalled}
							<p class="font-medium text-zinc-900 dark:text-zinc-100">
								SSDv2 est déjà installé sur ce serveur.
							</p>
							<p class="mt-1 text-zinc-600 dark:text-zinc-400">
								L’installation n’est pas proposée dans cet état.
							</p>
						{:else if !savedConfigReady}
							<p class="font-medium text-zinc-900 dark:text-zinc-100">Configuration incomplète.</p>
							<p class="mt-1 text-zinc-600 dark:text-zinc-400">
								Renseigne tous les champs requis, puis clique sur “Sauvegarder la configuration”.
							</p>
						{:else if unsavedChanges}
							<p class="font-medium text-zinc-900 dark:text-zinc-100">
								Des changements ne sont pas encore sauvegardés.
							</p>
							<p class="mt-1 text-zinc-600 dark:text-zinc-400">
								L’installation utilisera uniquement la configuration enregistrée côté serveur.
							</p>
						{:else}
							<p class="font-medium text-zinc-900 dark:text-zinc-100">
								Le serveur est prêt pour l’installation.
							</p>
							<p class="mt-1 text-zinc-600 dark:text-zinc-400">
								Le bouton lancera le job SSDv2, puis tu seras redirigé vers la page de suivi dédiée.
							</p>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>