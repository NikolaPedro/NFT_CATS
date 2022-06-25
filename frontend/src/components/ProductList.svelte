<script>
    import { onMount, onDestroy, debug } from "svelte/internal";
    import { getProductsCount } from "../utils/api";
    import ProductCard from "./ProductCard.svelte";

    let listElement;
    $: products = [];
    let maxCount = 0;

    onMount(async () => {
        getProductsCount()
            .then(response => response.json())
            .then(json => maxCount = json.count);
        
        window.addEventListener("scroll", function () {
            let scrollY = listElement.offsetTop + listElement.clientHeight;
            if (scrollY > window.scrollY && products.length < maxCount) {
                products = [...products, products.length]
            }
        });
    });

    onDestroy(() => {
        window.removeEventListener("scroll");
    });
</script>


<div bind:this={listElement}>
    {#each products as index}
        <ProductCard id={index} />
    {/each}
</div>


<style>
    div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        gap: 30px;
    }
</style>