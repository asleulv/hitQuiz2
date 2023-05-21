<script>
	import { scale, fade } from 'svelte/transition';
	import { Confetti } from 'svelte-confetti';
	import InfoScreen from '$lib/components/InfoScreen.svelte';
	import ScoreForm from '$lib/components/ScoreForm.svelte';
	import Timer from '$lib/components/Timer.svelte';
	import { background } from '$lib/stores.js';
	import { hexToRgb, hsvToRgb, rgbToHex, rgbToHsv } from '$lib/utils.js';


	let state = 1;
	let score = 0;
	let level = 1;
	let timer = null;

	let promise = fetch('/questions/').then(x => x.json());

	const startTimer = () => {
		timer.reset();
		timer.start();
	}
	
	const onSubmit = (e) => {
		const {submitter} = e;
		timer.stop();
		promise = fetch('/questions/', {
			method: 'post', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ value: submitter.value })
		}).then(x => x.json());
	};

	const onClick = () => {
		state = 1;
		timer.reset();
		promise = fetch('/questions/').then(x => x.json());
	};

	const onHide = () => {
		state = 0;
		startTimer();
	};

	const onStop = () => {
		promise = fetch('/questions/', {
			method: 'post', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ value: '' })
		}).then(x => x.json());
	};

	$: promise.then(data => { 
		if (score != data.points) score = data.points;
		if (level != data.level) {
			level = data.level; 
			timer.stop();
			timer.reset()
			state = 1;
		}
		if (data.finished) {
			state = 2;
			timer.reset()
		} else if (!data.finished && state == 0) {
			startTimer();
		}
	});

	$: level, (() => {
		let changeFactor = 30 * (1 + Math.floor(Math.random() * 10));
		let [h,s,v] = rgbToHsv(...hexToRgb($background)); 
		background.set(rgbToHex(...hsvToRgb((h + changeFactor) % 360, s, v)));
	})();
</script>

<div class="app" style:background-color={$background}>
	<div class="wrapper">
		<div class="hud">
			<div class="brand">hitQuiz</div>
			<Timer bind:this={timer} on:stop={onStop} />
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
			{#if state == 2}
				<InfoScreen success={score > 1}>
					<h1>{#if score > 0}Congratulations!{:else}Sorry!{/if}</h1>
					<p>You finished the quiz with {score} points.</p>
					<ScoreForm success={score >= 50} />
					<button on:click={onClick}>Try Again</button>
				</InfoScreen>
			{:else if state == 1}
				<InfoScreen success={level > 1}>
					{#if level > 1}
						<h1>Level Up</h1>
						<p>Congratulations you have reached level {level}.</p>
						<button on:click={onHide}>Continue</button>
					{:else}
						<h1>Let's go.</h1>
						<p>In each level you will be presented with a few tracks and a selection of artists. Choose the artist or band that had a hit with the track shown. Hurry up, time is valuable.</p>
						<p>Get ready for level {level}.</p>
						<button on:click={onHide} class="btn">I am ready</button>
					{/if}
				</InfoScreen>
			{:else}
				<div>
					<div class="question-wrapper">
						{#key data.question_info}
							<h2 class="question-info" in:fade={{ duration: 800 }}>{data.question_info}</h2>
						{/key}
						{#key data.question}
							<h1 class="question" in:fade={{ duration: 800 }}>{data.question}</h1>
						{/key}
					</div>
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
		background: linear-gradient(180deg, rgba(40,44,52,1) 0%, rgba(0,0,0,0.284) 25%, rgba(0,0,0,0) 55%);
		color: white;
		font-size: calc(8px + 1.5vmin);
		min-height: 100vh;
		padding: 2.4rem;
		transition: background-color 0.5s ease;
  	}

  	.wrapper {
  		max-width: 720px;
  		margin: auto;
  	}

	.hud {
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		align-items: center;
		gap: .6rem;
	}

	.brand {
		font-weight: 750;
		font-size: 1.8em;
		margin-right: auto;
	}

	.quest-form {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		grid-auto-rows: 1fr;
		column-gap: 10px;
		row-gap: 15px;
	}

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

	.quest-form button:hover {
		background-color: #dedede;
	}

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

	.question-wrapper {
		min-height: 12.5rem;
		margin: 1.8rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.question {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.question-info {
		margin: 0.64rem;
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

		.hud div {
			max-width: 36px;
		}
	}

</style>