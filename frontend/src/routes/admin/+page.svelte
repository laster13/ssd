<script lang="ts">
	let { data } = $props();

	const machines = data.machines ?? [];
	const jobs = data.jobs ?? [];
</script>

<h1>Admin</h1>

<p>Bonjour {data.user.email}</p>

<h2>Machines</h2>

{#if machines.length > 0}
	<table style="border-collapse: collapse; width: 100%; margin-bottom: 2rem;">
		<thead>
			<tr>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">ID</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">UUID</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Status</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Hostname</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Agent</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Last seen</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Action</th>
			</tr>
		</thead>
		<tbody>
			{#each machines as machine}
				<tr>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.id}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.machine_uuid}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.status}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.hostname ?? '-'}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.agent_version ?? '-'}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{machine.last_seen_at ?? '-'}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">
						<a href={`/admin/machines/${machine.id}`}>Voir</a>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
{:else}
	<p>Aucune machine.</p>
{/if}

<h2>Jobs</h2>

{#if jobs.length > 0}
	<table style="border-collapse: collapse; width: 100%;">
		<thead>
			<tr>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">ID</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Type</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Status</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Machine</th>
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
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.machine_id}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{job.created_at}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">
						<a href={`/admin/jobs/${job.id}`}>Voir</a>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
{:else}
	<p>Aucun job.</p>
{/if}