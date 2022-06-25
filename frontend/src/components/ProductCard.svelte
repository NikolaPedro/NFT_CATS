<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { getProductData, getImage } from "../utils/api";

    export let id = 0;
    let product = {};

    onMount(async() => {
        getProductData(id)
            .then(response => response.json())
            .then(json => product = json);
    });
</script>


<button on:click={() => navigate(`/store/${product.id}`)}>
        <img src={getImage(product.image)} alt="" />
        <div class="name">{product.name}</div>
        <div class="price">{product.price}</div>
</button>


<style>
    button {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        padding: 16px;
        border-radius: 20px;
        border: 2px solid var(--color-neutral-2);
    }

    img {
        width: 237px;
        height: 237px;
        border-radius: 10px;
    }

    .name {
        width: 237px;
        color: var(--color-neutral-6);
        font-size: 16px;
        font-weight: 700;
        text-align: left;
        margin: 10px 0px;
    }

    .price {
        color: var(--color-success);
        font-size: 12px;
        font-weight: 500;
        border-radius: 4px; 
        padding: 4px 6px;
        border: 2px solid var(--color-success);
    }
</style>