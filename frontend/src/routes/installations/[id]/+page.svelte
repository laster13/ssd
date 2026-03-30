<script lang="ts">
	import { onMount } from 'svelte';

	let { data } = $props();

	let job = $state(data.job);
	let logs = $state(data.logs ?? []);

	const isFinished = () => job.status === 'completed' || job.status === 'failed';

	function humanStatus(status: string) {
		if (status === 'pending') return 'En attente';
		if (status === 'claimed') return 'Préparation';
		if (status === 'running') return 'En cours';
		if (status === 'completed') return 'Terminée';
		if (status === 'failed') return 'Échec';
		return status;
	}

	onMount(() => {
		if (isFinished()) return;

		const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		const backendHost = `${window.location.hostname}:8000`;
                const ws = new WebSocket(`${protocol}//${backendHost}/ws/jobs/${job.id}`);

		ws.onmessage = (event) => {
			const payload = JSON.parse(event.data);

			if (payload.type === 'job_log' && payload.log) {
				logs = [...logs, payload.log];
			}

			if (payload.type === 'job_status') {
				job = {
					...job,
					status: payload.status ?? job.status,
					claimed_at: payload.claimed_at ?? job.claimed_at,
					completed_at: payload.completed_at ?? job.completed_at,
					result: payload.result ?? job.result,
					error_message: payload.error_message ?? job.error_message
				};

				if (isFinished()) {
					ws.close();
				}
			}
		};

		return () => {
			ws.close();
		};
	});
</script>

<svelte:head>
	<title>Suivi d’installation</title>
</svelte:head>

<div
	style="max-width:960px; margin:0 auto; border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28);"
>
	<p style="margin-top:0;">
		<a href="/installations" style="color:#93c5fd; text-decoration:none;">← Retour aux installations</a>
	</p>

	<h1 style="margin-bottom:0.5rem;">Suivi d’installation</h1>

	<div
		style="margin:1rem 0 1.5rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
	>
		<div><strong>Application :</strong> {job.payload?.app_slug ?? '-'}</div>
		<div><strong>Sous-domaine :</strong> {job.payload?.subdomain ?? '-'}</div>
		<div><strong>Authentification :</strong> {job.payload?.auth_type ?? '-'}</div>
		<div><strong>Statut :</strong> {humanStatus(job.status)}</div>
	</div>

	{#if !isFinished()}
		<p style="color:#94a3b8;">Connexion temps réel active…</p>
	{/if}

	{#if job.status === 'completed'}
		<div
			style="margin:1rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#bbf7d0;"
		>
			L’installation est terminée avec succès.
		</div>
	{/if}

	{#if job.status === 'failed'}
		<div
			style="margin:1rem 0; padding:1rem 1.1rem; border-radius:18px; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.22); color:#fecaca;"
		>
			L’installation a échoué.
		</div>
	{/if}

	<h2>Journal d’installation</h2>

	{#if logs.length > 0}
		<div
			style="border-radius:20px; border:1px solid rgba(255,255,255,0.08); background:rgba(2,6,23,0.6); padding:1rem; max-height:500px; overflow:auto; font-family:monospace; font-size:0.92rem;"
		>
			{#each logs as log}
				<div style="padding:0.35rem 0; border-bottom:1px solid rgba(255,255,255,0.04);">
					<span style="color:#64748b;">[{log.level}]</span>
					<span>{log.message}</span>
				</div>
			{/each}
		</div>
	{:else}
		<p style="color:#94a3b8;">Aucun log pour le moment.</p>
	{/if}
</div>