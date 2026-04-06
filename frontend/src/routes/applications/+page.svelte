<script lang="ts">
	import ApplicationInventory from '$lib/components/apps/ApplicationInventory.svelte';
	import InstallationsHistory from '$lib/components/apps/InstallationsHistory.svelte';
	import type { ApplicationState, HistoryFilter, Job, Machine } from '$lib/utils/jobs';

	let { data, form } = $props();

	const applications = $derived((data.applications ?? []) as ApplicationState[]);
	const jobs = $derived((data.jobs ?? []) as Job[]);
	const machines = $derived((data.machines ?? []) as Machine[]);

	const activeTab = $derived(
		(data.initialTab === 'history' ? 'history' : 'applications') as 'applications' | 'history'
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
				<div class="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
					<div>
						<h1 class="text-3xl font-semibold tracking-[-0.06em] text-zinc-950 dark:text-zinc-50 sm:text-4xl">
							Pilote tes Applications
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
	<ApplicationInventory {applications} {machines} {uninstallError} {uninstallSuccess} />
{:else}
	<InstallationsHistory {jobs} filter={historyFilter} {deleteError} {deleteSuccess} />
{/if}