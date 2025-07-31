document.showNotification = function(message){
    const notificationDom = document.querySelector('.notification')
    notificationDom.innerText = message
    notificationDom.style.display = 'block'
    notificationDom.style.opacity = 1
    document.hideNotification(2500)
}

document.hideNotification = function(timeout){
    const notificationDom = document.querySelector('.notification')
    setTimeout(()=>{notificationDom.style.opacity = 0}, timeout)
    setTimeout(()=>{notificationDom.style.display = 'none'}, timeout + 250)
}

document.hideNotification(6000)

// Phonenumber fix
const phoneNumberField = document.querySelector('#id_phone_number')
const submitButton = document.querySelector('button[type="submit"]')

submitButton.addEventListener('click', ()=>{
    if (phoneNumberField.value.startsWith('8')){
        phoneNumberField.value = `+7${phoneNumberField.value.slice(1)}`
    } 
})

// Double submit fix
document.querySelectorAll('form').forEach((form) => {
	form.addEventListener('submit', (e) => {
		if (form.classList.contains('is-submitting')) {
			e.preventDefault();
			e.stopPropagation();
			return false;	
		};

		form.classList.add('is-submitting');
	});
});