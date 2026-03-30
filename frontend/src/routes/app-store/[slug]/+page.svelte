<script lang="ts">
	let { data, form } = $props();

	const app = data.app;
	const machines = data.machines ?? [];
</script>

<svelte:head>
	<title>Installer {app.name}</title>
</svelte:head>

<div
	style="max-width:860px; margin:0 auto; border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<p style="margin-top:0;">
		<a href="/app-store" style="color:#93c5fd; text-decoration:none;">← Retour à l’App Store</a>
	</p>

	<div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
		<div
			style="width:64px; height:64px; border-radius:20px; display:grid; place-items:center; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08);"
		>
			<img src={app.icon} alt={app.name} style="width:36px; height:36px; object-fit:contain;" />
		</div>

		<div>
			<h1 style="margin:0 0 0.35rem 0;">Installer {app.name}</h1>
			<p style="margin:0; color:#cbd5e1; line-height:1.6;">{app.description}</p>
		</div>
	</div>

	<div
		style="margin:1.25rem 0 1.5rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.16); color:#cfefff;"
	>
		Application sélectionnée : <strong>{app.name}</strong>
		<span style="color:#7dd3fc;">({app.slug})</span>
	</div>

	<form method="POST" action="?/install" style="display:grid; gap:1rem;">
		<label style="display:grid; gap:0.5rem;">
			<span>Serveur cible</span>
			<select
				name="machine_id"
				style="padding:0.9rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
			>
				<option value="">Choisir un serveur</option>
				{#each machines as machine}
					<option value={machine.id} selected={form?.machine_id === machine.id}>
						{machine.hostname ?? machine.id} — {machine.status}
					</option>
				{/each}
			</select>
		</label>

		<label style="display:grid; gap:0.5rem;">
			<span>Sous-domaine</span>
			<input
				name="subdomain"
				value={form?.subdomain ?? app.slug}
				placeholder={app.slug}
				style="padding:0.9rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
			/>
		</label>

		<label style="display:grid; gap:0.5rem;">
			<span>Authentification</span>
			<select
				name="auth_type"
				style="padding:0.9rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
			>
				<option value="basique" selected={!form?.auth_type || form?.auth_type === 'basique'}>basique</option>
				<option value="oauth" selected={form?.auth_type === 'oauth'}>oauth</option>
				<option value="authelia" selected={form?.auth_type === 'authelia'}>authelia</option>
				<option value="aucune" selected={form?.auth_type === 'aucune'}>aucune</option>
				<option value="oauth2-proxy" selected={form?.auth_type === 'oauth2-proxy'}>oauth2-proxy</option>
			</select>
		</label>

		<button
			type="submit"
			style="margin-top:0.5rem; padding:0.95rem 1.1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #a855f7); color:white;"
		>
			Lancer l’installation de {app.name}
		</button>
	</form>

	{#if form?.error}
		<p style="color:#fca5a5; margin-top:1rem;">{form.error}</p>
	{/if}
</div>