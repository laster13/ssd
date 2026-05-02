<script lang="ts">
	let {
		app,
		installEnabled = false,
		isLast = false
	}: {
		app: {
			name?: string;
			title?: string;
			slug?: string;
			description?: string;
			tagline?: string;
			category?: string;
			docs_url?: string | null;
			docs_status?: string | null;
		};
		installEnabled?: boolean;
		isLast?: boolean;
	} = $props();

	const title = $derived(app.name ?? app.title ?? 'Application');
	const subtitle = $derived(app.description ?? app.tagline ?? '');
	const slug = $derived(app.slug ?? '');
	const category = $derived(app.category ?? 'Autre');

	const installHref = $derived(`/installations/new?app=${encodeURIComponent(app.slug ?? '')}`);
	const docsUrl = $derived(app.docs_url ?? '');
	const hasDocs = $derived(Boolean(app.docs_url));

	const docsLabel = $derived(
		app.docs_status === 'linked'
			? 'Doc liée'
			: app.docs_status === 'missing'
				? 'Doc manquante'
				: app.docs_url
					? 'Disponible'
					: 'Sans doc'
	);

	const titleClass = $derived(
		category === 'media'
			? 'text-cyan-700 dark:text-cyan-300'
			: category === 'telechargement'
				? 'text-violet-700 dark:text-violet-300'
				: category === 'securite'
					? 'text-amber-700 dark:text-amber-300'
					: category === 'monitoring'
						? 'text-emerald-700 dark:text-emerald-300'
						: 'text-blue-700 dark:text-blue-300'
	);

	const categoryClass = $derived(
		category === 'media'
			? 'border-cyan-200/70 bg-cyan-50 text-cyan-800 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-200'
			: category === 'telechargement'
				? 'border-violet-200/70 bg-violet-50 text-violet-800 dark:border-violet-400/20 dark:bg-violet-400/10 dark:text-violet-200'
				: category === 'securite'
					? 'border-amber-200/70 bg-amber-50 text-amber-800 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-200'
					: category === 'monitoring'
						? 'border-emerald-200/70 bg-emerald-50 text-emerald-800 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-200'
						: 'border-blue-200/70 bg-blue-50 text-blue-800 dark:border-blue-400/20 dark:bg-blue-400/10 dark:text-blue-200'
	);

	const docsClass = $derived(
		app.docs_url
			? 'border-emerald-200/70 bg-emerald-50 text-emerald-800 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-200'
			: 'border-zinc-300/50 bg-zinc-100/70 text-zinc-700 dark:border-zinc-500/30 dark:bg-white/[0.04] dark:text-zinc-300'
	);
</script>

<div class="relative">
	<div class="px-3 py-3">
		<div class="flex items-start justify-between gap-3">
			<div class="min-w-0 flex-1">
				<h3 class={`truncate text-[15px] font-semibold tracking-[-0.02em] ${titleClass}`}>
					{title}
				</h3>
				<p class="mt-0.5 truncate text-[11px] font-mono text-zinc-500 dark:text-zinc-500">{slug}</p>
			</div>

			<span
				class={`shrink-0 rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.12em] ${categoryClass}`}
			>
				{category}
			</span>
		</div>

		{#if subtitle}
			<p class="mt-2 line-clamp-2 text-[14px] leading-5 text-zinc-700 dark:text-zinc-300">
				{subtitle}
			</p>
		{/if}

		<div class="mt-2 flex flex-wrap items-center gap-1.5">
			<span
				class={`inline-flex items-center rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.12em] ${docsClass}`}
			>
				{docsLabel}
			</span>

			{#if !installEnabled}
				<span
					class="inline-flex items-center rounded-full border border-amber-300/40 bg-amber-100/70 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.12em] text-amber-800 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-200"
				>
					Visiteur
				</span>
			{/if}
		</div>

		<div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[12px] leading-5">
			{#if hasDocs}
				<a
					href={docsUrl}
					target="_blank"
					rel="noreferrer"
					class="text-zinc-700 transition hover:text-zinc-950 dark:text-zinc-200 dark:hover:text-white"
				>
					Documentation ↗
				</a>
			{:else}
				<span class="text-zinc-500 dark:text-zinc-500">Pas de doc</span>
			{/if}

			{#if installEnabled}
				<a
					href={installHref}
					class="font-medium text-cyan-700 transition hover:text-cyan-800 dark:text-cyan-200 dark:hover:text-white"
				>
					Installer →
				</a>
			{:else}
				<span class="text-zinc-500 dark:text-zinc-500">Connexion requise</span>
			{/if}
		</div>
	</div>

	{#if !isLast}
		<div
			class="mx-3 h-px bg-[linear-gradient(90deg,rgba(34,211,238,0.55),rgba(59,130,246,0.28),rgba(168,85,247,0.35),rgba(16,185,129,0.28))] dark:bg-[linear-gradient(90deg,rgba(34,211,238,0.7),rgba(59,130,246,0.35),rgba(168,85,247,0.45),rgba(16,185,129,0.35))]"
		></div>
	{/if}
</div>