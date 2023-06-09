<script>
	import { scale, fade } from 'svelte/transition';
	import { Confetti } from 'svelte-confetti';
	import InfoScreen from '$lib/components/InfoScreen.svelte';
	import Modal from '$lib/components/Modal.svelte';
	import Button from '$lib/components/Button.svelte';
	import ScoreForm from '$lib/components/ScoreForm.svelte';
	import ScoreList from '$lib/components/ScoreList.svelte';
	import Stats from '$lib/components/Stats.svelte';
	import Tabs from '$lib/components/Tabs.svelte';
	import Timer from '$lib/components/Timer.svelte';
	import Tooltip from '$lib/components/Tooltip.svelte';
	import { background } from '$lib/stores.js';
	import { hexToRgb, hsvToRgb, rgbToHex, rgbToHsv } from '$lib/utils.js';

	const tabs = [
		{ 
			label: 'Stats',
			value: 1,
			component: Stats, 
 			props: {}
		},
		{ 
			label: "Leaderboard",
			value: 2,
			component: ScoreList, 
 			props: {}
		},
  ];

	let state = 1;
	let score = 0;
	let level = 1;
	let lives = 3;
	let timer = null;

	let promise = fetch('/questions/').then(x => x.json());

	const startTimer = () => {
		timer.reset();
		timer.start();
	}
	
	const handleSubmit = (e) => {
		const {submitter} = e;
		timer.stop();
		promise = fetch('/questions/', {
			method: 'post', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ value: submitter.value })
		}).then(x => x.json());
	};

	/*
	const handleClick = () => {
		state = 1;
		timer.reset();
		promise = fetch('/questions/').then(x => x.json());
	};
*/
	const handleClick = async (file) => {
		switch (file) {
			case 'tryagain':
				state = 1;
				timer.reset();
				promise = fetch('/questions/').then(x => x.json());
				break; // Add break statement here

			case 'share':
				// promise = fetch('/share/').then(x => x.json());
				
				if (!('clipboard' in navigator)) {
					console.error('Clipboard not supported.');
					return;
				}

				const chars = ['🟢','🔴','⚪'];
				let stats = await fetch('/scores/stats').then(x => x.json());
				let value = `Level:\t${level}\nScore:\t${score}\n` 
					+ stats.fail_data.map((l,i) => {
							return `Level ${i+1}\t` + l.map(q => chars[q-1]).join('');
					}).join('\n')
					+ '\nVisit hitQuiz.me and try to beat me.';

				try {
					await navigator.clipboard.writeText(value);
				} catch(exc) {
					console.error('Error: ', exc)
				}

				break; // Add break statement here


			default:
				console.log('Invalid file:', file);
				break;
		}
	};

	const handleHide = () => {
		state = 0;
		startTimer();
	};

	const handleStop = () => {
		promise = fetch('/questions/', {
			method: 'post', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ value: '' })
		}).then(x => x.json());
	};

	$: promise.then(data => { 
		if (lives != data.lives) lives = data.lives;
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


	let modal = null;
	const showModal = () => {
		if (state > 0) modal.show();
	};
</script>

<svelte:head>
  <title>hitQuiz.me - Who had the hit?</title>
</svelte:head>

<div class="app" style:background-color={$background}>
	<div class="wrapper">
		<div class="hud">
			<div class="brand2">🎯hitQuiz.me</div>
			<Timer bind:this={timer} on:stop={handleStop} />
			<div class="score-wrapper">
				{#key lives}
					<div in:fade|global={{delay: 100, duration: 800}}>
						{#each {length: lives} as _}❤️{/each}
					</div>
				{/key}
				{#key level}
					<div>Level: <span in:scale|global={{ delay: 100, duration: 800 }}>{level}</span></div>
				{/key}
				{#key score}
					<div>Score: <span in:fade|global={{ delay: 100, duration: 800 }}>{score}</span></div>
				{/key}
				{#key state}
				<button 
					class="i-btn" 
					class:highlighted={state > 1} 
					on:click={showModal} 
					disabled={state == 0} 
					title="Additional Information"
					transition:scale|global
				>i</button>
				{/key}
			</div>
		</div>

		{#await promise}
			<div class="load-screen">
				<div class="lds-dual-ring"></div>
			</div>
		{:then data}
			{#if state == 2}
				<InfoScreen success={score > 1}>
					<p class="titletext">{#if score > 99}🥳 Well done!{:else if (score === 0)}😖 Very poor!{:else}😐 Meh...{/if}</p>
					<p class="thintext">You finished the quiz with {score} points.</p>
					<p class="thintext">{#if score < 100}100 points are required for a place on the leaderboard.{:else}You have earned a place on the leaderboard!{/if}</p>
					{#if score > 0}<ScoreForm success={score >= 100} />{/if}
					<div class="button-container">
						<Button type="primary" handleClick={handleClick} goToUrl="share" id="share-btn">〽️ Share results</Button>
						<Button type="primary" handleClick={handleClick} goToUrl="tryagain">↻ Try Again</Button>
						<Tooltip target="#share-btn" trigger="click" position="top">Copied</Tooltip>
					</div>
				</InfoScreen>
			{:else if state == 1}
				<InfoScreen success={level > 1}>
					{#if level > 1}
						<p class="titletext">Level Up</p>
						<p>Congratulations you have reached level {level}.</p>
						<button on:click={handleHide}>Continue</button>
					{:else}
						<p class="titletext">Who had the hit?</p>
						<p class="thintext">Given the song title, year and peak position the question remains exactly that…</p>
						<p class="thintext">If you score 100 points or more you'll get your name on the leaderboard. What an honor!</p>
						<p>Get ready for level {level}.</p>
						<button on:click={handleHide} class="btn">🚀 Let's go!</button>
					{/if}
				</InfoScreen>
			{:else}
				<div>
					<div class="question-wrapper">
						{#key data.question_info}
							<h2 class="question-info" in:fade|global={{ duration: 800 }}>{data.question_info}</h2>
						{/key}
						{#key data.question}
							<p class="titletext" in:fade|global={{ duration: 800 }}>{data.question}</p>
						{/key}
					</div>
					{#key data.answers}
						<form class="quest-form" on:submit|preventDefault={handleSubmit}>
							{#each Object.values(data.alternatives) as answer, i}
								<button type="submit" value="{ answer }" in:scale|global={{ duration: 400, delay: i*100 }}>{answer}</button>
							{/each}
						</form>
					{/key}
				</div>
			{/if}
		{:catch error}
			<p>{error.message}</p>
		{/await}
	</div>
	<Modal bind:this={modal}> 
		<Tabs {tabs} />
	</Modal>
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
		z-index: 1;
	}

	.brand2 {
		font-weight: 750;
		font-size: 1.4em;
		margin-right: auto;
		padding: 0;
		color: white;
		text-shadow: 0 0.1em 20px rgba(0, 0, 0, 1), 0.05em -0.03em 0 rgba(0, 0, 0, 1),
			0.05em 0.005em 0 rgba(0, 0, 0, 1), 0em 0.08em 0 rgba(0, 0, 0, 1),
			0.05em 0.08em 0 rgba(0, 0, 0, 1), 0px -0.03em 0 rgba(0, 0, 0, 1),
			-0.03em -0.03em 0 rgba(0, 0, 0, 1), -0.03em 0.08em 0 rgba(0, 0, 0, 1), -0.03em 0 0 rgba(0, 0, 0, 1);
	}

	.score-wrapper {
		display: flex;
		font-size: medium;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		flex-wrap: wrap;
		padding: 0.64rem;
		gap: 1rem;
		background-color: rgba(255,255,255,0.1);
		border: 0;
		border-radius: 24px;
	}

	.i-btn {
		height: 20px;
		width: 20px;
		padding: 0;
		border: 1px solid white;
		border-radius: 50%;
		background-color: rgba(255,255,255,0.1);
		color: white;
		cursor: pointer;
		z-index: 1;
		transition: background-color 0.5s ease, font-weight 0.5s ease;
	}

	.i-btn:hover {
		background-color: rgba(255,255,255,0.2);
		font-weight: 600;
	}

	.i-btn[disabled] {
		display: none;
	}

	.highlighted {
		animation: pulse 2s infinite;
	}

	.highlighted:hover {
		animation: none;
	}

	@keyframes pulse {
	  0% {
	    box-shadow: 0 0 0 0 rgba(255,255,255, 0.4);
	  }
	  70% {
	    box-shadow: 0 0 0 0.64rem rgba(255,255,255, 0);
	  }
	  100% {
	    box-shadow: 0 0 0 0 rgba(255,255,255, 0);
	  }
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
		color: black;
		border: 1px solid #ddd;
		border-radius: 3px;
		background-color: #eee;
		color: #000;
		font-size: 0.85em;
		transition-property: color, background-color;
		transition-duration: 200ms;
		transition-timing-function: ease-out;
	}

	.quest-form button:hover {
		background-color: #d6d6d6;
	}

	.quest-form button:active {
		background: linear-gradient(-45deg, #aaa, #ccc, #aaa, #fff);
		background-size: 400% 400%; 
		animation: gradient 15s ease infinite;
	}

	.button-container {
    display: flex;
	justify-content: center;
    gap: 10px; 
    }

	.thintext {
	font-weight: 100;
	}

	.titletext {
	font-weight: 100;
	font-size: 2em;
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

	@media only screen and (max-width: 768px) { /* 576 */
		.quest-form {
			grid-template-columns: repeat(1, 1fr);
		}

		.question-wrapper {
			min-height: 8.5rem;
		}

		.hud {
			min-height: 60px;
			flex-direction: column;
		}

		.brand2 {
			margin: 0;
		}
	}
</style>