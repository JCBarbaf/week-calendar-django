let requestResetform = document.querySelector('.request-reset-form')
let sendedMessage = document.querySelector('.email-sended')
requestResetform.addEventListener('submit', async (event) => {
    event.preventDefault()
    let formData = new FormData(requestResetform)
    console.log(requestResetform)
    try {
        let response = await fetch(requestResetform.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        requestResetform.classList.toggle('active')
        sendedMessage.classList.toggle('active')
    } catch (error) {
        console.error("Error:", error)
    }
})