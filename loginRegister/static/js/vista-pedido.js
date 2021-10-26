//Boton de  Menú
let toggle = document.querySelector('.toggle');
let navigation = document.querySelector('.navigation');
let main = document.querySelector('.main');

toggle.onclick = function() {
    navigation.classList.toggle('active');
    main.classList.toggle('active');
}

//Añadir clase hover en el elemento seleccionado en menu
let list = document.querySelectorAll('.navigation li');

function activeLink() {
    list.forEach((item) =>
    item.classList.remove('hovered'));
    this.classList.add('hovered');
}

list.forEach((item) => 
item.addEventListener('mouseover', activeLink));

// Ver los productos del pedido

function verPedido(){
    const home = document.querySelector('.mostrar-compra')
    const compraTotal = document.querySelector('.compra-total');
    const htmlCompra = compraTotal.textContent;
    const htmlConfirm = document.createElement('div');
    const htmlCompraContent = `
    ${htmlCompra}
    `;
    htmlConfirm.innerHTML = htmlCompraContent;
    home.append(htmlConfirm)

    console.log(htmlCompra)
}

verPedido()
