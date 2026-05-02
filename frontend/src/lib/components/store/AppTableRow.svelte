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

<div
	class={`transition-colors duration-150 hover:bg-black/[0.02] dark:hover:bg-white/[0.03] ${!isLast ? 'border-b border-black/5 dark:border-white/10' : ''}`}
>
	<div class="items-center gap-4 px-5 py-4 md:grid md:grid-cols-[minmax(0,1.1fr)_minmax(0,1.6fr)_170px_150px_220px]">
		<div class="min-w-0">
			<h3 class={`truncate text-sm font-semibold tracking-[-0.01em] ${titleClass}`}>
				{title}
			</h3>
			<p class="mt-1 truncate text-xs font-mono text-zinc-500 dark:text-zinc-500">
				{slug}
			</p>
		</div>

		<div class="min-w-0">
			<p class="line-clamp-2 text-sm leading-6 text-zinc-700 dark:text-zinc-300">
				{subtitle}
			</p>
		</div>

		<div>
			<span
				class={`inline-flex items-center rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.12em] ${categoryClass}`}
			>
				{category}
			</span>
		</div>

		<div>
			<span
				class={`inline-flex items-center rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.12em] ${docsClass}`}
			>
				{docsLabel}
			</span>
		</div>

		<div class="flex items-center justify-end gap-2">
			{#if hasDocs}
				<a
					href={docsUrl}
					target="_blank"
					rel="noreferrer"
					class="inline-flex items-center gap-2 rounded-[12px] border border-black/8 bg-black/[0.03] px-3 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-800 transition duration-200 hover:border-cyan-300 hover:bg-cyan-50 hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-100 dark:hover:border-cyan-400/20 dark:hover:bg-cyan-400/10 dark:hover:text-white"
				>
					<span>Doc</span>
					<span>↗</span>
				</a>
			{/if}

			{#if installEnabled}
				<a
					href={installHref}
					class="inline-flex items-center gap-2 rounded-[12px] border border-cyan-200 bg-cyan-50 px-3 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-cyan-800 transition duration-200 hover:border-cyan-300 hover:bg-cyan-100 hover:text-cyan-900 dark:border-cyan-400/20 dark:bg-cyan-400/10 dark:text-cyan-100 dark:hover:border-cyan-400/30 dark:hover:bg-cyan-400/15 dark:hover:text-white"
				>
					<span>Installer</span>
					<span>→</span>
				</a>
			{:else}
				<button
					type="button"
					disabled
					class="inline-flex cursor-not-allowed items-center gap-2 rounded-[12px] border border-zinc-300/60 bg-zinc-100/70 px-3 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-500 opacity-90 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-500"
					title="Connexion requise pour installer"
				>
					Connexion
				</button>
			{/if}
		</div>
	</div>
</div>