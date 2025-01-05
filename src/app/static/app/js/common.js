document.showNotification = function(message){
    const notificationDom = document.querySelector('.notification')
    notificationDom.innerText = message
    notificationDom.style.display = 'block'
    notificationDom.style.opacity = 1
    setTimeout(()=>{notificationDom.style.opacity = 0}, 2500)
    setTimeout(()=>{notificationDom.style.display = 'none'}, 2750)
}

// Phonenumber fix
const phoneNumberField = document.querySelector('#id_phone_number')
const submitButton = document.querySelector('button[type="submit"]')

submitButton.addEventListener('click', ()=>{
    if (phoneNumberField.value.startsWith('8')){
        phoneNumberField.value = `+7${phoneNumberField.value.slice(1)}`
    } 
})