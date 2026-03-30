<script lang="ts">
	let { data, form } = $props();

	const pairing = $derived(form?.pairing ?? data.pairing);
	const pairingCode = $derived(pairing?.pairing_code ?? '-');
	const machineUuid = $derived(pairing?.machine_uuid ?? '-');
	const backendUrl = $derived(data.backendUrl ?? 'http://127.0.0.1:8000');

	const bootstrapCommand = $derived(
		pairing
			? `curl -fsSL ${backendUrl}/bootstrap.sh | sudo bash -s -- --pairing-code ${pairing.pairing_code} --backend-url ${backendUrl}`
			: ''
	);
</script>

<svelte:head>
	<title>Ajouter un serveur</title>
</svelte:head>

<div
	style="max-width:980px; margin:0 auto; border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<p style="margin-top:0;">
		<a href="/servers" style="color:#93c5fd; text-decoration:none;">← Retour aux serveurs</a>
	</p>

	<h1 style="margin-bottom:0.5rem;">Ajouter un serveur</h1>
	<p style="color:#cbd5e1; line-height:1.7; max-width:52rem;">
		Connecte un VPS à la plateforme en lançant le bootstrap ci-dessous sur le serveur distant.
	</p>

	<div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1.5rem 0;">
		<div
			style="padding:1rem 1.1rem; border-radius:20px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
		>
			<div style="color:#94a3b8; font-size:0.9rem;">Code de connexion</div>
			<div style="font-size:1.8rem; font-weight:800; letter-spacing:0.08em; margin-top:0.35rem;">
				{pairingCode}
			</div>
		</div>

		<div
			style="padding:1rem 1.1rem; border-radius:20px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
		>
			<div style="color:#94a3b8; font-size:0.9rem;">Machine UUID pré-enregistrée</div>
			<div style="font-size:1rem; font-weight:700; margin-top:0.45rem; word-break:break-all;">
				{machineUuid}
			</div>
		</div>
	</div>

	<div
		style="padding:1rem 1.1rem; border-radius:20px; background:rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.08); margin-bottom:1rem;"
	>
		<div style="color:#94a3b8; margin-bottom:0.75rem;">Commande bootstrap</div>
		<pre style="margin:0; white-space:pre-wrap; word-break:break-word; color:#e2e8f0; font-family:monospace;">{bootstrapCommand}</pre>
	</div>

	<form method="POST" action="?/regenerate">
		<button
			type="submit"
			style="padding:0.9rem 1.05rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #a855f7); color:white;"
		>
			Générer un nouveau code
		</button>
	</form>

	{#if form?.error}
		<p style="color:#fca5a5; margin-top:1rem;">{form.error}</p>
	{/if}
</div>