<script>
	import { onMount } from 'svelte';
	import { writable, get } from 'svelte/store';

	const stats = writable([]); 
	const songs = writable([]);

	onMount(async () => {
		const resp = await fetch('/scores/stats');
		const data = await resp.json();
		stats.set(data.fail_data);
		songs.set(data.fail_songs);
	});
</script>

<div class="scroller">
	<p class="stats-titles">🚨 Failed songs:</p>
	<ul class="song-list">
		{#each $songs as hit}
			<li>
				<div>
					<span class="artist">{hit.artist}</span>
					<span class="song">{hit.song}</span>
				</div>
			</li>
		{:else}
			<li>No songs available.</li>
		{/each}
	</ul>
	<p class="stats-titles">🎢 Levels:</p>
	<table>
		{#each $stats as level, i}
			<tr>
				<td>Level {i+1}</td>
				{#each level as question}
					<td class="type-{question}"></td>
				{/each}
			</tr>
		{/each}
	</table>
</div>

<style>
	.scroller {
		box-sizing: border-box;
		position: relative;
		height: auto;
		display: block;
		overflow: auto;
		margin: 1.5rem 0;
	}
	table {
		width: 100%;
		border-collapse: collapse;
	}
	table, th, td {
		border: 1px solid #ffffff;
	}
	.type-1 {
		background-color: lime;
	}
	.type-2 {
		background-color: red;
	}
	.type-3 {
		background-color: rgb(255,255,255,.5);
	}
	.song-list {
		margin-top: 0rem;
		text-align: initial;
		padding-left: 0; /* 1.4rem; */
		list-style: None;
		border: 1px solid #fff;
		border-radius: 0px;
	}
	.song-list > li {
		padding: 0.5rem;
		border-bottom: 1px dotted #fff;
	}
	.song-list > li:last-child {
		border-bottom: none;
	}
	.artist, .song {
		display: block;
		font-weight: 300;
	}
	.artist {
		font-weight: 600;
		font-size: medium;
	}
	.stats-titles {
		font-size: large;
		text-align: left;
		text-transform: uppercase;
		background-color: rgba(255, 255, 255, 0.032);
	}
</style>