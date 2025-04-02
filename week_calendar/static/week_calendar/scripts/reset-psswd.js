const resetPsswdForm = document.querySelector('.reset-psswd-form')
resetPsswdForm.addEventListener('submit', async (event) => {
    event.preventDefault()
    const token = new URLSearchParams(window.location.search).get("token")
    if (!token) {
        alert("Token inválido o expirado.")
        return
    }
    const formData = new FormData(resetPsswdForm)
    formData.append('token', token)
    console.log(formData)
    try {
        let response = await fetch(resetPsswdForm.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        })

        if (response.redirected) {
            window.location.href = response.url
        } else {
            let html = await response.text()
            document.documentElement.innerHTML = html
        }

    } catch (error) {
        console.error("Error:", error)
    }
})