<script>
    import { onMount } from "svelte/internal";
    import { productID } from "../stores/stores.js";
    import Button from "../components/Button.svelte";
    import { API_HOST } from "../utils/api.js";
    import { navigate } from "svelte-routing";

    let product = {
        name: "Best Product Name",
        imagePath: "",
        price: 16.9,
        description: `But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. 
        No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful.`,
        authorName: "Nikola Pedro",
        authorImagePath: ""
    };

    onMount(async () => {
        const responce = await fetch(`${API_HOST}/store/${$productID}`);
        product = await responce.json();
    });

    let buy = async () => {
        const responce = await fetch(`${API_HOST}/buy/${$productID}`);
        navigate("/profile");
    };
</script>


<div class="container">
    <section class="block">
        <img src={product.imagePath} alt="" class="image">
        <div class="info">
            <div class="title">{product.name}</div>
            <div class="author">
                <img src={product.authorImagePath} alt="">
                <div class="author-name">{product.authorName}</div>
            </div>
            <p class="description">{product.description}</p>
            <div class="end">
                <div class="price">{product.price + " ETH"}</div>
                <Button type="light" size="big" text="Buy" action={buy} />
            </div>
        </div>
    </section>
</div>


<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .block {
        border: 2px solid var(--color-neutral-2);
        border-radius: 20px;
        display: flex;
        padding: 30px;
        margin: 60px 0px;
    }

    .info {
        display: flex;
        flex-direction: column;
        padding: 0px 10px 0px 30px;
        max-width: 500px;
        min-width: 300px;
    }

    .image {
        height: 400px;
        width: 400px;
    }

    .title {
        color: var(--color-neutral-6);
        font-size: 24px;
        font-weight: 700;
    }

    .author {
        color: var(--color-neutral-6);
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 16px;
    }

    .description {
        color: var(--color-neutral-5);
        font-size: 16px;
        font-weight: 400;
        white-space: pre-line;
    }

    .end {
        margin: auto auto 0px auto;
    }

    .price {
        font-size: 16px;
        font-weight: 700;
        color: var(--color-success);
        border-radius: 4px; 
        padding: 4px 6px;
        border: 3px solid var(--color-success);
        margin-bottom: 10px;
    }
</style>