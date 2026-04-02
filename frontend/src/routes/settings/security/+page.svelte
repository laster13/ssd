<script lang="ts">
	import { onMount } from 'svelte';
	import QRCode from 'qrcode';

	let { data, form } = $props();

	const enabled = $derived(
		form?.confirmed ? true : form?.disabled ? false : data.status?.enabled ?? false
	);

	const setup = $derived(form?.setup ?? null);
	const requiredForAdmin = $derived(data.required === 'admin-2fa');

	let qrDataUrl = $state('');

	onMount(async () => {
		if (setup?.otpauth_url) {
			try {
				qrDataUrl = await QRCode.toDataURL(setup.otpauth_url);
			} catch {
				qrDataUrl = '';
			}
		}
	});
</script>

<svelte:head>
	<title>Sécurité</title>
</svelte:head>

<section class="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<div class="mb-6">
					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						Sécurité
					</div>

					<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Sécurité
					</h1>

					<p class="mt-3 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Protège ton compte avec la double authentification. Une fois activée, une
						application TOTP te demandera un code à 6 chiffres lors de la connexion.
					</p>
				</div>

				{#if requiredForAdmin}
					<div class="mb-5 rounded-[18px] border border-amber-200 bg-amber-50 px-4 py-4 text-amber-800 dark:border-amber-500/28 dark:bg-amber-500/[0.08] dark:text-amber-200">
						<strong>Accès admin protégé :</strong> active le 2FA pour pouvoir accéder à
						l’interface admin.
					</div>
				{/if}

				<div class="mb-6 rounded-[18px] border border-black/5 bg-white/70 px-4 py-4 dark:border-white/10 dark:bg-white/[0.04]">
					<div class="text-sm text-zinc-700 dark:text-zinc-300">
						<strong>Statut 2FA :</strong>
						{#if enabled}
							<span class="ml-2 font-semibold text-emerald-600 dark:text-emerald-300">Activé</span>
						{:else}
							<span class="ml-2 font-semibold text-amber-600 dark:text-amber-300">Désactivé</span>
						{/if}
					</div>
				</div>

				{#if !enabled}
					<section class="mb-5 rounded-[22px] border border-black/5 bg-white/60 p-5 dark:border-white/10 dark:bg-[rgba(15,23,42,0.45)]">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Activer le 2FA
						</h2>

						{#if !setup}
							<form method="POST" action="?/setup" class="mt-4">
								<input type="hidden" name="_csrf" value={data.csrfToken} />
								<button
									type="submit"
									class="inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#a855f7)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(59,130,246,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(59,130,246,0.26)] dark:border-white/10"
								>
									Générer mon secret 2FA
								</button>
							</form>
						{:else}
							<div class="mt-5 grid gap-5 lg:grid-cols-[minmax(220px,260px)_minmax(0,1fr)] lg:items-start">
								<div class="rounded-[18px] border border-black/5 bg-white/70 p-4 dark:border-white/10 dark:bg-white/[0.04]">
									{#if qrDataUrl}
										<img src={qrDataUrl} alt="QR code 2FA" class="w-full rounded-[12px]" />
									{:else}
										<p class="m-0 text-sm text-zinc-500 dark:text-zinc-400">
											QR code indisponible.
										</p>
									{/if}
								</div>

								<div>
									<p class="mt-0 text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
										Scanne ce QR code avec ton application 2FA, ou copie le secret
										ci-dessous.
									</p>

									<div class="mb-4 rounded-[16px] border border-black/5 bg-black/[0.03] p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.6)]">
										<div class="mb-2 text-sm text-zinc-500 dark:text-zinc-400">Secret</div>
										<div class="break-all font-mono text-sm text-zinc-900 dark:text-zinc-100">
											{setup.secret}
										</div>
									</div>

									<form method="POST" action="?/confirm" class="grid gap-4">
										<input type="hidden" name="_csrf" value={data.csrfToken} />

										<label class="grid gap-2">
											<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
												Code 2FA
											</span>
											<input
												name="otp_code"
												type="text"
												inputmode="numeric"
												autocomplete="one-time-code"
												value={form?.otp_code ?? ''}
												placeholder="123456"
												class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
											/>
										</label>

										<button
											type="submit"
											class="inline-flex items-center justify-center rounded-[16px] border border-emerald-200 bg-[linear-gradient(90deg,#22c55e,#16a34a)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(34,197,94,0.18)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(34,197,94,0.24)] dark:border-white/10"
										>
											Confirmer l’activation
										</button>
									</form>
								</div>
							</div>
						{/if}
					</section>
				{/if}

				{#if enabled}
					<section class="rounded-[22px] border border-black/5 bg-white/60 p-5 dark:border-white/10 dark:bg-[rgba(15,23,42,0.45)]">
						<h2 class="text-xl font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
							Désactiver le 2FA
						</h2>
						<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
							Pour désactiver la double authentification, confirme ton mot de passe et
							saisis un code 2FA valide.
						</p>

						<form method="POST" action="?/disable" class="mt-5 grid max-w-[520px] gap-4">
							<input type="hidden" name="_csrf" value={data.csrfToken} />

							<label class="grid gap-2">
								<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
									Mot de passe
								</span>
								<input
									name="password"
									type="password"
									placeholder="••••••••••••"
									class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
								/>
							</label>

							<label class="grid gap-2">
								<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
									Code 2FA
								</span>
								<input
									name="otp_code"
									type="text"
									inputmode="numeric"
									autocomplete="one-time-code"
									value={form?.disable_otp_code ?? ''}
									placeholder="123456"
									class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
								/>
							</label>

							<button
								type="submit"
								class="inline-flex items-center justify-center rounded-[16px] border border-red-200 bg-[linear-gradient(90deg,#ef4444,#dc2626)] px-4 py-3 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(239,68,68,0.18)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(239,68,68,0.24)] dark:border-white/10"
							>
								Désactiver le 2FA
							</button>
						</form>
					</section>
				{/if}

				{#if form?.error}
					<p class="mt-5 text-sm font-medium text-red-600 dark:text-red-300">{form.error}</p>
				{/if}

				{#if form?.confirmed}
					<p class="mt-5 text-sm font-medium text-emerald-600 dark:text-emerald-300">
						Le 2FA a bien été activé.
					</p>
				{/if}

				{#if form?.disabled}
					<p class="mt-5 text-sm font-medium text-emerald-600 dark:text-emerald-300">
						Le 2FA a bien été désactivé.
					</p>
				{/if}
			</div>
		</div>
	</div>
</section>