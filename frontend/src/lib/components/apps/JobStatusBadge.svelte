<script lang="ts">
	import { humanJobStatus, jobStatusClass } from '$lib/utils/jobs';
	import type { JobStatusVariant } from '$lib/utils/jobs';

	let {
		status,
		variant = 'history',
		className = ''
	}: {
		status: string;
		variant?: JobStatusVariant;
		className?: string;
	} = $props();
</script>

<span
	class={`group relative inline-flex overflow-hidden rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] shadow-[0_10px_24px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.78)] backdrop-blur-xl dark:shadow-[0_10px_24px_rgba(0,0,0,0.24),inset_0_1px_0_rgba(255,255,255,0.04)] ${jobStatusClass(status)} ${className}`}
>
	<span class="pointer-events-none absolute inset-0 opacity-70 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.38),transparent_58%)] dark:bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.10),transparent_58%)]"></span>
	<span class="pointer-events-none absolute inset-0 opacity-0 transition duration-300 group-hover:opacity-100 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.16),transparent_60%)] dark:bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.08),transparent_60%)]"></span>
	<span class="relative">{humanJobStatus(status, variant)}</span>
</span>