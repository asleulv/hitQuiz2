<script>
	import { scale, fade } from 'svelte/transition';
	import { Confetti } from 'svelte-confetti';

	let score = 0;
	let level = 1;
	let promise = fetch('/quiz').then(x => x.json());

	function onSubmit(e) {
		const {submitter} = e;
		promise = fetch('/quiz', {
			method: 'post', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ value: submitter.value })
		}).then(x => x.json());
	}

	function onClick() {
		promise = fetch('/quiz').then(x => x.json());
	}

	$: promise.then(data => { if (score != data.points) score = data.points; });
	$: promise.then(data => { if (level != data.level) level = data.level; });
</script>

<div class="app">
	<div class="wrapper">
		<div class="hud">
			{#key level}
				<div>Level: <span in:scale={{ delay: 100, duration: 800 }}>{level}</span></div>
			{/key}
			{#key score}
				<div>Score: <span in:fade={{ delay: 100, duration: 800 }}>{score}</span></div>
			{/key}
		</div>

		{#await promise}
			<div class="load-screen">
				<div class="lds-dual-ring"></div>
			</div>
		{:then data}
			{#if data.finished}
				{#key data.finished}
					<div in:fade={{ duration: 800 }} class="quest-info">
						<h1>{#if score > 0}Congratulations!<Confetti />{:else}Sorry!{/if}</h1>
						<h1>You finished the quiz with {score} points.</h1>
						<button on:click={onClick}>Try Again</button>
					</div>
				{/key}
			{:else}
				<div>
					{#key data.question_info}
						<h2 class="question_info" in:fade={{ duration: 800 }}>{data.question_info}</h2>
					{/key}
					{#key data.question}
						<h1 class="question" in:fade={{ duration: 800 }}>{data.question}</h1>
					{/key}
					{#key data.answers}
						<form class="quest-form" on:submit|preventDefault={onSubmit}>
							{#each Object.values(data.alternatives) as answer, i}
								<button type="submit" value="{ answer }" in:scale={{ duration: 400, delay: i*100 }}>{answer}</button>
							{/each}
						</form>
					{/key}
				</div>
			{/if}
		{:catch error}
			<p>{error.message}</p>
		{/await}
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
			'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
			sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}
	:global(*) {
		box-sizing: border-box;
	}
	.app {
		text-align: center;
		background-color: #282c34;
		color: white;
		font-size: calc(8px + 1.5vmin);
		min-height: 100vh;
		padding: 2.4rem;
  	}

  	.wrapper {
  		max-width: 720px;
  		margin: auto;
  	}

	.hud {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		gap: .6rem;
	}

	.quest-form {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		column-gap: 10px;
		row-gap: 15px;
	}

	.quest-info {
		margin: 5.6rem 0;
	}

	.quest-info button, 
	.quest-form button {
		padding: 0.5rem 1.5rem;
		border: 1px solid #ddd;
		border-radius: 3px;
		background-color: #eee;
		font-size: 0.85em;
		transition-property: color, background-color;
		transition-duration: 200ms;
		transition-timing-function: ease-out;
	}

	.quest-info button:hover, 
	.quest-form button:hover {
		background-color: #dedede;
	}

	.quest-info button:active, 
	.quest-form button:active {
		background: linear-gradient(-45deg, #aaa, #ccc, #aaa, #fff);
		background-size: 400% 400%; 
		animation: gradient 15s ease infinite;
	}
/*
	.quest-form button[disabled] {
		color: #dedede;
	}
*/
	@keyframes gradient {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}

	.question {
		min-height: 1rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.question_info {
		min-height: 1rem;
		display: flex;
		font-weight: lighter;
		align-items: center;
		justify-content: center;
	}

	.load-screen {
		position: absolute;
		bottom: 0px;
		right: 0px;
		z-index: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2.4rem;
	}

	.lds-dual-ring {
		display: inline-block;
		width: 48px;
		height: 48px;
	}

	.lds-dual-ring:after {
		content: " ";
		display: block;
		width: 24px;
		height: 24px;
		margin: 8px;
		border-radius: 50%;
		border: 4px solid #fff;
		border-color: #fff transparent #fff transparent;
		animation: lds-dual-ring .6s linear infinite;
	}

	@keyframes lds-dual-ring {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(180deg);
		}
	}

	@media only screen and (max-width: 480px) { /* 576*/
		.quest-form {
			grid-template-columns: repeat(1, 1fr);
		}
	}

</style>