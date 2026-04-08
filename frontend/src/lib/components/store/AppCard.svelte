<script lang="ts">
	import { resolveAppVisual } from '$lib/icons/app-icons';

	type App = {
		name?: string;
		slug?: string;
		description?: string;
		tagline?: string;
		category?: string;
		status?: string;
		docs_url?: string | null;
		docs_status?: string | null;
	};

	let { app, compact = false } = $props<{
		app: App;
		compact?: boolean;
	}>();

	const visual = $derived(resolveAppVisual(app.slug ?? '', app.description ?? ''));

	const name = $derived(app.name ?? 'Application');
	const slug = $derived(app.slug ?? '');
	const description = $derived(app.description ?? '');
	const tagline = $derived(app.tagline ?? app.description ?? '');
	const installHref = $derived(`/installations/new?app=${encodeURIComponent(slug)}`);
	const docsUrl = $derived(app.docs_url ?? '');
	const hasDocs = $derived(Boolean(docsUrl));
	const badge = $derived(app.name ?? 'Application');
</script>

{#if compact}
	<article
		class="group relative min-h-[214px] overflow-hidden rounded-[32px] border border-black/5 bg-[rgba(255,255,255,0.72)] p-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)] ring-1 ring-inset ring-black/[0.03] transform-gpu transition-[transform,border-color,box-shadow] duration-500 hover:-translate-y-2 hover:scale-[1.015] hover:border-black/10 hover:shadow-[0_30px_90px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-[rgba(10,10,14,0.72)] dark:ring-white/[0.04] dark:shadow-[0_20px_60px_rgba(0,0,0,0.42)] dark:hover:border-white/20 dark:hover:shadow-[0_30px_90px_rgba(0,0,0,0.58)]"
		style="will-change: transform;"
	>
		<div class="pointer-events-none absolute inset-0">
			<div
				class="absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.82),rgba(255,255,255,0.70))] dark:bg-[radial-gradient(circle_at_top_left,rgba(244,114,182,0.16),transparent_30%),radial-gradient(circle_at_bottom_right,rgba(96,165,250,0.14),transparent_32%),linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"
			></div>
			<div class="absolute inset-x-0 top-0 h-px bg-black/5 dark:bg-white/10"></div>
			<div class="absolute -left-20 top-0 h-36 w-36 rounded-full opacity-0 blur-2xl transition-opacity duration-500 dark:bg-fuchsia-400/[0.08] dark:opacity-100 group-hover:opacity-100"></div>
			<div class="absolute -right-20 bottom-0 h-36 w-36 rounded-full opacity-0 blur-2xl transition-opacity duration-500 dark:bg-sky-400/[0.08] dark:opacity-100 group-hover:opacity-100"></div>
		</div>

		<div class="relative flex h-full flex-col">
			<div class="flex items-start justify-between gap-4">
				<div class="relative">
					<div
						class="absolute -inset-3 rounded-[28px] opacity-0 transition-[transform,opacity] duration-500 group-hover:scale-110 dark:bg-[radial-gradient(circle,rgba(168,85,247,0.22),transparent_70%)] dark:opacity-70 dark:group-hover:opacity-100"
					></div>

					<div
						class="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] border border-black/5 shadow-[0_6px_18px_rgba(15,23,42,0.06)] transform-gpu transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:scale-[1.04] dark:border-white/10 dark:shadow-[0_12px_34px_rgba(0,0,0,0.24),inset_0_1px_0_rgba(255,255,255,0.10)]"
						style={`background:${visual.bg}; will-change: transform; filter:none;`}
					>
						<div
							class="pointer-events-none absolute inset-0 rounded-[22px] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.12),rgba(255,255,255,0.02)_40%,transparent)]"
						></div>
						<div class="scale-[0.98] transform-gpu transition-transform duration-300 group-hover:scale-[1.03]">
							{@html visual.svg}
						</div>
					</div>
				</div>

				<span
					class="shrink-0 rounded-full border border-fuchsia-300/30 bg-fuchsia-200/60 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-fuchsia-700 dark:border-fuchsia-200/20 dark:bg-fuchsia-300/10 dark:text-fuchsia-100"
				>
					{badge}
				</span>
			</div>

			<p class="mt-8 max-w-[78%] line-clamp-2 text-[14px] leading-6 text-zinc-600 dark:text-zinc-400">
				{description || tagline}
			</p>

			<div class="mt-auto flex items-center justify-end gap-3 pt-6">
				{#if hasDocs}
					<a
						href={docsUrl}
						target="_blank"
						rel="noreferrer"
						class="inline-flex items-center gap-2 rounded-[14px] border border-black/8 bg-black/[0.02] px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)] transition-[transform,border-color,background-color,box-shadow] duration-300 hover:border-black/12 hover:bg-black/[0.06] hover:text-zinc-950 hover:shadow-[0_10px_24px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.08)] dark:hover:border-white/20 dark:hover:bg-white/[0.10] dark:hover:text-white dark:hover:shadow-[0_10px_24px_rgba(255,255,255,0.06)]"
					>
						<span>Documentation</span>
						<span>↗</span>
					</a>
				{/if}

				<a
					href={installHref}
					class="inline-flex items-center gap-2 rounded-[14px] border border-black/8 bg-black/[0.04] px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)] transition-[transform,border-color,background-color,box-shadow] duration-300 hover:border-black/12 hover:bg-black/[0.08] hover:shadow-[0_10px_24px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.08] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.08)] dark:hover:border-white/20 dark:hover:bg-white/[0.14] dark:hover:shadow-[0_10px_24px_rgba(255,255,255,0.06)]"
				>
					<span>Installer</span>
					<span class="transform-gpu transition-transform duration-300 group-hover:translate-x-0.5">→</span>
				</a>
			</div>
		</div>
	</article>
{:else}
	<article
		class="group relative min-h-[214px] overflow-hidden rounded-[32px] border border-black/5 bg-[rgba(255,255,255,0.74)] p-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)] ring-1 ring-inset ring-black/[0.03] transform-gpu transition-[transform,border-color,box-shadow] duration-500 hover:-translate-y-2 hover:scale-[1.015] hover:border-black/10 hover:shadow-[0_30px_90px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-[rgba(10,10,14,0.74)] dark:ring-white/[0.04] dark:shadow-[0_20px_60px_rgba(0,0,0,0.42)] dark:hover:border-white/20 dark:hover:shadow-[0_30px_90px_rgba(0,0,0,0.58)]"
		style="will-change: transform;"
	>
		<div class="pointer-events-none absolute inset-0">
			<div
				class="absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.82),rgba(255,255,255,0.70))] dark:bg-[radial-gradient(circle_at_top_left,rgba(244,114,182,0.16),transparent_30%),radial-gradient(circle_at_bottom_right,rgba(96,165,250,0.14),transparent_32%),linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"
			></div>
			<div class="absolute inset-x-0 top-0 h-px bg-black/5 dark:bg-white/10"></div>
			<div class="absolute -left-20 top-0 h-36 w-36 rounded-full opacity-0 blur-2xl transition-opacity duration-500 dark:bg-fuchsia-400/[0.08] dark:opacity-100 group-hover:opacity-100"></div>
			<div class="absolute -right-20 bottom-0 h-36 w-36 rounded-full opacity-0 blur-2xl transition-opacity duration-500 dark:bg-sky-400/[0.08] dark:opacity-100 group-hover:opacity-100"></div>

			<div class="absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
				<div
					class="absolute inset-y-0 -left-1/2 w-1/2 rotate-12 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.45),transparent)] blur-lg transform-gpu transition-transform duration-700 group-hover:translate-x-[240%] dark:bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.07),transparent)]"
					style="will-change: transform;"
				></div>
			</div>
		</div>

		<div class="relative flex h-full flex-col">
			<div class="flex items-start justify-between gap-4">
				<div class="relative">
					<div
						class="absolute -inset-3 rounded-[28px] opacity-0 transition-[transform,opacity] duration-500 group-hover:scale-110 dark:bg-[radial-gradient(circle,rgba(168,85,247,0.22),transparent_70%)] dark:opacity-70 dark:group-hover:opacity-100"
					></div>

					<div
						class="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] border border-black/5 shadow-[0_6px_18px_rgba(15,23,42,0.06)] transform-gpu transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:scale-[1.04] dark:border-white/10 dark:shadow-[0_12px_34px_rgba(0,0,0,0.24),inset_0_1px_0_rgba(255,255,255,0.10)]"
						style={`background:${visual.bg}; will-change: transform; filter:none;`}
					>
						<div
							class="pointer-events-none absolute inset-0 rounded-[22px] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.12),rgba(255,255,255,0.02)_40%,transparent)]"
						></div>
						<div class="scale-[0.98] transform-gpu transition-transform duration-300 group-hover:scale-[1.03]">
							{@html visual.svg}
						</div>
					</div>
				</div>

				<span
					class="shrink-0 rounded-full border border-fuchsia-300/30 bg-fuchsia-200/60 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-fuchsia-700 dark:border-fuchsia-200/20 dark:bg-fuchsia-300/10 dark:text-fuchsia-100"
				>
					{badge}
				</span>
			</div>

			<p class="mt-8 max-w-[78%] line-clamp-2 text-[14px] leading-6 text-zinc-600 dark:text-zinc-400">
				{description || tagline}
			</p>

			<div class="mt-auto flex items-center justify-end gap-3 pt-6">
				{#if hasDocs}
					<a
						href={docsUrl}
						target="_blank"
						rel="noreferrer"
						class="inline-flex items-center gap-2 rounded-[14px] border border-black/8 bg-black/[0.02] px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)] transition-[transform,border-color,background-color,box-shadow] duration-300 hover:border-black/12 hover:bg-black/[0.06] hover:text-zinc-950 hover:shadow-[0_10px_24px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.08)] dark:hover:border-white/20 dark:hover:bg-white/[0.10] dark:hover:text-white dark:hover:shadow-[0_10px_24px_rgba(255,255,255,0.06)]"
					>
						<span>Documentation</span>
						<span>↗</span>
					</a>
				{:else}
					<span class="text-xs text-zinc-500 dark:text-zinc-400">Documentation non disponible</span>
				{/if}

				<a
					href={installHref}
					class="inline-flex items-center gap-2 rounded-[14px] border border-black/8 bg-black/[0.04] px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-zinc-900 shadow-[inset_0_1px_0_rgba(255,255,255,0.65)] transition-[transform,border-color,background-color,box-shadow] duration-300 hover:border-black/12 hover:bg-black/[0.08] hover:shadow-[0_10px_24px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.08] dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.08)] dark:hover:border-white/20 dark:hover:bg-white/[0.14] dark:hover:shadow-[0_10px_24px_rgba(255,255,255,0.06)]"
				>
					<span>Installer</span>
					<span class="transform-gpu transition-transform duration-300 group-hover:translate-x-0.5">→</span>
				</a>
			</div>
		</div>
	</article>
{/if}