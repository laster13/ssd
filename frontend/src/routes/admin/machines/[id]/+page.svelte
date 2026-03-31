<script lang="ts">
	let { data, form } = $props();

	const machine = data.machine;
	const jobs = data.jobs ?? [];
	const authOptions = ['basique', 'oauth', 'authelia', 'aucune', 'oauth2-proxy'];

	const effectiveStatus = form?.revoked ? 'revoked' : machine.status;
</script>

<svelte:head>
	<title>Détail machine</title>
</svelte:head>

<section style="max-width:1100px; margin:0 auto; padding:2rem 1rem 4rem;">
	<a href="/admin" style="display:inline-block; margin-bottom:1rem; color:#93c5fd; text-decoration:none;">
		← Retour admin
	</a>

	{#if form?.error}
		<div
			style="margin-bottom:1rem; padding:1rem 1.1rem; border-radius:18px; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.28); color:#fecaca;"
		>
			{form.error}
		</div>
	{/if}

	{#if form?.rotated}
		<div
			style="margin-bottom:1rem; padding:1rem 1.1rem; border-radius:18px; background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.28); color:#bbf7d0;"
		>
			<div style="font-weight:700; margin-bottom:0.5rem;">Nouveau token machine généré</div>
			<div style="margin-bottom:0.5rem;">
				Copie-le maintenant. Il ne sera plus réaffiché ensuite.
			</div>
			<div
				style="padding:0.85rem 1rem; border-radius:14px; background:rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.08); font-family:monospace; word-break:break-all;"
			>
				{form.rotatedToken}
			</div>
		</div>
	{/if}

	{#if form?.revoked}
		<div
			style="margin-bottom:1rem; padding:1rem 1.1rem; border-radius:18px; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.28); color:#fde68a;"
		>
			La machine a été révoquée. Elle ne pourra plus communiquer avec le backend tant qu’elle
			n’est pas re-pairée.
		</div>
	{/if}

	<div
		style="display:grid; grid-template-columns:minmax(320px, 380px) minmax(0, 1fr); gap:1rem; align-items:start;"
	>
		<div style="display:grid; gap:1rem;">
			<div
				style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
			>
				<h2 style="margin-top:0;">Actions sécurité machine</h2>

				<div style="display:grid; gap:0.9rem;">
					<form method="POST" action="?/rotateToken">
						<input type="hidden" name="_csrf" value={data.csrfToken} />
						<button
							type="submit"
							disabled={effectiveStatus === 'revoked'}
							style="width:100%; padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #2563eb); color:white; opacity:{effectiveStatus === 'revoked' ? '0.6' : '1'};"
						>
							Rotate machine token
						</button>
					</form>

					<form method="POST" action="?/revokeMachine">
						<input type="hidden" name="_csrf" value={data.csrfToken} />
						<button
							type="submit"
							disabled={effectiveStatus === 'revoked'}
							style="width:100%; padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #ef4444, #dc2626); color:white; opacity:{effectiveStatus === 'revoked' ? '0.6' : '1'};"
						>
							Revoke machine
						</button>
					</form>

					<p style="margin:0; color:#94a3b8; line-height:1.6; font-size:0.92rem;">
						<strong>Rotate</strong> génère un nouveau token machine. <strong>Revoke</strong>
						coupe immédiatement la relation entre cette machine et le backend.
					</p>
				</div>
			</div>

			<div
				style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
			>
				<h2 style="margin-top:0;">Installer une app</h2>

				<form method="POST" action="?/createJob" style="display:grid; gap:0.9rem;">
					<input type="hidden" name="_csrf" value={data.csrfToken} />

					<label style="display:grid; gap:0.4rem;">
						<span>App slug</span>
						<input
							name="app_slug"
							value={form?.app_slug ?? ''}
							placeholder="n8n"
							disabled={effectiveStatus === 'revoked'}
							style="padding:0.85rem 0.95rem; border-radius:14px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
						/>
					</label>

					<label style="display:grid; gap:0.4rem;">
						<span>Sous-domaine</span>
						<input
							name="subdomain"
							value={form?.subdomain ?? ''}
							placeholder="demo"
							disabled={effectiveStatus === 'revoked'}
							style="padding:0.85rem 0.95rem; border-radius:14px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
						/>
					</label>

					<label style="display:grid; gap:0.4rem;">
						<span>Type d'auth</span>
						<select
							name="auth_type"
							disabled={effectiveStatus === 'revoked'}
							style="padding:0.85rem 0.95rem; border-radius:14px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
						>
							{#each authOptions as option}
								<option value={option} selected={(form?.auth_type ?? 'aucune') === option}>
									{option}
								</option>
							{/each}
						</select>
					</label>

					<button
						type="submit"
						disabled={effectiveStatus === 'revoked'}
						style="padding:0.9rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #2563eb); color:white; opacity:{effectiveStatus === 'revoked' ? '0.6' : '1'};"
					>
						Créer le job
					</button>
				</form>
			</div>
		</div>

		<div style="display:grid; gap:1rem;">
			<div
				style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
			>
				<h2 style="margin-top:0;">Informations</h2>

				<ul style="margin:0; padding-left:1.2rem; color:#cbd5e1; line-height:1.8;">
					<li><strong>ID :</strong> {machine.id}</li>
					<li><strong>UUID :</strong> {machine.machine_uuid}</li>
					<li><strong>Status :</strong> {effectiveStatus}</li>
					<li><strong>Hostname :</strong> {machine.hostname ?? '-'}</li>
					<li><strong>Agent version :</strong> {machine.agent_version ?? '-'}</li>
					<li><strong>Auth token créé le :</strong> {machine.auth_token_created_at ?? '-'}</li>
					<li><strong>Last seen :</strong> {machine.last_seen_at ?? '-'}</li>
					<li><strong>Created at :</strong> {machine.created_at}</li>
					<li><strong>Updated at :</strong> {machine.updated_at}</li>
				</ul>
			</div>

			<div
				style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
			>
				<h2 style="margin-top:0;">Jobs de cette machine</h2>

				{#if jobs.length > 0}
					<div style="overflow:auto;">
						<table style="width:100%; border-collapse:collapse;">
							<thead>
								<tr style="text-align:left; color:#94a3b8;">
									<th style="padding:0.8rem 0.5rem;">ID</th>
									<th style="padding:0.8rem 0.5rem;">Type</th>
									<th style="padding:0.8rem 0.5rem;">Status</th>
									<th style="padding:0.8rem 0.5rem;">Créé le</th>
									<th style="padding:0.8rem 0.5rem;">Action</th>
								</tr>
							</thead>
							<tbody>
								{#each jobs as job}
									<tr style="border-top:1px solid rgba(255,255,255,0.08);">
										<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{job.id}</td>
										<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{job.type}</td>
										<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{job.status}</td>
										<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{job.created_at}</td>
										<td style="padding:0.8rem 0.5rem;">
											<a
												href={`/admin/jobs/${job.id}`}
												style="color:#7dd3fc; text-decoration:none;"
											>
												Voir
											</a>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{:else}
					<p style="color:#94a3b8; margin:0;">Aucun job pour cette machine.</p>
				{/if}
			</div>
		</div>
	</div>
</section>