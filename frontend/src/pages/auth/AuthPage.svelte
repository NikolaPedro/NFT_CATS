<script>
    import { navigate } from "svelte-routing";
    import Button from "../../components/Button.svelte";

    let login = "";
    let password = "";
    let maxlength = 30;
</script>


<div class="container">
    <form>
        <input type="text" placeholder="Login" {maxlength} bind:value={login}>
        <input type="password" placeholder="Password" {maxlength} bind:value={password}>
        <button class="auth-button" on:click={() => navigate("/reg")}>Don't have an account?</button>
        <Button type="accent" size="big" text="Login" action={() => navigate("/")} />
    </form>
</div>


<style>
    .container {
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-bottom: 100px;
    }

    input {
        width: 300px;
        font-size: 14px;
        padding: 12px 18px;
        border-radius: 8px;
        border: 2px solid var(--color-neutral-2);
        margin: 6px;
    }

    input:focus {
        border: 2px solid var(--color-primary);
    }

    .auth-button {
        font-size: 14px;
        margin: 14px;
        color: var(--color-neutral-3);
        text-decoration: underline;
    }
    
    .auth-button:hover {
        color: var(--color-primary);
    }
</style>