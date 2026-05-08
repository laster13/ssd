<script lang="ts">
	import FileUploadButton from '$lib/components/forum/FileUploadButton.svelte';
	import ImageUploadButton from '$lib/components/forum/ImageUploadButton.svelte';
	import MarkdownPreview from '$lib/components/forum/MarkdownPreview.svelte';

	let { data, form } = $props();

	const { categories, user, csrfToken } = data;

	const values = form?.values ?? data.values ?? {
		category_slug: 'tutoriels',
		related_tutorial_slug: '',
		title: '',
		content: ''
	};

	let liveContent = $state(values.content);

	const loginNext = $derived(
		values.related_tutorial_slug
			? `/login?next=${encodeURIComponent(
					`/forum/new?tutorial=${values.related_tutorial_slug}&title=${values.title}`
				)}`
			: '/login?next=/forum/new'
	);

	function insertImage(markdown: string) {
		liveContent = `${liveContent}\n${markdown}\n`.trim();
	}

	function insertFile(markdown: string) {
		liveContent = `${liveContent}\n${markdown}\n`.trim();
	}
</script>

<svelte:head>
	<title>Créer un sujet | Forum SSD</title>
</svelte:head>

<div class="mx-auto w-full max-w-7xl py-6 pb-28 sm:px-6 sm:py-8 sm:pb-8 lg:px-8">
	<div class="px-4 sm:px-0">
		<div class="flex flex-wrap gap-3">
			<a
				href="/forum"
				class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				← Retour au forum
			</a>

			{#if values.related_tutorial_slug}
				<a
					href={`/tutos/${values.related_tutorial_slug}`}
					class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
				>
					← Retour au tuto
				</a>
			{/if}

			<a
				href="/"
				class="inline-flex items-center justify-center rounded-2xl border border-zinc-300 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				⌂ Accueil
			</a>
		</div>
	</div>

	<section class="mt-6 border-y border-zinc-200 px-4 py-6 dark:border-zinc-800 sm:rounded-3xl sm:border sm:bg-white sm:p-6 sm:shadow-sm dark:sm:bg-zinc-950/40">
		<p class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
			Nouveau sujet
		</p>

		<h1 class="mt-2 text-3xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-100">
			Créer une discussion claire et exploitable
		</h1>

		<p class="mt-3 max-w-3xl text-sm leading-6 text-zinc-600 dark:text-zinc-300">
			Décris précisément ton problème, ajoute si besoin une capture ou un fichier, et utilise
			l’aperçu pour vérifier la mise en forme avant publication.
		</p>

		{#if values.related_tutorial_slug}
			<div class="mt-5 rounded-2xl border border-indigo-200 bg-indigo-50 px-4 py-3 text-sm text-indigo-800 dark:border-indigo-900/50 dark:bg-indigo-950/20 dark:text-indigo-300">
				Ce sujet sera lié au tutoriel :
				<a
					href={`/tutos/${values.related_tutorial_slug}`}
					class="font-semibold underline underline-offset-4"
				>
					{values.related_tutorial_slug}
				</a>
			</div>
		{/if}

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
								<option value={category.slug} selected={values.category_slug === category.slug}>
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
							<div class="flex flex-wrap gap-3">
								<ImageUploadButton onUploaded={insertImage} />
								<FileUploadButton onUploaded={insertFile} />
							</div>
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
						href={values.related_tutorial_slug ? `/tutos/${values.related_tutorial_slug}` : '/forum'}
						class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
					>
						Annuler
					</a>
				</div>
			</form>
		{:else}
			<div class="mt-8 rounded-2xl border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900/60 dark:text-zinc-200">
				Tu dois être connecté pour créer un sujet.
				<a href={loginNext} class="ml-1 font-medium underline underline-offset-4">
					Se connecter
				</a>
			</div>
		{/if}
	</section>
</div>

<div class="fixed inset-x-0 bottom-0 z-30 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] lg:hidden">
	<div class="mx-auto max-w-sm rounded-[1.5rem] border border-zinc-200/70 bg-white/80 p-1.5 shadow-[0_10px_30px_rgba(0,0,0,0.10)] backdrop-blur-xl dark:border-zinc-800/70 dark:bg-zinc-900/80">
		<div class="grid grid-cols-3 gap-1.5">
			<a
				href="/forum"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100/80 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800/80 dark:hover:text-zinc-100"
			>
				<span class="text-base leading-none">←</span>
				<span>Forum</span>
			</a>

			<a
				href="/"
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] px-3 py-2.5 text-sm font-medium text-zinc-600 transition hover:bg-zinc-100/80 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800/80 dark:hover:text-zinc-100"
			>
				<span class="text-base leading-none">⌂</span>
				<span>Accueil</span>
			</a>

			<a
				href={values.related_tutorial_slug ? `/tutos/${values.related_tutorial_slug}` : '/tutos'}
				class="inline-flex items-center justify-center gap-2 rounded-[1.1rem] bg-gradient-to-r from-zinc-900 to-zinc-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm transition active:scale-[0.98] dark:from-white dark:to-zinc-200 dark:text-zinc-900"
			>
				<span class="text-base leading-none">←</span>
				<span>Tuto</span>
			</a>
		</div>
	</div>
</div>