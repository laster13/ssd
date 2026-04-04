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
</script>

<svelte:head>
	<title>Applications</title>
</svelte:head>

<section class="relative isolate overflow-hidden">
	<div class="pointer-events-none absolute inset-0 -z-30 bg-[linear-gradient(180deg,#f8fafc_0%,#eef2ff_24%,#f8fafc_50%,#ecfeff_100%)] dark:bg-[linear-gradient(180deg,#050816_0%,#0b1020_38%,#0a1120_68%,#07111f_100%)]"></div>

	<div class="pointer-events-none absolute inset-0 -z-20 opacity-90">
		<div class="absolute left-[-8rem] top-[-7rem] h-[28rem] w-[28rem] rounded-full bg-cyan-400/18 blur-3xl dark:bg-cyan-400/16"></div>
		<div class="absolute right-[-10rem] top-[-5rem] h-[32rem] w-[32rem] rounded-full bg-fuchsia-400/14 blur-3xl dark:bg-fuchsia-500/14"></div>
		<div class="absolute bottom-[-12rem] left-[12%] h-[26rem] w-[26rem] rounded-full bg-emerald-400/14 blur-3xl dark:bg-emerald-400/12"></div>
		<div class="absolute bottom-[-8rem] right-[16%] h-[24rem] w-[24rem] rounded-full bg-sky-400/12 blur-3xl dark:bg-sky-400/10"></div>
	</div>

	<div class="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.9),transparent_24%),radial-gradient(circle_at_80%_0%,rgba(125,211,252,0.18),transparent_22%),radial-gradient(circle_at_20%_100%,rgba(52,211,153,0.14),transparent_18%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.06),transparent_20%),radial-gradient(circle_at_82%_0%,rgba(56,189,248,0.14),transparent_22%),radial-gradient(circle_at_18%_100%,rgba(16,185,129,0.12),transparent_18%)]"></div>

	<div class="pointer-events-none absolute inset-x-0 top-0 -z-10 h-px bg-gradient-to-r from-transparent via-black/10 to-transparent dark:via-white/12"></div>

	<div class="mx-auto max-w-7xl px-4 pb-8 pt-6 sm:px-6 lg:px-8 lg:pt-8">
		<div class="relative overflow-hidden rounded-[30px] border border-black/5 bg-white/75 shadow-[0_24px_70px_rgba(15,23,42,0.10)] backdrop-blur-3xl dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_24px_70px_rgba(0,0,0,0.42)]">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.88),rgba(255,255,255,0.64)_42%,rgba(255,255,255,0.52)_100%)] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.07),rgba(255,255,255,0.03)_45%,rgba(255,255,255,0.02)_100%)]"></div>
			<div class="pointer-events-none absolute inset-0 rounded-[30px] ring-1 ring-inset ring-white/70 dark:ring-white/10"></div>

			<div class="pointer-events-none absolute -left-12 top-0 h-56 w-56 rounded-full bg-emerald-400/10 blur-3xl dark:bg-emerald-400/10"></div>
			<div class="pointer-events-none absolute right-[-3rem] top-[-2rem] h-64 w-64 rounded-full bg-sky-400/10 blur-3xl dark:bg-sky-400/10"></div>

			<div class="relative p-5 sm:p-6 lg:p-7">
				<div class="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
					<div class="max-w-3xl">
						<div class="mb-3 flex flex-wrap items-center gap-2.5">
							<div class="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50/90 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.22em] text-emerald-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.06] dark:text-emerald-200">
								<span class="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.55)] dark:bg-emerald-400"></span>
								Applications
							</div>
						</div>

                                                <h1 class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]">
	                                                <span class="mt-1 block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]">
		                                                Pilote tes Applications
	                                                </span>
                                                </h1>

						<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-300 sm:text-[15px]">
							Suivre l’état actuel de tes applications et accéder à
							l’historique complet des installations.
						</p>
					</div>

					<div class="w-full max-w-md">
						<div class="relative overflow-hidden rounded-[22px] border border-black/5 bg-white/72 p-3 shadow-[0_14px_40px_rgba(15,23,42,0.10)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_14px_40px_rgba(0,0,0,0.30)]">
							<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.82),rgba(255,255,255,0.55))] dark:bg-[linear-gradient(135deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"></div>
							<div class="pointer-events-none absolute left-[-1.5rem] top-[-1.5rem] h-16 w-16 rounded-full bg-cyan-300/20 blur-2xl dark:bg-cyan-400/20"></div>
							<div class="pointer-events-none absolute bottom-[-1rem] right-[-1rem] h-16 w-16 rounded-full bg-violet-300/20 blur-2xl dark:bg-violet-400/16"></div>

							<div class="relative">

								<div class="grid grid-cols-2 gap-2 rounded-[18px] border border-black/5 bg-black/[0.03] p-1.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
									<a
										href="/applications?tab=applications"
										class={`group relative inline-flex items-center justify-center overflow-hidden rounded-[14px] px-3 py-2.5 text-sm font-semibold transition ${
											activeTab === 'applications'
												? 'border border-cyan-200 text-white shadow-[0_12px_24px_rgba(37,99,235,0.22)] dark:border-cyan-400/15'
												: 'border border-transparent bg-white/70 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.03] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.05]'
										}`}
									>
										{#if activeTab === 'applications'}
											<span class="absolute inset-0 bg-[linear-gradient(135deg,rgba(14,165,233,0.98),rgba(37,99,235,0.96),rgba(124,58,237,0.92))]"></span>
											<span class="absolute inset-0 opacity-80 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.26),transparent_55%)]"></span>
										{/if}
										<span class="relative">Applications</span>
									</a>

									<a
										href={`/applications?tab=history&filter=${historyFilter}`}
										class={`group relative inline-flex items-center justify-center overflow-hidden rounded-[14px] px-3 py-2.5 text-sm font-semibold transition ${
											activeTab === 'history'
												? 'border border-cyan-200 text-white shadow-[0_12px_24px_rgba(37,99,235,0.22)] dark:border-cyan-400/15'
												: 'border border-transparent bg-white/70 text-zinc-700 hover:border-black/8 hover:bg-white dark:bg-white/[0.03] dark:text-zinc-200 dark:hover:border-white/10 dark:hover:bg-white/[0.05]'
										}`}
									>
										{#if activeTab === 'history'}
											<span class="absolute inset-0 bg-[linear-gradient(135deg,rgba(14,165,233,0.98),rgba(37,99,235,0.96),rgba(124,58,237,0.92))]"></span>
											<span class="absolute inset-0 opacity-80 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.26),transparent_55%)]"></span>
										{/if}
										<span class="relative">Historique</span>
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="mt-5 flex items-center gap-3">
					<div class="h-px flex-1 bg-gradient-to-r from-transparent via-black/10 to-transparent dark:via-white/10"></div>
					<div class="rounded-full border border-black/5 bg-white/70 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-zinc-500 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
						Control Center
					</div>
					<div class="h-px flex-1 bg-gradient-to-r from-transparent via-black/10 to-transparent dark:via-white/10"></div>
				</div>
			</div>
		</div>
	</div>
</section>

{#if activeTab === 'applications'}
	<ApplicationInventory {jobs} {machines} />
{:else}
	<InstallationsHistory {jobs} filter={historyFilter} {deleteError} {deleteSuccess} />
{/if}