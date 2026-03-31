<script lang="ts">
	let { data } = $props();

	const jobs = data.jobs ?? [];
	const machines = data.machines ?? [];
</script>

<svelte:head>
	<title>Admin</title>
</svelte:head>

<section style="max-width:1200px; margin:0 auto; padding:2rem 1rem 4rem;">
	<div
		style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap; margin-bottom:1.25rem;"
	>
		<div>
			<h1 style="margin:0;">Admin</h1>
			<p style="margin:0.5rem 0 0 0; color:#94a3b8;">
				Console interne pour superviser les machines, les jobs et les événements sensibles.
			</p>
		</div>

		<div style="display:flex; gap:0.75rem; flex-wrap:wrap;">
			<a
				href="/admin/security-audit"
				style="display:inline-flex; align-items:center; justify-content:center; padding:0.8rem 1rem; border-radius:16px; text-decoration:none; color:white; font-weight:700; background:linear-gradient(90deg, #f59e0b, #ea580c);"
			>
				Audit sécurité
			</a>
		</div>
	</div>

	<div style="display:grid; grid-template-columns:1fr; gap:1rem;">
		<div
			style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
		>
			<h2 style="margin-top:0;">Machines</h2>

			{#if machines.length > 0}
				<div style="overflow:auto;">
					<table style="width:100%; border-collapse:collapse;">
						<thead>
							<tr style="text-align:left; color:#94a3b8;">
								<th style="padding:0.8rem 0.5rem;">ID</th>
								<th style="padding:0.8rem 0.5rem;">UUID</th>
								<th style="padding:0.8rem 0.5rem;">Status</th>
								<th style="padding:0.8rem 0.5rem;">Hostname</th>
								<th style="padding:0.8rem 0.5rem;">Agent</th>
								<th style="padding:0.8rem 0.5rem;">Last seen</th>
								<th style="padding:0.8rem 0.5rem;">Action</th>
							</tr>
						</thead>
						<tbody>
							{#each machines as machine}
								<tr style="border-top:1px solid rgba(255,255,255,0.08);">
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.id}</td>
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.machine_uuid}</td>
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.status}</td>
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.hostname ?? '-'}</td>
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.agent_version ?? '-'}</td>
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{machine.last_seen_at ?? '-'}</td>
									<td style="padding:0.8rem 0.5rem;">
										<a
											href={`/admin/machines/${machine.id}`}
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
				<p style="color:#94a3b8; margin:0;">Aucune machine.</p>
			{/if}
		</div>

		<div
			style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
		>
			<h2 style="margin-top:0;">Jobs récents</h2>

			{#if jobs.length > 0}
				<div style="overflow:auto;">
					<table style="width:100%; border-collapse:collapse;">
						<thead>
							<tr style="text-align:left; color:#94a3b8;">
								<th style="padding:0.8rem 0.5rem;">ID</th>
								<th style="padding:0.8rem 0.5rem;">Machine</th>
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
									<td style="padding:0.8rem 0.5rem; color:#cbd5e1;">{job.machine_id}</td>
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
				<p style="color:#94a3b8; margin:0;">Aucun job.</p>
			{/if}
		</div>
	</div>
</section>