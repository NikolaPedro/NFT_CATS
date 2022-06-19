<script>
    import { navigate } from "svelte-routing";
    import Button from "../../components/Button.svelte";
    import { account } from "../../stores/stores.js";
    import { API_HOST } from "../../utils/api.js";

    let login = "";
    let password = "";
    let maxlength = 30;

    let error = "";

    let auth = async () => {
        if (error == "") {
            const responce = await fetch(`${API_HOST}/auth`, {
                method: 'POST', 
                headers: { 'Content-Type' : 'application/json' },
                body: JSON.stringify({ login: login, password: password })
            });
            const { answer } = await responce.json();
            if (answer === "loginError") {
                error = "User with this name does not exist!";
            } else if (answer === "passwordError") {
                error = "Wrong password!";
            } else if (answer === "done") {
                $account = login;
                navigate("/");
            }
        }
    };
</script>


<div class="container">
    <form>
        <div class="error">{error}</div>
        <input type="text" placeholder="Login" {maxlength} bind:value={login}>
        <input type="password" placeholder="Password" {maxlength} bind:value={password}>
        <button class="auth-button" on:click={() => navigate("/reg")}>Don't have an account?</button>
        <Button type="accent" size="big" text="Login" action={auth} />
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

    .error {
        margin: 10px;
        color: var(--color-error);
        font-size: 16px;
        font-weight: 500;
    }
</style>