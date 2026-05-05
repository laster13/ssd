<script lang="ts">
	let {
		onUploaded,
		label = 'Ajouter un fichier'
	}: {
		onUploaded: (markdown: string) => void;
		label?: string;
	} = $props();

	let fileInput: HTMLInputElement | null = null;
	let uploading = $state(false);
	let error = $state('');

	async function handleChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		const file = input.files?.[0];

		if (!file) return;

		error = '';
		uploading = true;

		try {
			const formData = new FormData();
			formData.set('file', file);

			const response = await fetch('/api/forum/upload-file', {
				method: 'POST',
				body: formData
			});

			const payload = await response.json();

			if (!response.ok) {
				throw new Error(payload?.error || "Impossible d'envoyer le fichier.");
			}

			onUploaded(payload.markdown);
			input.value = '';
		} catch (err) {
			error = err instanceof Error ? err.message : "Impossible d'envoyer le fichier.";
		} finally {
			uploading = false;
		}
	}
</script>

<div class="space-y-2">
	<input
		bind:this={fileInput}
		type="file"
		accept=".pdf,.txt,.md,.csv,.json,.zip,.rar,.7z,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
		class="hidden"
		onchange={handleChange}
	/>

	<button
		type="button"
		class="rounded-2xl border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 disabled:cursor-not-allowed disabled:opacity-60 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
		disabled={uploading}
		onclick={() => fileInput?.click()}
	>
		{uploading ? 'Envoi...' : label}
	</button>

	{#if error}
		<p class="text-sm text-red-600 dark:text-red-400">{error}</p>
	{/if}

	<p class="text-xs text-zinc-500 dark:text-zinc-400">
		PDF, TXT, MD, CSV, JSON, ZIP, RAR, 7Z, DOC, DOCX, XLS, XLSX, PPT, PPTX • 20 MB max
	</p>
</div>