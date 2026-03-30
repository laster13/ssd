<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let { data } = $props();

	const job = data.job;
	const logs = data.logs ?? [];

	const isFinished = job.status === 'completed' || job.status === 'failed';

	onMount(() => {
		if (!browser || isFinished) return;

		const interval = setInterval(async () => {
			await goto(window.location.pathname, {
				invalidateAll: true,
				noScroll: true,
				replaceState: true,
				keepFocus: true
			});
		}, 5000);

		return () => clearInterval(interval);
	});
</script>

<h1>Détail job</h1>

<p><a href="/admin">← Retour admin</a></p>

{#if !isFinished}
	<p style="color: #666;">Rafraîchissement automatique toutes les 5 secondes…</p>
{/if}

<h2>Informations</h2>

<ul>
	<li><strong>ID :</strong> {job.id}</li>
	<li><strong>Machine ID :</strong> {job.machine_id}</li>
	<li><strong>Type :</strong> {job.type}</li>
	<li><strong>Status :</strong> {job.status}</li>
	<li><strong>Claimed at :</strong> {job.claimed_at ?? '-'}</li>
	<li><strong>Completed at :</strong> {job.completed_at ?? '-'}</li>
	<li><strong>Created at :</strong> {job.created_at}</li>
	<li><strong>Updated at :</strong> {job.updated_at}</li>
</ul>

<h2>Payload</h2>
<pre>{JSON.stringify(job.payload, null, 2)}</pre>

<h2>Résultat</h2>
<pre>{JSON.stringify(job.result, null, 2)}</pre>

<h2>Erreur</h2>
<pre>{job.error_message ?? '-'}</pre>

<h2>Logs</h2>

{#if logs.length > 0}
	<table style="border-collapse: collapse; width: 100%;">
		<thead>
			<tr>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Seq</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Level</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Message</th>
				<th style="text-align:left; border-bottom:1px solid #ddd; padding:0.5rem;">Created at</th>
			</tr>
		</thead>
		<tbody>
			{#each logs as log}
				<tr>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{log.seq}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{log.level}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{log.message}</td>
					<td style="border-bottom:1px solid #eee; padding:0.5rem;">{log.created_at}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{:else}
	<p>Aucun log pour ce job.</p>
{/if}