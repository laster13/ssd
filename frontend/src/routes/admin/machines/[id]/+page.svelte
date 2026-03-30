<script lang="ts">
	let { data, form } = $props();

	const machine = data.machine;
	const jobs = data.jobs ?? [];
</script>

<h1>Détail machine</h1>

<p><a href="/admin">← Retour admin</a></p>

<h2>Installer une app</h2>

<form method="POST" action="?/createJob" style="display:flex; flex-direction:column; gap:1rem; max-width:28rem; margin: 1rem 0 2rem 0;">
	<label>
		App slug
		<input name="app_slug" value={form?.app_slug ?? ''} placeholder="autoindex" />
	</label>

	<label>
		Sous-domaine
		<input name="subdomain" value={form?.subdomain ?? ''} placeholder="autoindex" />
	</label>

	<label>
		Type d'auth
		<select name="auth_type">
			<option value="basique" selected={form?.auth_type === 'basique'}>basique</option>
			<option value="oauth" selected={form?.auth_type === 'oauth'}>oauth</option>
			<option value="authelia" selected={form?.auth_type === 'authelia'}>authelia</option>
			<option value="aucune" selected={form?.auth_type === 'aucune'}>aucune</option>
			<option value="oauth2-proxy" selected={form?.auth_type === 'oauth2-proxy'}>oauth2-proxy</option>
		</select>
	</label>

	<button type="submit">Créer le job</button>
</form>

{#if form?.error}
	<p style="color:red;">{form.error}</p>
{/if}

<h2>Informations</h2>

<ul>
	<li><strong>ID :</strong> {machine.id}</li>
	<li><strong>UUID :</strong> {machine.machine_uuid}</li>
	<li><strong>Status :</strong> {machine.status}</li>
	<li><strong>Hostname :</strong> {machine.hostname ?? '-'}</li>
	<li><strong>Agent version :</strong> {machine.agent_version ?? '-'}</li>
	<li><strong>Auth token créé le :</strong> {machine.auth_token_created_at ?? '-'}</li>
	<li><strong>Last seen :</strong> {machine.last_seen_at ?? '-'}</li>
	<li><strong>Created at :</strong> {machine.created_at}</li>
	<li><strong>Updated at :</strong> {machine.updated_at}</li>
</ul>

<h2>Jobs de cette machine</h2>

{#if jobs.length > 0}
	<table style="border-collapse: collapse; width: 100%;">
		<thead>
			<tr>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">ID</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Type</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Status</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Créé le</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Action</th>
			</tr>
		</thead>
		<tbody>
			{#each jobs as job}
				<tr>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.id}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.type}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.status}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.created_at}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">
						<a href={`/admin/jobs/${job.id}`}>Voir</a>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
{:else}
	<p>Aucun job pour cette machine.</p>
{/if}