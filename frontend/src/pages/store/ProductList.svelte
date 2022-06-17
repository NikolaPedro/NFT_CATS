<script>
import { onMount } from "svelte/internal";

    import ProductCard from "./ProductCard.svelte";

    export let pageNumber = 1;

    let products = [];

    onMount(async () => {
        const res = await fetch("http://127.0.0.1:5000/store?page=" + pageNumber);
        products = await res.json();
    });

    // let products = [
    //     { id: 0, productName: "BEER", productImage: "", authorName: "Pedro", price: 75.7},
    //     { id: 1, productName: "VODKA", productImage: "", authorName: "Pedro", price: 34.2},
    //     { id: 2, productName: "GAYBOY", productImage: "", authorName: "Roma", price: 332.99},
    //     { id: 3, productName: "ILIYA", productImage: "", authorName: "Roma", price: 0.02},
    //     { id: 4, productName: "ABODBUHOV", productImage: "", authorName: "Roma", price: 0.13},
    // ];
</script>


<div class="product-list">
    {#each products as { id, name, image_file, creator_id, price }}
        <ProductCard {id} {name} {image_file} {creator_id} {price}/>
    {/each}
</div>


<style>
    .product-list {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        gap: 30px;
    }
</style>