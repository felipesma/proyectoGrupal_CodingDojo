const paymentform = document.getElementById('payment-validator')
    paymentform.onsubmit = function(e){
        e.preventDefault()
        email_validator = document.getElementById('paymentEmail').value
        if (email_validator.length == 0){
            const errorMsge = document.getElementById('errorMessages1')
            errorMsge.innerHTML = '<h1>*Email cannot be empty</h1>'
            console.log('error email')
        }
        password_validator = document.getElementById('paymentPassword').value
        if (password_validator.length == 0){
            console.log('error password')
            const errorMsgp = document.getElementById('errorMessages2')
            errorMsgp.innerHTML = '<h1>*Password cannot be empty</h1>'
        }
    }