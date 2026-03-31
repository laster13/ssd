<script lang="ts">
	let { data } = $props();

	const logs = data.logs ?? [];

	function formatValue(value: unknown) {
		if (value == null) return '-';
		if (typeof value === 'object') return JSON.stringify(value, null, 2);
		return String(value);
	}

	function severityStyle(severity: string) {
		switch (severity) {
			case 'critical':
				return 'background:rgba(239,68,68,0.14); border:1px solid rgba(239,68,68,0.28); color:#fecaca;';
			case 'warning':
				return 'background:rgba(245,158,11,0.14); border:1px solid rgba(245,158,11,0.28); color:#fde68a;';
			default:
				return 'background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#bbf7d0;';
		}
	}

	function successStyle(success: boolean) {
		return success
			? 'background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#86efac;'
			: 'background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.22); color:#fca5a5;';
	}
</script>

<svelte:head>
	<title>Audit sécurité</title>
</svelte:head>

<section style="max-width:1200px; margin:0 auto; padding:2rem 1rem 4rem;">
	<a href="/admin" style="display:inline-block; margin-bottom:1rem; color:#93c5fd; text-decoration:none;">
		← Retour admin
	</a>

	<div
		style="border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28); margin-bottom:1.25rem;"
	>
		<h1 style="margin:0 0 0.75rem 0;">Audit sécurité</h1>
		<p style="margin:0; color:#cbd5e1; line-height:1.7;">
			Retrouve ici les événements sensibles du système : authentification, 2FA, pairing,
			création de jobs, rotation de tokens machine et révocation de machines.
		</p>
	</div>

	{#if logs.length > 0}
		<div style="display:grid; gap:1rem;">
			{#each logs as log}
				<article
					style="border:1px solid rgba(255,255,255,0.08); border-radius:22px; background:rgba(15,23,42,0.68); padding:1.1rem;"
				>
					<div
						style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap; margin-bottom:0.9rem;"
					>
						<div>
							<h2 style="margin:0; font-size:1.05rem;">{log.event_type}</h2>
							<div style="margin-top:0.35rem; color:#94a3b8; font-size:0.9rem;">
								{log.created_at}
							</div>
						</div>

						<div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
							<div
								style={`padding:0.4rem 0.7rem; border-radius:999px; font-size:0.82rem; ${severityStyle(log.severity)}`}
							>
								{log.severity}
							</div>
							<div
								style={`padding:0.4rem 0.7rem; border-radius:999px; font-size:0.82rem; ${successStyle(log.success)}`}
							>
								{log.success ? 'success' : 'failure'}
							</div>
							{#if log.status_code}
								<div
									style="padding:0.4rem 0.7rem; border-radius:999px; font-size:0.82rem; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08); color:#cbd5e1;"
								>
									HTTP {log.status_code}
								</div>
							{/if}
						</div>
					</div>

					{#if log.description}
						<p style="margin:0 0 0.9rem 0; color:#e2e8f0; line-height:1.6;">
							{log.description}
						</p>
					{/if}

					<div
						style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:0.75rem; margin-bottom:0.9rem;"
					>
						<div
							style="padding:0.85rem 0.95rem; border-radius:16px; background:rgba(255,255,255,0.04);"
						>
							<div style="color:#64748b; font-size:0.82rem; margin-bottom:0.35rem;">Actor type</div>
							<div style="color:#e2e8f0;">{formatValue(log.actor_type)}</div>
						</div>

						<div
							style="padding:0.85rem 0.95rem; border-radius:16px; background:rgba(255,255,255,0.04);"
						>
							<div style="color:#64748b; font-size:0.82rem; margin-bottom:0.35rem;">Actor user</div>
							<div style="color:#e2e8f0;">{formatValue(log.actor_user_id)}</div>
						</div>

						<div
							style="padding:0.85rem 0.95rem; border-radius:16px; background:rgba(255,255,255,0.04);"
						>
							<div style="color:#64748b; font-size:0.82rem; margin-bottom:0.35rem;">Target machine</div>
							<div style="color:#e2e8f0;">{formatValue(log.target_machine_id)}</div>
						</div>

						<div
							style="padding:0.85rem 0.95rem; border-radius:16px; background:rgba(255,255,255,0.04);"
						>
							<div style="color:#64748b; font-size:0.82rem; margin-bottom:0.35rem;">IP</div>
							<div style="color:#e2e8f0;">{formatValue(log.ip_address)}</div>
						</div>
					</div>

					{#if log.details}
						<div
							style="padding:0.95rem 1rem; border-radius:16px; background:rgba(2,6,23,0.65); border:1px solid rgba(255,255,255,0.08);"
						>
							<div style="color:#94a3b8; margin-bottom:0.45rem;">Details</div>
							<pre
								style="margin:0; white-space:pre-wrap; word-break:break-word; color:#cbd5e1; font-size:0.9rem;"
							>{JSON.stringify(log.details, null, 2)}</pre>
						</div>
					{/if}
				</article>
			{/each}
		</div>
	{:else}
		<div
			style="padding:1.25rem; border-radius:22px; border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.03); color:#cbd5e1;"
		>
			Aucun événement d’audit pour le moment.
		</div>
	{/if}
</section>
