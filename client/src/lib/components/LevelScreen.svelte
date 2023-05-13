<script>
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	export let visible = false;
	export let level = 1;

	function onClick() {
		dispatch('hide');
	}
</script>

{#key visible}
	<div class="level-screen" in:fade={{ duration: 800 }}>
		{#if level > 1}
			<h1>Level Up</h1>
			<p>Congratulations you have reached level {level}.</p>
			<button on:click={onClick}>Continue</button>
		{:else}
			<h1>Let's go.</h1>
			<p>In each level you will be presented with a few tracks and a selection of artists. Choose the artist or band that had a hit with the track shown. Hurry up, time is valuable.</p>
			<p>Get ready for level {level}.</p>
			<button on:click={onClick}>I am ready</button>
		{/if}
	</div>
{/key}

<style>
	.level-screen {
		margin: 5.6rem 0;
	}

	.level-screen p {
		margin: 1.2rem 0 2.4rem ;
	}

	.level-screen button {
		padding: 0.5rem 1.5rem;
		border: 1px solid #ddd;
		border-radius: 3px;
		background-color: #eee;
		font-size: 0.85em;
		transition-property: color, background-color;
		transition-duration: 200ms;
		transition-timing-function: ease-out;
	}

	.level-screen button:hover {
		background-color: #dedede;
	}

	.level-screen button:active {
		background: linear-gradient(-45deg, #aaa, #ccc, #aaa, #fff);
		background-size: 400% 400%; 
		animation: gradient 15s ease infinite;
	}
/*
	.level-screen button[disabled] {
		color: #dedede;
	}
*/
</style>