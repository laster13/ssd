<script lang="ts">
	let { data } = $props();

	const servers = data.machines ?? [];

	function badgeFor(server: any) {
		if (server.status === 'revoked') {
			return {
				label: 'Révoquée',
				style:
					'background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.22); color:#fca5a5;'
			};
		}

		if (server.status === 'paired') {
			return {
				label: 'En ligne',
				style:
					'background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#86efac;'
			};
		}

		return {
			label: server.status ?? 'Inconnu',
			style:
				'background:rgba(148,163,184,0.12); border:1px solid rgba(148,163,184,0.22); color:#cbd5e1;'
		};
	}
</script>

<svelte:head>
	<title>Mes serveurs</title>
</svelte:head>

<section style="max-width:1100px; margin:0 auto; padding:2rem 1rem 4rem;">
	<div
		style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap; margin-bottom:1.25rem;"
	>
		<div>
			<h1 style="margin:0;">Mes serveurs</h1>
			<p style="margin:0.5rem 0 0 0; color:#94a3b8; line-height:1.6;">
				Retrouve ici les serveurs pairés à ton compte et ajoute-en un nouveau si besoin.
			</p>
		</div>

		<a
			href="/servers/add"
			style="display:inline-flex; align-items:center; justify-content:center; padding:0.85rem 1rem; border-radius:16px; text-decoration:none; color:white; font-weight:700; background:linear-gradient(90deg, #38bdf8, #2563eb);"
		>
			Ajouter un serveur
		</a>
	</div>

	{#if servers.length > 0}
		<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">
			{#each servers as server}
				{@const badge = badgeFor(server)}
				<article
					style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.65); padding:1.25rem;"
				>
					<div
						style="display:flex; justify-content:space-between; align-items:flex-start; gap:0.75rem; margin-bottom:1rem;"
					>
						<div>
							<h2 style="margin:0; font-size:1.1rem;">{server.hostname ?? 'Serveur sans nom'}</h2>
							<div style="margin-top:0.3rem; color:#94a3b8; font-size:0.92rem;">
								{server.machine_uuid}
							</div>
						</div>

						<div
							style={`padding:0.45rem 0.7rem; border-radius:999px; font-size:0.82rem; white-space:nowrap; ${badge.style}`}
						>
							{badge.label}
						</div>
					</div>

					<div style="display:grid; gap:0.55rem; color:#cbd5e1;">
						<div><strong>ID :</strong> {server.id}</div>
						<div><strong>Agent :</strong> {server.agent_version ?? '-'}</div>
						<div><strong>Dernier contact :</strong> {server.last_seen_at ?? '-'}</div>
						<div><strong>Status brut :</strong> {server.status}</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div
			style="padding:1.1rem 1.2rem; border-radius:18px; border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.03); color:#cbd5e1;"
		>
			Aucun serveur pairé pour le moment.
		</div>
	{/if}
</section>