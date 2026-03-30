<script lang="ts">
	let { data } = $props();

	const jobs = $derived(data.jobs ?? []);
	const machines = $derived(data.machines ?? []);

	const machineById = $derived(
		new Map(machines.map((machine) => [machine.id, machine]))
	);

	const appItems = $derived.by(() => {
		const seen = new Set<string>();
		const items = [];

		for (const job of jobs) {
			const payload = job.payload ?? {};
			const appSlug = payload.app_slug ?? 'unknown';
			const subdomain = payload.subdomain ?? '—';
			const authType = payload.auth_type ?? '—';

			const key = `${job.machine_id}:${appSlug}`;

			if (seen.has(key)) continue;
			seen.add(key);

			const machine = machineById.get(job.machine_id);

			items.push({
				key,
				jobId: job.id,
				appSlug,
				subdomain,
				authType,
				status: job.status,
				createdAt: job.created_at,
				updatedAt: job.updated_at,
				machineName: machine?.hostname || machine?.machine_uuid || 'Serveur inconnu',
				machineStatus: machine?.status || 'unknown'
			});
		}

		return items;
	});

	const stats = $derived.by(() => {
		const values = appItems;

		return {
			total: values.length,
			running: values.filter((item) => ['pending', 'claimed', 'running'].includes(item.status)).length,
			failed: values.filter((item) => item.status === 'failed').length,
			completed: values.filter((item) => item.status === 'completed').length
		};
	});

	function humanStatus(status: string) {
		switch (status) {
			case 'pending':
				return 'En attente';
			case 'claimed':
				return 'Prise en charge';
			case 'running':
				return 'En cours';
			case 'completed':
				return 'Terminée';
			case 'failed':
				return 'Échec';
			default:
				return status;
		}
	}

	function statusStyle(status: string) {
		switch (status) {
			case 'completed':
				return 'background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#86efac;';
			case 'failed':
				return 'background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.22); color:#fca5a5;';
			case 'running':
				return 'background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.22); color:#7dd3fc;';
			case 'claimed':
				return 'background:rgba(96,165,250,0.12); border:1px solid rgba(96,165,250,0.22); color:#93c5fd;';
			default:
				return 'background:rgba(245,158,11,0.12); border:1px solid rgba(245,158,11,0.22); color:#fcd34d;';
		}
	}
</script>

<svelte:head>
	<title>Mes applications</title>
</svelte:head>

<section
	style="position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.08); border-radius:28px; padding:2rem; background:linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)); box-shadow: 0 20px 80px rgba(0,0,0,0.35); margin-bottom:1.5rem;"
>
	<div
		style="display:grid; grid-template-columns:minmax(0,1.3fr) minmax(280px,0.7fr); gap:2rem; align-items:center;"
	>
		<div>
			<div
				style="display:inline-flex; align-items:center; gap:0.5rem; padding:0.45rem 0.8rem; border-radius:999px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.25); color:#86efac; font-size:0.9rem; margin-bottom:1rem;"
			>
				<span>●</span>
				<span>Mes applications</span>
			</div>

			<h1
				style="font-size:clamp(2rem, 4vw, 4rem); line-height:1.02; margin:0 0 0.9rem 0; letter-spacing:-0.04em;"
			>
				Suis tes apps
				<span
					style="background:linear-gradient(90deg, #22c55e 0%, #38bdf8 45%, #a855f7 100%); -webkit-background-clip:text; background-clip:text; color:transparent;"
				>
					par serveur
				</span>
			</h1>

			<p style="margin:0; max-width:52rem; color:#cbd5e1; font-size:1.05rem; line-height:1.7;">
				Vue simplifiée des applications lancées depuis l’App Store, regroupées par serveur, avec
				accès rapide au détail et aux logs.
			</p>
		</div>

		<div
			style="border-radius:24px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); padding:1.25rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);"
		>
			<div style="display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:0.9rem;">
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Applications</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">{stats.total}</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">En cours</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">{stats.running}</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Terminées</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">{stats.completed}</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Échecs</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">{stats.failed}</div>
				</div>
			</div>
		</div>
	</div>
</section>

{#if appItems.length > 0}
	<section
		style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1.1:1.1:1.1rem;"
	>
		{#each appItems as item}
			<article
				style="position:relative; overflow:hidden; border-radius:26px; border:1px solid rgba(255,255,255,0.08); background:linear-gradient(180deg, rgba(15,23,42,0.78), rgba(15,23,42,0.5)); padding:1.15rem; box-shadow:0 18px 50px rgba(0,0,0,0.24);"
			>
				<div
					style="display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin-bottom:1rem;"
				>
					<div>
						<h2 style="margin:0; font-size:1.12rem;">{item.appSlug}</h2>
						<div style="margin-top:0.3rem; color:#94a3b8; font-size:0.92rem;">
							Serveur : {item.machineName}
						</div>
					</div>

					<div
						style={`padding:0.45rem 0.7rem; border-radius:999px; font-size:0.82rem; white-space:nowrap; ${statusStyle(item.status)}`}
					>
						{humanStatus(item.status)}
					</div>
				</div>

				<div style="display:grid; gap:0.7rem; margin-bottom:1.1rem;">
					<div style="display:flex; justify-content:space-between; gap:1rem;">
						<span style="color:#64748b;">Sous-domaine</span>
						<strong style="color:#e2e8f0;">{item.subdomain}</strong>
					</div>

					<div style="display:flex; justify-content:space-between; gap:1rem;">
						<span style="color:#64748b;">Auth</span>
						<strong style="color:#e2e8f0;">{item.authType}</strong>
					</div>

					<div style="display:flex; justify-content:space-between; gap:1rem;">
						<span style="color:#64748b;">Machine</span>
						<strong style="color:#e2e8f0;">{item.machineStatus}</strong>
					</div>

					<div style="display:flex; justify-content:space-between; gap:1rem;">
						<span style="color:#64748b;">Dernière mise à jour</span>
						<strong style="color:#e2e8f0;">{item.updatedAt}</strong>
					</div>
				</div>

				<div style="display:flex; align-items:center; justify-content:space-between; gap:0.8rem;">
					<a
						href={`/installations/${item.jobId}`}
						style="display:inline-flex; align-items:center; justify-content:center; gap:0.5rem; padding:0.85rem 1rem; border-radius:16px; text-decoration:none; color:white; font-weight:600; background:linear-gradient(135deg, rgba(14,165,233,0.95), rgba(59,130,246,0.95)); min-width:140px;"
					>
						Voir les logs
					</a>

					<a
						href={`/installations/new?app=${encodeURIComponent(item.appSlug)}`}
						style="color:#94a3b8; text-decoration:none; font-size:0.9rem;"
					>
						Réinstaller
					</a>
				</div>
			</article>
		{/each}
	</section>
{:else}
	<div
		style="margin-top:1.25rem; padding:1.25rem; border-radius:22px; border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.03); color:#cbd5e1;"
	>
		Aucune application lancée pour le moment. Va dans <a href="/app-store" style="color:#7dd3fc;">App Store</a>.
	</div>
{/if}
