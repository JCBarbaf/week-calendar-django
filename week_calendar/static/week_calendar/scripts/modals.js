import { SetDates } from "./week-handler.js"
import { DeleteEvent } from "./event-handler.js"
import { DeleteSubject } from "./subject-handler.js"
import { CreateSubjectsList } from "./subject-handler.js"

const modals = document.querySelectorAll('.modal-background')
const eventsModal = document.querySelector('.modal-background.events')
const form = document.querySelector('.event-form')

document.querySelector('.calendar').addEventListener('click', (event) => {
  if (event.target.closest('.add-button')) {
    document.querySelector('[name="eventDate"]').value = event.target.closest('.add-button').dataset.date
    eventsModal.classList.add('active')
  }
})

modals.forEach(modal => {
  modal.addEventListener('click', async (event) => {
    if (event.target.closest('.close-button') || event.target.closest('.cancel-delete') || !event.target.closest('.modal')) {
        if (event.target.closest('.modal-background').classList.contains('subjects')) {
            window.location.reload()
        }
        document.querySelector('[name="id"]').value = null
        form.reset()
        modal.classList.remove('active')
    } else if (event.target.closest('.confirm-delete')) {
        if (event.target.closest('.delete-event')) {
            await DeleteEvent()
            SetDates(document.querySelector('.date-input').value)
        } else if (event.target.closest('.delete-subject')) {
            await DeleteSubject()
            CreateSubjectsList(false)
            SetDates(document.querySelector('.date-input').value)
        }
        event.target.closest('.modal-background').classList.remove('active')
    }
  })
})