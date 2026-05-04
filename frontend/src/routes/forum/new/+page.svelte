<script lang="ts">
	import ImageUploadButton from '$lib/components/forum/ImageUploadButton.svelte';
	import MarkdownPreview from '$lib/components/forum/MarkdownPreview.svelte';

	let { data, form } = $props();

	const { categories, user, csrfToken } = data;

	const values = form?.values ?? {
		category_slug: 'tutoriels',
		related_tutorial_slug: '',
		title: '',
		content: ''
	};

	let liveContent = $state(values.content);

	function insertMarkdown(markdown: string) {
		liveContent = `${liveContent}\n${markdown}\n`.trim();
	}
</script>

<svelte:head>
	<title>Créer un sujet | Forum SSD</title>
</svelte:head>

<div class="mx-auto w-full max-w-7xl py-6 sm:px-6 sm:py-8 lg:px-8">
	<div class="px-4 sm:px-0">
		<a
			href="/forum"
			class="text-sm font-medium text-zinc-600 underline underline-offset-4 dark:text-zinc-300"
		>
			← Retour au forum
		</a>
	</div>

	<section class="mt-6 border-y border-zinc-200 px-4 py-6 dark:border-zinc-800 sm:rounded-3xl sm:border sm:bg-white sm:p-6 sm:shadow-sm dark:sm:bg-zinc-950/40">
		<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
			Nouveau sujet
		</p>
		<h1 class="mt-2 text-3xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-100">
			Créer une discussion claire et exploitable
		</h1>
		<p class="mt-3 max-w-3xl text-sm leading-6 text-zinc-600 dark:text-zinc-300">
			Décris précisément ton problème, ajoute si besoin une capture et utilise l’aperçu pour
			vérifier la mise en forme avant publication.
		</p>

		{#if user}
			<form method="POST" class="mt-8 space-y-6">
				<input type="hidden" name="_csrf" value={csrfToken} />

				<div class="grid gap-5 lg:grid-cols-2">
					<div>
						<label
							for="category_slug"
							class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200"
						>
							Catégorie
						</label>
						<select
							id="category_slug"
							name="category_slug"
							required
							class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
						>
							{#each categories as category}
								<option
									value={category.slug}
									selected={values.category_slug === category.slug}
								>
									{category.name}
								</option>
							{/each}
						</select>
					</div>

					<div>
						<label
							for="related_tutorial_slug"
							class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200"
						>
							Tutoriel lié
							<span class="font-normal text-zinc-500 dark:text-zinc-400">(optionnel)</span>
						</label>
						<input
							id="related_tutorial_slug"
							name="related_tutorial_slug"
							type="text"
							value={values.related_tutorial_slug}
							placeholder="Ex. nextcloud"
							class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
						/>
					</div>
				</div>

				<div>
					<label
						for="title"
						class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200"
					>
						Titre
					</label>
					<input
						id="title"
						name="title"
						type="text"
						required
						minlength="5"
						maxlength="200"
						value={values.title}
						placeholder="Ex. Erreur 502 à la fin du tuto Nextcloud"
						class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
					/>
				</div>

				<div class="grid gap-6 xl:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)]">
					<div class="space-y-4">
						<div>
							<label
								for="content"
								class="mb-2 block text-sm font-medium text-zinc-800 dark:text-zinc-200"
							>
								Message en markdown
							</label>
							<textarea
								id="content"
								name="content"
								rows="16"
								required
								minlength="10"
								maxlength="20000"
								bind:value={liveContent}
								placeholder="Décris précisément ton problème, les étapes suivies, les messages d’erreur et ce que tu as déjà testé."
								class="w-full rounded-2xl border border-zinc-300 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
							></textarea>
						</div>

						<div class="rounded-2xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
							<ImageUploadButton onUploaded={insertMarkdown} />
						</div>

						<div class="rounded-2xl border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900/60 dark:text-zinc-200">
							Sois précis : environnement, étapes suivies, message d’erreur, tests déjà faits.
						</div>
					</div>

					<div class="border-t border-zinc-200 pt-4 dark:border-zinc-800 xl:border-l xl:border-t-0 xl:pl-6 xl:pt-0">
						<div class="mb-3">
							<h2 class="text-base font-semibold text-zinc-950 dark:text-zinc-100">Aperçu</h2>
							<p class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
								Le rendu sera affiché ainsi après publication.
							</p>
						</div>

						<MarkdownPreview content={liveContent} />
					</div>
				</div>

				{#if form?.error}
					<div class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
						{form.error}
					</div>
				{/if}

				<div class="flex flex-wrap gap-3">
					<button
						type="submit"
						class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
					>
						Créer le sujet
					</button>

					<a
						href="/forum"
						class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
					>
						Annuler
					</a>
				</div>
			</form>
		{:else}
			<div class="mt-8 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900/60 dark:text-zinc-200">
				Tu dois être connecté pour créer un sujet.
				<a href="/login?next=/forum/new" class="ml-1 font-medium underline underline-offset-4">
					Se connecter
				</a>
			</div>
		{/if}
	</section>
</div>