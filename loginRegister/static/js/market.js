
let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active');
    shoppingCart.classList.remove('active');
    navbar.classList.remove('active');
}

let shoppingCart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = () =>{
    shoppingCart.classList.toggle('active');
    searchForm.classList.remove('active');
    navbar.classList.remove('active');
}


let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.toggle('active');
    searchForm.classList.remove('active');
    shoppingCart.classList.remove('active');
}

// Añadir elementos al carrito de compra

const addToCart = document.querySelectorAll('.addToCart');
addToCart.forEach((addToCartButton) => {
    addToCartButton.addEventListener('click', addToCartClicked);
});

const shoppingCartItemContainer = document.querySelector('.shopping-cart-container')

function addToCartClicked(event) {
    const button = event.target;
    const item = button.closest('.box');

    const itemTitle = item.querySelector('.product').textContent;
    const itemPrice = item.querySelector('.price').textContent;
    const itemImg = item.querySelector('.img').src;
    const itemQuantity = item.querySelector('.quantity').value;
    addItemtoShoppingCart(itemTitle, itemPrice, itemImg, itemQuantity) 
}

function addItemtoShoppingCart(itemTitle, itemPrice, itemImg, itemQuantity) {
    
    const elementTittle = shoppingCartItemContainer.getElementsByClassName('shoppingCartItemTitle');
    for (let i = 0; i < elementTittle.length; i++){
        if (elementTittle[i].innerText === itemTitle){
            let elementQuantity = elementTittle[i].parentElement.querySelector('.quantity');
            elementQuantity.value++;
            updateShoppingCartTotal();
            return;
        }
    }

    const shoppingCartRow = document.createElement('div');
    const shoppingCartContent = `
    <div class='box shoppingCartItem'>
        <i class='fas fa-trash'></i>
        <img src=${itemImg} - alt='imagen de producto' />
        <div class='content'>
        <h3 class='shoppingCartItemTitle'>${itemTitle}</h3>
        <span class='item-price'>$ <span class='price'>${itemPrice}</span></>
        <span>Ctd: <input class='quantity' type='text' value=${itemQuantity} /></span>
        </div>
    </div>`;
    shoppingCartRow.innerHTML = shoppingCartContent;
    shoppingCartItemContainer.append(shoppingCartRow);
    shoppingCartRow.querySelector('.fa-trash').addEventListener('click', removeShoppingCartItem)

    shoppingCartRow.querySelector('.quantity').addEventListener('change', quantitChanged)

    updateShoppingCartTotal()
}

function updateShoppingCartTotal(){
    let total = 0;
    const shoppingCartTotal = document.querySelector('.shoppingCartTotal');

    const shoppingCartItems = document.querySelectorAll('.shoppingCartItem');

    shoppingCartItems.forEach((shoppingCartItem) => {
        const shoppingCartItemPriceElement = shoppingCartItem.querySelector('.price');
        const shoppingCartItemPrice = Number(shoppingCartItemPriceElement.textContent);
        const shoppingCartItemQuantityElement = shoppingCartItem.querySelector('.quantity');
        const shoppingCartItemQuantity = Number(shoppingCartItemQuantityElement.value);
        total = total + shoppingCartItemPrice * shoppingCartItemQuantity;
    });

    shoppingCartTotal.innerHTML = `${total}`;
}

function removeShoppingCartItem(event) {
    const buttonClicked = event.target;
    buttonClicked.closest('.shoppingCartItem').remove();
    updateShoppingCartTotal();
}

function quantitChanged(event) {
    const input = event.target;
    input.value <= 0 ? (input.value = 1) : null;
    updateShoppingCartTotal();
}

function pagarButtonClicked() {
    const pay = document.querySelector('.shopping-cart').outerHTML;
    const shoppValue = document.querySelector('.compraTotal');
    const total = document.querySelector('.shoppingCartTotal').textContent;
    const totalPay = document.querySelector('.pagoTotal');
    shoppValue.value = pay;
    totalPay.value = total;
    totalPay.value > 0?
        document.getElementById("compra").submit():
        null 
}

const pagarButton = document.querySelector('.pagar');
pagarButton.addEventListener('click', pagarButtonClicked);

const idSuccess = document.querySelector('#success')

const paypalBtn = document.querySelector('#paypal-btn')
paypalBtn.addEventListener('click', (e)=>{e.preventDefault();idSuccess.submit()})