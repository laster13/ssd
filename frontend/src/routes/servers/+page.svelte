<script lang="ts">
	let { data } = $props();

	const servers = $derived(data.servers ?? []);

	function humanStatus(status: string) {
		if (status === 'paired') return 'En ligne';
		if (status === 'pending_pairing') return 'Connexion en attente';
		if (status === 'failed') return 'Erreur';
		return status;
	}
</script>

<svelte:head>
	<title>Serveurs</title>
</svelte:head>

<section
	style="border:1px solid rgba(255,255,255,0.08); border-radius:28px; padding:2rem; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1rem;">
		<div>
			<h1 style="margin:0;">Mes serveurs</h1>
			<p style="color:#cbd5e1; line-height:1.7; margin:0.6rem 0 0 0;">
				Retrouve ici les serveurs connectés à ton espace et leur état général.
			</p>
		</div>

		<a
			href="/servers/add"
			style="display:inline-flex; align-items:center; justify-content:center; padding:0.9rem 1rem; border-radius:16px; text-decoration:none; color:white; font-weight:700; background:linear-gradient(90deg, #38bdf8, #a855f7);"
		>
			Ajouter un serveur
		</a>
	</div>

	{#if servers.length > 0}
		<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">
			{#each servers as server}
				<article
					style="border-radius:24px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.55); padding:1.1rem;"
				>
					<div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:0.8rem;">
						<h2 style="margin:0; font-size:1.1rem;">{server.hostname ?? 'Serveur sans nom'}</h2>
						<span
							style="padding:0.38rem 0.65rem; border-radius:999px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#86efac; font-size:0.82rem;"
						>
							{humanStatus(server.status)}
						</span>
					</div>

					<div style="display:grid; gap:0.45rem; color:#cbd5e1;">
						<div><strong>Agent :</strong> {server.agent_version ?? '-'}</div>
						<div><strong>Dernier contact :</strong> {server.last_seen_at ?? '-'}</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<p style="color:#94a3b8;">Aucun serveur connecté.</p>
	{/if}
</section>