const login_btn = document.querySelector(".iniciar-sesion-btn");
const register_btn = document.querySelector(".registro-btn");
const container = document.querySelector(".container");

register_btn.addEventListener("click", () => {
    container.classList.remove("inicio-mode");
    container.classList.add("register-mode");
});

login_btn.addEventListener("click", () => {
    container.classList.remove("register-mode");
    container.classList.add("inicio-mode");
});