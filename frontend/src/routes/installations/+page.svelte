<script lang="ts">
	let { data } = $props();

	const jobs = data.jobs ?? [];

	function humanStatus(status: string) {
		if (status === 'pending') return 'En attente';
		if (status === 'claimed') return 'Préparation';
		if (status === 'running') return 'En cours';
		if (status === 'completed') return 'Terminée';
		if (status === 'failed') return 'Échec';
		return status;
	}
</script>

<svelte:head>
	<title>Installations</title>
</svelte:head>

<section
	style="border:1px solid rgba(255,255,255,0.08); border-radius:28px; padding:2rem; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<h1 style="margin-top:0;">Installations</h1>
	<p style="color:#cbd5e1; line-height:1.7; margin-bottom:1.5rem;">
		Suis l’avancement des installations lancées depuis l’App Store.
	</p>

	{#if jobs.length > 0}
		<div style="display:grid; gap:0.9rem;">
			{#each jobs as job}
				<a
					href={`/installations/${job.id}`}
					style="display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:1rem 1.1rem; border-radius:20px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.55); text-decoration:none; color:white;"
				>
					<div>
						<div style="font-weight:700;">Installation</div>
						<div style="color:#94a3b8; margin-top:0.25rem;">Créée le {job.created_at}</div>
					</div>

					<div
						style="padding:0.42rem 0.7rem; border-radius:999px; background:rgba(255,255,255,0.05); color:#cbd5e1; font-size:0.86rem;"
					>
						{humanStatus(job.status)}
					</div>
				</a>
			{/each}
		</div>
	{:else}
		<p style="color:#94a3b8;">Aucune installation pour le moment.</p>
	{/if}
</section>
