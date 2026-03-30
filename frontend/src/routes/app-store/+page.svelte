<script lang="ts">
	let { data } = $props();

	let query = $state('');
	let activeCategory = $state('Tous');

	const apps = $derived(data.apps ?? []);
	const categories = $derived(['Tous', ...new Set(apps.map((app) => app.category))]);

	const filteredApps = $derived(
		apps.filter((app) => {
			const matchesCategory = activeCategory === 'Tous' || app.category === activeCategory;
			const q = query.trim().toLowerCase();

			const matchesQuery =
				!q ||
				app.name.toLowerCase().includes(q) ||
				app.slug.toLowerCase().includes(q) ||
				app.description.toLowerCase().includes(q) ||
				app.category.toLowerCase().includes(q);

			return matchesCategory && matchesQuery;
		})
	);
</script>

<svelte:head>
	<title>App Store</title>
</svelte:head>

<section
	style="position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.08); border-radius:28px; padding:2rem; background:linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)); box-shadow: 0 20px 80px rgba(0,0,0,0.35); margin-bottom:1.5rem;"
>
	<div
		style="display:grid; grid-template-columns: minmax(0,1.3fr) minmax(280px,0.7fr); gap:2rem; align-items:center;"
	>
		<div>
			<div
				style="display:inline-flex; align-items:center; gap:0.5rem; padding:0.45rem 0.8rem; border-radius:999px; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.25); color:#7dd3fc; font-size:0.9rem; margin-bottom:1rem;"
			>
				<span>●</span>
				<span>Premium App Store</span>
			</div>

			<h1
				style="font-size:clamp(2rem, 4vw, 4rem); line-height:1.02; margin:0 0 0.9rem 0; letter-spacing:-0.04em;"
			>
				Installe tes apps
				<span
					style="background:linear-gradient(90deg, #38bdf8 0%, #a855f7 45%, #22c55e 100%); -webkit-background-clip:text; background-clip:text; color:transparent;"
				>
					en quelques clics
				</span>
			</h1>

			<p style="margin:0; max-width:52rem; color:#cbd5e1; font-size:1.05rem; line-height:1.7;">
				Choisis une application, configure son accès, puis laisse l’agent l’installer sur ton VPS.
				L’App Store sert d’entrée utilisateur. La page Admin reste ta console technique.
			</p>
		</div>

		<div
			style="border-radius:24px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); padding:1.25rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);"
		>
			<div style="display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:0.9rem;">
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Apps initiales</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">{apps.length}</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Objectif catalogue</div>
					<div style="font-size:1.8rem; font-weight:700; margin-top:0.35rem;">180</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Mode</div>
					<div style="font-size:1.15rem; font-weight:700; margin-top:0.35rem;">App Store</div>
				</div>
				<div style="padding:1rem; border-radius:18px; background:rgba(255,255,255,0.04);">
					<div style="color:#64748b; font-size:0.85rem;">Installation</div>
					<div style="font-size:1.15rem; font-weight:700; margin-top:0.35rem;">Pilotée par jobs</div>
				</div>
			</div>
		</div>
	</div>
</section>

<section
	style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1.25rem;"
>
	<div style="display:flex; flex-wrap:wrap; gap:0.75rem;">
		{#each categories as category}
			<button
				type="button"
				onclick={() => (activeCategory = category)}
				style={`padding:0.75rem 1rem; border-radius:999px; border:1px solid ${
					activeCategory === category ? 'rgba(56,189,248,0.35)' : 'rgba(255,255,255,0.08)'
				}; background:${
					activeCategory === category ? 'rgba(56,189,248,0.14)' : 'rgba(255,255,255,0.04)'
				}; color:${activeCategory === category ? '#e0f2fe' : '#cbd5e1'}; cursor:pointer; transition:all .2s ease;`}
			>
				{category}
			</button>
		{/each}
	</div>

	<div style="min-width:min(100%, 360px);">
		<input
			bind:value={query}
			placeholder="Rechercher une application…"
			style="width:100%; padding:0.9rem 1rem; border-radius:18px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white; outline:none;"
		/>
	</div>
</section>

<section
	style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1.1rem;"
>
	{#each filteredApps as app}
		<article
			style="position:relative; overflow:hidden; border-radius:26px; border:1px solid rgba(255,255,255,0.08); background:linear-gradient(180deg, rgba(15,23,42,0.78), rgba(15,23,42,0.5)); padding:1.15rem; box-shadow:0 18px 50px rgba(0,0,0,0.24);"
		>
			<div
				style={`position:absolute; inset:0 auto auto 0; width:100%; height:5px; background:${app.accent}; opacity:0.95;`}
			/>

			<div
				style="display:flex; align-items:flex-start; justify-content:space-between; gap:1rem; margin-bottom:1rem;"
			>
				<div style="display:flex; align-items:center; gap:0.9rem;">
					<div
						style={`width:60px; height:60px; border-radius:18px; background:${app.accent}; padding:1px; box-shadow:0 10px 30px rgba(0,0,0,0.25);`}
					>
						<div
							style="width:100%; height:100%; border-radius:17px; background:rgba(15,23,42,0.88); display:grid; place-items:center;"
						>
							<img
								src={app.icon}
								alt={app.name}
								style="width:34px; height:34px; object-fit:contain;"
								loading="lazy"
							/>
						</div>
					</div>

					<div>
						<h2 style="margin:0; font-size:1.12rem;">{app.name}</h2>
						<div style="margin-top:0.3rem; color:#94a3b8; font-size:0.92rem;">{app.tagline}</div>
					</div>
				</div>

				<div
					style="padding:0.45rem 0.7rem; border-radius:999px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.22); color:#86efac; font-size:0.82rem; white-space:nowrap;"
				>
					{app.status}
				</div>
			</div>

			<div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1rem;">
				<span
					style="padding:0.38rem 0.65rem; border-radius:999px; background:rgba(255,255,255,0.05); color:#cbd5e1; font-size:0.82rem;"
				>
					{app.category}
				</span>
				<span
					style="padding:0.38rem 0.65rem; border-radius:999px; background:rgba(255,255,255,0.05); color:#cbd5e1; font-size:0.82rem;"
				>
					{app.slug}
				</span>
			</div>

			<p style="margin:0 0 1.25rem 0; color:#cbd5e1; line-height:1.65; min-height:5.4rem;">
				{app.description}
			</p>

			<div style="display:flex; align-items:center; justify-content:space-between; gap:0.8rem;">
				<a
					href={`/installations/new?app=${encodeURIComponent(app.slug)}`}
					style={`display:inline-flex; align-items:center; justify-content:center; gap:0.5rem; padding:0.85rem 1rem; border-radius:16px; text-decoration:none; color:white; font-weight:600; background:${app.accent}; min-width:140px;`}
				>
					Installer
				</a>

				<div style="color:#64748b; font-size:0.85rem;">Config puis déploiement</div>
			</div>
		</article>
	{/each}
</section>

{#if filteredApps.length === 0}
	<div
		style="margin-top:1.25rem; padding:1.25rem; border-radius:22px; border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.03); color:#cbd5e1;"
	>
		Aucune application ne correspond à ta recherche.
	</div>
{/if}