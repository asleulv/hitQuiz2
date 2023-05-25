<script>
	export let tabs = [];
	export let activeTabValue = 1;

	const handleClick = tabValue => () => (activeTabValue = tabValue);
</script>

<ul>
	{#each tabs as tab}
		<li class={activeTabValue === tab.value ? 'active' : ''}>
			<span on:click={handleClick(tab.value)}>{tab.label}</span>
		</li>
	{/each}
</ul>
{#each tabs as tab}
	{#if activeTabValue == tab.value}
		<div class="box">
			<svelte:component this={tab.component}/>
		</div>
	{/if}
{/each}

<style>
	.box {
		margin-bottom: 10px;
		padding: 0 1rem;
		overflow: auto;
	}
	ul {
		display: flex;
		flex-wrap: wrap;
		padding-left: 0;
		margin-bottom: 0;
		margin-top: 0;
		list-style: none;
		border-bottom: 1px solid #dee2e6;
	}
	li {
		margin-bottom: -1px;
	}
	span {
		display: block;
		padding: 0.5rem 1rem;
		cursor: pointer;
	}
	span:hover {
		border-color: #e9ecef #e9ecef #dee2e6;
	}
	li.active > span {
		border-bottom: 3px solid #fff;
	}
</style>