<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	
	export let success = false;

	let promise = fetch('/scores/').then(x => x.json());
	let scores = [];
	let name = '';

	const handleSubmit = () => {
		promise = fetch('/scores/', {
			method: 'POST', 
			headers: { 'Content-Type': 'application/json' }, 
			body: JSON.stringify({ name: name })
		}).then(x => x.json());
		promise.then(data => {
			success = false;
			dispatch('updated');
		});
	};

	const isCurrentItem = (data, id) => {
		return data.meta 
			&& data.meta.current_id 
			&& data.meta.current_id === id
	};
</script>

<div class="wrapper">
	{#if success}
		<form on:submit|preventDefault={handleSubmit}>
			<div class="input-group">
				<input 
					type="text" 
					bind:value={name} 
					placeholder="user123" 
					minlength="3" 
					maxlength="8" 
					pattern="[A-Za-z]+[A-Za-z\-\_]*[0-9]*"
				/>
				<button type="submit">Send</button>
			</div>
		</form>
	{/if}
	<div class="highscores">
		{#await promise}
			<p>Loading scores.</p>
		{:then data}
			<table>
				{#each data.data as user, i}
					<tr class:current={isCurrentItem(data, user.id)}>
						<td>{user.rank}</td>
						<td>{user.name}</td>
						<td>{user.points}</td>
					</tr>
				{/each}
			</table>
		{/await}
	</div>
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		max-width: 320px;
		min-width: 200px;
		margin: .64rem auto;
		margin-bottom: 1.2rem;
	}

	.highscores {
		display: inline-block;
		overflow: auto;
/*		height: 128px;*/
		height: 212px;
		margin: 0.64rem 0;
	}

	input {
		padding: .5rem .25rem;
		border: 1px solid #ddd;
		border-radius: 3px;
		background-color: #eee;
		font-size: 0.85em;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.84em;
	}
	table, th, td {
 		border: 1px solid;
	}

	.current {
		font-weight: 700;
		background-color: rgba(255,255,255,0.2);
	}

	.input-group {
		margin: .25rem 0;
		display: flex;
		align-items: stretch;
		flex-wrap: wrap;

		width: 100%;
	}

	.input-group > * {
		padding: .5rem;
		border: 1px solid #ccc;
	}

	.input-group *:first-child {
/*		flex: .25 1 0;*/
		text-align: center;
		border-bottom-left-radius: 3px;
		border-top-left-radius: 3px;
	}

	.input-group *:last-child {
		flex: .125 1 0;
		border-radius: 0;
		border-bottom-right-radius: 3px;
		border-top-right-radius: 3px;
	}

	.input-group > input {
		flex: 1 0 auto;
		flex-grow: 1;
		border-radius: 0px;
		border-left: none;
		border-right: none;
		outline:none;
	}
	.input-group > input:focus {
		outline: 2px solid #8df;
		outline-offset: 0px;
		z-index: 1;
	}

	button:focus {
		outline: none;
	}

	button:hover {
		background-color: #dedede;
	}

	button[type="submit"] {
		width: 100%;
	}

	@media only screen and (max-width: 480px) { /* 576*/
		.highscores {
			height: 151px;
		}
	}
</style>