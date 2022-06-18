export default function validate(form) {
    if (form.login.length < 5) {
        return "Login cannot be less than 5 characters!";
    }

    const reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (!reg.test(form.email)) {
        return "Email is incorrect!";
    }

    if (form.password.length < 6) {
        return "Password cannot be less than 6 characters!";
    }
    
    if (form.password !== form.repeatPassword) {
        return "Passwords do not match!";
    }
    
    return "";
}