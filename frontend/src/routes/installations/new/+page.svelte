<script lang="ts">
	let { data, form } = $props();

	const app = data.app;
	const machines = data.machines ?? [];
	const authOptions = ['aucune', 'basique', 'oauth', 'authelia', 'oauth2-proxy'];
</script>

<svelte:head>
	<title>Nouvelle installation</title>
</svelte:head>

<section class="page">
	<div class="header">
		<a class="back" href="/app-store">← Retour à l’App Store</a>
		<h1>Installer {app.name}</h1>
		<p>{app.tagline}</p>
	</div>

	{#if form?.error}
		<div class="alert error">{form.error}</div>
	{/if}

	{#if machines.length === 0}
		<div class="alert warning">
			Aucun serveur pairé trouvé. Va d’abord dans <a href="/servers">Mes serveurs</a>.
		</div>
	{/if}

	<div class="card">
		<form
			method="POST"
			action={`?/createInstallation&app=${encodeURIComponent(app.slug)}`}
			class="form"
		>
			<input type="hidden" name="_csrf" value={data.csrfToken} />
			<input type="hidden" name="app_slug" value={app.slug} />

			<div class="field">
				<label for="app">Application</label>
				<input id="app" value={app.name} disabled />
			</div>

			<div class="field">
				<label for="machine_id">Serveur</label>
				<select id="machine_id" name="machine_id" required disabled={machines.length === 0}>
					<option value="">Sélectionne un serveur</option>
					{#each machines as machine}
						<option value={machine.id} selected={form?.machine_id === machine.id}>
							{machine.hostname || machine.machine_uuid} — {machine.status}
						</option>
					{/each}
				</select>
			</div>

			<div class="field">
				<label for="subdomain">Sous-domaine</label>
				<input
					id="subdomain"
					name="subdomain"
					required
					placeholder={app.slug}
					value={form?.subdomain ?? app.slug}
				/>
			</div>

			<div class="field">
				<label for="auth_type">Auth</label>
				<select id="auth_type" name="auth_type" required>
					{#each authOptions as option}
						<option value={option} selected={(form?.auth_type ?? 'aucune') === option}>
							{option}
						</option>
					{/each}
				</select>
			</div>

			<div class="actions">
				<a class="secondary" href="/app-store">Annuler</a>
				<button type="submit" disabled={machines.length === 0}>Lancer l’installation</button>
			</div>
		</form>
	</div>
</section>

<style>
	.page {
		max-width: 760px;
		margin: 0 auto;
		padding: 2rem 1rem 4rem;
		color: #e5eef8;
	}

	.header {
		margin-bottom: 1.5rem;
	}

	.back {
		display: inline-block;
		margin-bottom: 1rem;
		color: #93c5fd;
		text-decoration: none;
	}

	h1 {
		margin: 0;
		font-size: 2rem;
	}

	.header p {
		margin-top: 0.5rem;
		color: #94a3b8;
	}

	.card,
	.alert {
		border: 1px solid rgba(148, 163, 184, 0.15);
		background: rgba(15, 23, 42, 0.7);
		backdrop-filter: blur(12px);
		border-radius: 1rem;
	}

	.card {
		padding: 1.25rem;
	}

	.alert {
		padding: 0.9rem 1rem;
		margin-bottom: 1rem;
	}

	.alert.error {
		color: #fecaca;
		border-color: rgba(239, 68, 68, 0.35);
	}

	.alert.warning {
		color: #fde68a;
		border-color: rgba(245, 158, 11, 0.35);
	}

	.alert a {
		color: #93c5fd;
	}

	.form {
		display: grid;
		gap: 1rem;
	}

	.field {
		display: grid;
		gap: 0.4rem;
	}

	label {
		font-size: 0.95rem;
		color: #cbd5e1;
	}

	input,
	select,
	button,
	.secondary {
		border-radius: 0.8rem;
		border: 1px solid rgba(148, 163, 184, 0.18);
		padding: 0.85rem 0.95rem;
		font: inherit;
	}

	input,
	select {
		background: rgba(15, 23, 42, 0.85);
		color: white;
	}

	.actions {
		display: flex;
		gap: 0.75rem;
		justify-content: flex-end;
		margin-top: 0.5rem;
	}

	button {
		background: linear-gradient(135deg, rgba(14, 165, 233, 0.95), rgba(59, 130, 246, 0.95));
		color: white;
		font-weight: 700;
		cursor: pointer;
	}

	.secondary {
		display: inline-flex;
		align-items: center;
		text-decoration: none;
		color: #cbd5e1;
		background: rgba(255, 255, 255, 0.04);
	}

	button[disabled] {
		opacity: 0.6;
		cursor: not-allowed;
	}
</style>