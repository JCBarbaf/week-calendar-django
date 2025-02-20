import { getUserID } from "./user-handler.js"

let subjectsList = document.querySelector('.subjects-list-container')
let deleteSubjectsModal = document.querySelector('.modal-background.delete-subject')

CreateSubjectsList(false)

subjectsList.addEventListener('click', async (event) => {
        let testColorButton
        if (event.target.closest('.add-subject-button')) {
            try {
                const response = await fetch('/create-subject/')
                if (response.status === 200) {
                    console.log('Subject created successfully')
                    CreateSubjectsList(true)
                } else {
                    const errorData = await response.json()
                    console.log('Error message:', errorData.error)
                }
            } catch (error) {
                console.error('Network or server error:', error)
            }
        }
        if ((testColorButton = event.target.closest('.text-color-button'))) {
            event.preventDefault()
            let textColorInput = event.target.closest('.subject-item').querySelector('.subject-text-color-input')
            if (testColorButton.classList.contains('white')) {
                testColorButton.classList.remove('white')
                testColorButton.classList.add('black')
                textColorInput.checked = false
            } else {
                testColorButton.classList.remove('black')
                testColorButton.classList.add('white')
                textColorInput.checked = true
            }
            textColorInput.dispatchEvent(new Event('change', { bubbles: true }))
        }
        if (event.target.closest('.delete-subject-button')) {
            let subjectItem = event.target.closest('.subject-item')
            let subjectID = subjectItem.querySelector('.subject-id-input').value
            let response = await fetch(`/events-number/?subject_id=${subjectID}`)
            let data = await response.json()
            deleteSubjectsModal.querySelector('.delete-input').value = subjectID
            deleteSubjectsModal.querySelector('.subject-name').innerHTML = subjectItem.querySelector('.subject-name-input').value
            deleteSubjectsModal.querySelector('.events-number').innerHTML = data.eventsNumber
            deleteSubjectsModal.classList.add('active')
        }
    }
)

subjectsList.addEventListener('change', async (event) => {
        let csrfToken = document.querySelector('.csrf-token-item input').value
        let inputValue = null
        if (event.target.name == 'subject_white_text') {
            inputValue = event.target.checked.toString()
        } else {
            inputValue = event.target.value
        }
        let subjectData = {
            subject_id: event.target.parentNode.querySelector('.subject-id-input').value,
            column_name: event.target.name,
            new_value: inputValue
        }
        try {
            const response = await fetch('/update-subject/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(subjectData),
            })
            if (response.status === 200) {
                console.log('Subject Updated')
            } else {
                const errorData = await response.json()
                console.log('Error message:', errorData.error)
            }
        } catch (error) {
            console.error('Network or server error:', error)
        }
    }
)

export async function CreateSubjectsList(doScroll) {
    try {
        let userID = await getUserID()
        const response = await fetch(`/subjects/?user_id=${userID}`)
        const subjectsData = await response.json()

        let mainSubjectsList = document.querySelector('.subjects-list')
        mainSubjectsList.innerHTML = ''

        subjectsData.subjects.forEach(subject => {
            let subjectItem = document.createElement('li')
            subjectItem.classList.add('subject-item')

            let subjectInputs = document.createElement('div')
            subjectInputs.classList.add('subject-inputs')

            let subjectIDInput = document.createElement('input')
            subjectIDInput.classList.add('subject-id-input')
            subjectIDInput.type = 'hidden'
            subjectIDInput.name = 'subject_id'
            subjectIDInput.value = subject.id

            let subjectNameInput = document.createElement('input')
            subjectNameInput.classList.add('subject-name-input')
            subjectNameInput.type = 'text'
            subjectNameInput.name = 'subject_name'
            subjectNameInput.value = subject.subject_name

            let subjectCodeInput = document.createElement('input')
            subjectCodeInput.classList.add('subject-code-input')
            subjectCodeInput.type = 'text'
            subjectCodeInput.name = 'subject_code'
            subjectCodeInput.value = subject.subject_code
            subjectCodeInput.maxLength = 4

            let subjectColorInput = document.createElement('input')
            subjectColorInput.classList.add('subject-color-input')
            subjectColorInput.type = 'color'
            subjectColorInput.name = 'subject_color'
            subjectColorInput.value = subject.subject_color

            let subjectTextColorInput = document.createElement('input')
            subjectTextColorInput.classList.add('subject-text-color-input')
            subjectTextColorInput.type = 'checkbox'
            subjectTextColorInput.name = 'subject_white_text'
            subjectTextColorInput.value = subject.subject_white_text

            let inputSeparator1 = document.createElement('p')
            inputSeparator1.classList.add('input-separator')
            inputSeparator1.innerHTML = '|'
            let inputSeparator2 = document.createElement('p')
            inputSeparator2.classList.add('input-separator')
            inputSeparator2.innerHTML = '|'
            let inputSeparator3 = document.createElement('p')
            inputSeparator3.classList.add('input-separator')
            inputSeparator3.innerHTML = '|'

            let textColorButton = document.createElement('button')
            textColorButton.classList.add('text-color-button')
            textColorButton.classList.add(subject.subject_white_text ? 'white' : 'black')
            textColorButton.innerHTML = 'Txt'

            let deleteSubjectButton = document.createElement('button')
            deleteSubjectButton.classList.add('delete-subject-button')
            deleteSubjectButton.innerHTML ='<svg class="delete-subject-icon" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M74.9753 139.327C74.152 132.315 79.6198 126.154 86.6661 126.154H413.334C420.38 126.154 425.848 132.315 425.025 139.327L386.248 469.583C385.551 475.523 380.527 480 374.557 480H125.443C119.473 480 114.449 475.523 113.752 469.583L74.9753 139.327Z" fill="black"/><path d="M198.418 20C193.959 20 189.883 22.5241 187.889 26.5201L179.371 43.5897H55.7714C49.2702 43.5897 44 48.8705 44 55.3846V102.564H456V55.3846C456 48.8705 450.73 43.5897 444.229 43.5897H320.629L312.111 26.52C310.117 22.5241 306.041 20 301.582 20H198.418Z" fill="black"/></svg>'

            subjectInputs.appendChild(subjectIDInput)
            subjectInputs.appendChild(subjectNameInput)
            subjectInputs.appendChild(inputSeparator1)
            subjectInputs.appendChild(subjectCodeInput)
            subjectInputs.appendChild(inputSeparator2)
            subjectInputs.appendChild(subjectColorInput)
            subjectInputs.appendChild(inputSeparator3)
            subjectInputs.appendChild(subjectTextColorInput)
            subjectInputs.appendChild(textColorButton)
            subjectItem.appendChild(subjectInputs)
            subjectItem.appendChild(deleteSubjectButton)
            mainSubjectsList.appendChild(subjectItem)
        })
        if (doScroll) {
            mainSubjectsList.scrollTo({ top: mainSubjectsList.scrollHeight, behavior: "smooth" });
        }
    } catch (error) {
        console.error('Network or server error:', error)
    }
}

export async function DeleteSubject() {
    const deleteData = new FormData(document.querySelector('.delete-subject .delete-form'))
    try {
      const response = await fetch('/delete-subject/', {
        method: 'POST',
        body: deleteData,
      })
      if (response.status != 200) {
        const errorData = await response.json()
        console.log('Error message:', errorData.error)
      }
    } catch (error) {
      console.error('Network or server error:', error)
    }
  }