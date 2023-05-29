<script>
	import { onMount } from 'svelte';
	import { writable, get } from 'svelte/store';

	const store = writable([]); 

	onMount(async () => {
		const resp = await fetch('/scores/stats');
		const data = await resp.json();
		store.set(data);
	});
</script>

<div class="scroller">
	<table>
		{#each $store as level, i}
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
		border: 1px solid  #ffffff57;
	}
	.type-1 {
		background-color: lime;
	}
	.type-2 {
		background-color: red;
	}
	.type-3 {
		background-color: gray;
	}
</style>