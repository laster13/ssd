<script lang="ts">
	import ApplicationInventory from '$lib/components/apps/ApplicationInventory.svelte';
	import InstallationsHistory from '$lib/components/apps/InstallationsHistory.svelte';
	import type { HistoryFilter, Job, Machine } from '$lib/utils/jobs';

	let { data, form } = $props();

	const jobs = $derived((data.jobs ?? []) as Job[]);
	const machines = $derived((data.machines ?? []) as Machine[]);
	const activeTab = $derived(
		(data.initialTab === 'history' ? 'history' : 'applications') as
			| 'applications'
			| 'history'
	);
	const historyFilter = $derived((data.initialFilter ?? 'all') as HistoryFilter);

	const deleteError = $derived((form?.deleteError ?? null) as string | null);
	const deleteSuccess = $derived((form?.deleteSuccess ?? null) as string | null);

	const uninstallError = $derived((form?.uninstallError ?? null) as string | null);
	const uninstallSuccess = $derived((form?.uninstallSuccess ?? null) as string | null);
</script>

<svelte:head>
	<title>Applications</title>
</svelte:head>

<section class="relative isolate bg-zinc-50 dark:bg-[#07111f]">
	<div class="mx-auto max-w-7xl px-4 pb-6 pt-6 sm:px-6 lg:px-8 lg:pt-8">
		<div class="relative overflow-hidden rounded-[24px] border border-black/5 bg-white/80 shadow-[0_18px_50px_rgba(15,23,42,0.08)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_18px_50px_rgba(0,0,0,0.32)]">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.92),rgba(255,255,255,0.72)_45%,rgba(255,255,255,0.62)_100%)] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03)_45%,rgba(255,255,255,0.02)_100%)]"></div>
			<div class="pointer-events-none absolute inset-0 rounded-[24px] ring-1 ring-inset ring-white/70 dark:ring-white/10"></div>

			<div class="relative p-5 sm:p-6">
				<div class="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
					<div class="max-w-3xl">
						<div class="mb-3 flex flex-wrap items-center gap-2.5">
							<div class="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50/90 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.22em] text-emerald-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.06] dark:text-emerald-200">
								<span class="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500 dark:bg-emerald-400"></span>
								Applications
							</div>
						</div>

						<h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
							<span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
								Pilote tes Applications
							</span>
						</h1>

						<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-300 sm:text-[15px]">
							Suivre l’état actuel de tes applications et accéder à l’historique complet des installations.
						</p>
					</div>

					<div class="w-full max-w-md">
						<div class="rounded-[18px] border border-black/5 bg-white/80 p-2 shadow-[0_10px_24px_rgba(15,23,42,0.06)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_10px_24px_rgba(0,0,0,0.22)]">
							<div class="grid grid-cols-2 gap-2 rounded-[14px] border border-black/5 bg-black/[0.03] p-1 dark:border-white/10 dark:bg-white/[0.03]">
								<a
									href="/applications?tab=applications"
									class={`inline-flex items-center justify-center rounded-[12px] px-3 py-2.5 text-sm font-semibold transition ${
										activeTab === 'applications'
											? 'border border-black/10 bg-white text-zinc-950 shadow-sm dark:border-white/10 dark:bg-white/[0.10] dark:text-white'
											: 'border border-transparent bg-transparent text-zinc-600 hover:bg-white/80 hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white'
									}`}
								>
									Applications
								</a>

								<a
									href={`/applications?tab=history&filter=${historyFilter}`}
									class={`inline-flex items-center justify-center rounded-[12px] px-3 py-2.5 text-sm font-semibold transition ${
										activeTab === 'history'
											? 'border border-black/10 bg-white text-zinc-950 shadow-sm dark:border-white/10 dark:bg-white/[0.10] dark:text-white'
											: 'border border-transparent bg-transparent text-zinc-600 hover:bg-white/80 hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white'
									}`}
								>
									Historique
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

{#if activeTab === 'applications'}
	<ApplicationInventory
		{jobs}
		{machines}
		{uninstallError}
		{uninstallSuccess}
	/>
{:else}
	<InstallationsHistory {jobs} filter={historyFilter} {deleteError} {deleteSuccess} />
{/if}