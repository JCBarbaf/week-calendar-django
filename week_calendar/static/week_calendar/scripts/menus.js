let optionsMenu = document.querySelector('.options-menu-background')
document.querySelector('.options-button').addEventListener('click', (event) => {
    event.preventDefault()
    optionsMenu.classList.add('active')
})
optionsMenu.addEventListener('click', async (event) => {
    if (!event.target.closest('.options-menu-container')) {
      optionsMenu.classList.remove('active')
    }
    if (event.target.closest('.subjects-button')) {
        document.querySelector('.modal-background.subjects').classList.add('active')
    }
})