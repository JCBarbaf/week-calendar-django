document.querySelectorAll('.visibility-psswd-button').forEach(button => {
    button.addEventListener('click', (event) => {
        event.preventDefault()
        button.parentNode.querySelector('.password-input').type = button.classList.contains('show')? 'text' : 'password'
        button.classList.toggle('show')
        button.classList.toggle('hide')
    })
});