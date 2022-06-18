<script>
    import { Router, Route } from "svelte-routing";
    import StorePage from "./pages/store/StorePage.svelte";
    import RegPage from "./pages/reg/RegPage.svelte";
    import AuthPage from "./pages/auth/AuthPage.svelte";
    import Header from "./components/Header.svelte";
    import Footer from "./components/Footer.svelte";
</script>


<Router>
    <Header/>
    <main>
        <Route path="/">
            <StorePage/>
        </Route>
        <Route path="/regestration">
            <RegPage/>
        </Route>
        <Route path="/authorization">
            <AuthPage/>
        </Route>
        <Route path="/profile">
            <StorePage/>
        </Route>
    </main>
    <Footer/>
</Router>


<style>
    main {
        max-width: 1280px;
        margin: 0px auto;
    }
</style>