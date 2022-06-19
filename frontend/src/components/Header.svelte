<script>
    import { navigate } from "svelte-routing";
    import SearchLine from "./SearchLine.svelte";
    import Button from "./Button.svelte";
    import { account } from "../stores/stores.js";

    let uploadAction = () => {
        if ($account != "") {
            navigate("/upload");
        } 
    };
    let accountAction = () => {
        if ($account != "") {
            navigate("/account");
        } else {
            navigate("/auth");
        }
    };
</script>


<header>
    <div class="container">
        <button class="logo" on:click={() => navigate("/")}>NFT cats</button>
        <div class="right">
            <SearchLine/>
            <Button type="accent" size="medium" text="Upload" disabled={$account == ""} action={uploadAction} />
            <Button type="light" size="medium" text="Account" action={accountAction} />
        </div>
    </div>
</header>


<style> 
    header {
        border-bottom: 1px solid var(--color-neutral-2);
    }

    .container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        max-width: 1280px;
        margin: 0 auto;
        padding: 14px 0px;
    }
    
    .right {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
    }
    
    .logo {
        justify-self: flex-start;
        font-size: 28px;
        font-weight: 700;
        color: var(--color-neutral-6);
    }
</style>