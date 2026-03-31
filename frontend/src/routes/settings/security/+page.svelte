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

<div
	style="max-width:920px; margin:0 auto; border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<h1 style="margin-top:0;">Sécurité</h1>
	<p style="color:#cbd5e1; line-height:1.7;">
		Protège ton compte avec la double authentification. Une fois activée, une application TOTP
		te demandera un code à 6 chiffres lors de la connexion.
	</p>

	{#if requiredForAdmin}
		<div
			style="margin:1rem 0 1.25rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.28); color:#fde68a;"
		>
			<strong>Accès admin protégé :</strong> active le 2FA pour pouvoir accéder à l’interface
			admin.
		</div>
	{/if}

	<div
		style="margin:1.25rem 0 1.5rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
	>
		<div>
			<strong>Statut 2FA :</strong>
			{#if enabled}
				<span style="color:#86efac;">Activé</span>
			{:else}
				<span style="color:#fbbf24;">Désactivé</span>
			{/if}
		</div>
	</div>

	{#if !enabled}
		<section
			style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:1.25rem; background:rgba(15,23,42,0.45); margin-bottom:1.25rem;"
		>
			<h2 style="margin-top:0;">Activer le 2FA</h2>

			{#if !setup}
				<form method="POST" action="?/setup">
					<input type="hidden" name="_csrf" value={data.csrfToken} />
					<button
						type="submit"
						style="padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #a855f7); color:white;"
					>
						Générer mon secret 2FA
					</button>
				</form>
			{:else}
				<div
					style="display:grid; grid-template-columns:minmax(220px, 260px) minmax(0,1fr); gap:1.25rem; align-items:start;"
				>
					<div
						style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
					>
						{#if qrDataUrl}
							<img src={qrDataUrl} alt="QR code 2FA" style="width:100%; border-radius:12px;" />
						{:else}
							<p style="color:#94a3b8; margin:0;">QR code indisponible.</p>
						{/if}
					</div>

					<div>
						<p style="margin-top:0; color:#cbd5e1; line-height:1.7;">
							Scanne ce QR code avec ton application 2FA, ou copie le secret ci-dessous.
						</p>

						<div
							style="padding:1rem; border-radius:16px; background:rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.08); margin-bottom:1rem;"
						>
							<div style="color:#94a3b8; margin-bottom:0.45rem;">Secret</div>
							<div style="font-family:monospace; word-break:break-all;">{setup.secret}</div>
						</div>

						<form method="POST" action="?/confirm" style="display:grid; gap:1rem;">
							<input type="hidden" name="_csrf" value={data.csrfToken} />

							<label style="display:grid; gap:0.5rem;">
								<span>Code 2FA</span>
								<input
									name="otp_code"
									type="text"
									inputmode="numeric"
									autocomplete="one-time-code"
									value={form?.otp_code ?? ''}
									placeholder="123456"
									style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
								/>
							</label>

							<button
								type="submit"
								style="padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #22c55e, #16a34a); color:white;"
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
		<section
			style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:1.25rem; background:rgba(15,23,42,0.45);"
		>
			<h2 style="margin-top:0;">Désactiver le 2FA</h2>
			<p style="color:#cbd5e1; line-height:1.7;">
				Pour désactiver la double authentification, confirme ton mot de passe et saisis un code
				2FA valide.
			</p>

			<form method="POST" action="?/disable" style="display:grid; gap:1rem; max-width:520px;">
				<input type="hidden" name="_csrf" value={data.csrfToken} />

				<label style="display:grid; gap:0.5rem;">
					<span>Mot de passe</span>
					<input
						name="password"
						type="password"
						placeholder="••••••••••••"
						style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
					/>
				</label>

				<label style="display:grid; gap:0.5rem;">
					<span>Code 2FA</span>
					<input
						name="otp_code"
						type="text"
						inputmode="numeric"
						autocomplete="one-time-code"
						value={form?.disable_otp_code ?? ''}
						placeholder="123456"
						style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
					/>
				</label>

				<button
					type="submit"
					style="padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #ef4444, #dc2626); color:white;"
				>
					Désactiver le 2FA
				</button>
			</form>
		</section>
	{/if}

	{#if form?.error}
		<p style="color:#fca5a5; margin-top:1rem;">{form.error}</p>
	{/if}

	{#if form?.confirmed}
		<p style="color:#86efac; margin-top:1rem;">Le 2FA a bien été activé.</p>
	{/if}

	{#if form?.disabled}
		<p style="color:#86efac; margin-top:1rem;">Le 2FA a bien été désactivé.</p>
	{/if}
</div>