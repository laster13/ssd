<script lang="ts">
	import MarkdownContent from '$lib/components/forum/MarkdownContent.svelte';
	import type { ForumPostRevision, ForumTopicRevision } from '$lib/types/forum';

	type TopicMode = {
		mode: 'topic';
		title: string;
		revisions: ForumTopicRevision[];
	};

	type PostMode = {
		mode: 'post';
		title: string;
		revisions: ForumPostRevision[];
	};

	let {
		open = false,
		data,
		onClose
	}: {
		open: boolean;
		data: TopicMode | PostMode;
		onClose: () => void;
	} = $props();

	function formatDate(value: string) {
		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(value));
	}
</script>

{#if open}
	<div
		class="fixed inset-0 z-[100] bg-black/50 backdrop-blur-sm"
		role="button"
		tabindex="0"
		onclick={onClose}
		onkeydown={(event) => {
			if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') onClose();
		}}
	>
		<div class="flex min-h-full items-center justify-center p-4">
			<div
				class="max-h-[90vh] w-full max-w-5xl overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-800 dark:bg-zinc-950"
				role="dialog"
				aria-modal="true"
				aria-label="Historique des éditions"
				onclick={(event) => event.stopPropagation()}
			>
				<div class="flex items-center justify-between border-b border-zinc-200 px-6 py-4 dark:border-zinc-800">
					<div>
						<p class="text-sm font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
							Historique
						</p>
						<h2 class="mt-1 text-xl font-semibold text-zinc-900 dark:text-zinc-100">
							{data.title}
						</h2>
					</div>

					<button
						type="button"
						class="rounded-2xl border border-zinc-300 px-4 py-2 text-sm text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
						onclick={onClose}
					>
						Fermer
					</button>
				</div>

				<div class="max-h-[calc(90vh-88px)] overflow-y-auto p-6">
					{#if data.revisions.length > 0}
						<div class="space-y-6">
							{#each data.revisions as revision}
								<section class="rounded-3xl border border-zinc-200 bg-zinc-50 p-5 dark:border-zinc-800 dark:bg-zinc-900/60">
									<div class="mb-4 flex flex-wrap gap-x-4 gap-y-2 text-sm text-zinc-500 dark:text-zinc-400">
										<span>Édité par {revision.editor.email}</span>
										<span>Le {formatDate(revision.created_at)}</span>
									</div>

									{#if data.mode === 'topic'}
										<div class="mb-4">
											<div class="mb-2 text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
												Ancien titre
											</div>
											<div class="rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm font-medium text-zinc-900 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-100">
												{revision.previous_title}
											</div>
										</div>
									{/if}

									<div>
										<div class="mb-2 text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
											Ancien contenu
										</div>
										<div class="rounded-2xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950">
											<MarkdownContent content={revision.previous_content} />
										</div>
									</div>
								</section>
							{/each}
						</div>
					{:else}
						<div class="rounded-3xl border border-dashed border-zinc-300 bg-zinc-50 p-6 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/50 dark:text-zinc-300">
							Aucune révision enregistrée.
						</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}