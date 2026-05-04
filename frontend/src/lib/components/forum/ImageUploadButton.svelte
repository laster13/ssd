<script lang="ts">
	let {
		onUploaded,
		label = 'Ajouter une image'
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
			formData.set('image', file);

			const response = await fetch('/api/forum/upload-image', {
				method: 'POST',
				body: formData
			});

			const payload = await response.json();

			if (!response.ok) {
				throw new Error(payload?.error || "Impossible d'envoyer l'image.");
			}

			onUploaded(payload.markdown);
			input.value = '';
		} catch (err) {
			error = err instanceof Error ? err.message : "Impossible d'envoyer l'image.";
		} finally {
			uploading = false;
		}
	}
</script>

<div class="space-y-2">
	<input
		bind:this={fileInput}
		type="file"
		accept="image/png,image/jpeg,image/webp,image/gif"
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
		<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
			{error}
		</div>
	{/if}

	<p class="text-xs text-zinc-500 dark:text-zinc-400">
		PNG, JPG, WEBP ou GIF • 5 MB max
	</p>
</div>