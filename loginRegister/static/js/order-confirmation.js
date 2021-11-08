
function confirmarCompra(){
    const home = document.querySelector('.confirmacion')
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
confirmarCompra()
