import { SetDates } from "./week-handler.js"

const calendar = document.querySelector('.calendar')
const eventsModal = document.querySelector('.modal-background.events')
const deleteModal = document.querySelector('.modal-background.delete-event')

calendar.addEventListener('click', async (event) => {
  if (event.target.closest('.edit-button')) {
    EditEvent(parseInt(event.target.closest('.day-content').dataset.eventId))
  } else if (event.target.closest('.delete-button')) {
    document.querySelector('.delete-input').value = event.target.closest('.delete-button').dataset.eventId
    deleteModal.classList.add('active')
  }
})

calendar.addEventListener('dblclick', async (event) => {
  if (event.target.closest('.day-content')) {
    EditEvent(parseInt(event.target.closest('.day-content').dataset.eventId))
  } else if (event.target.closest('.day')) {
    document.querySelector('[name="eventDate"]').value = event.target.closest('.day-content-container').dataset.date
  }
  eventsModal.classList.add('active')
})

const eventForm = document.querySelector('.event-form')
eventForm.addEventListener('submit', async (event) => {
  event.preventDefault()
  const eventData = new FormData(eventForm)
  try {
    const response = await fetch('/save-event/', {
      method: 'POST',
      body: eventData,
    })
    if (response.status === 200) {
      SetDates(document.querySelector('.date-input').value)
      document.querySelector('.modal-background.events').classList.remove('active')
      document.querySelector('[name="id"]').value = null
      eventForm.reset()
    } else {
      const errorData = await response.json()
      console.log('Error message:', errorData.error)
    }
  } catch (error) {
    console.error('Network or server error:', error)
  }
})

async function EditEvent(eventID) {
  const response = await fetch(`/event/?id=${eventID}`)
  const data = await response.json()
  const eventData = {
    id: data.event.id,
    eventName: data.event.event_name,
    eventSubject: data.event.subject,
    eventDate: new Date(data.event.event_date).toISOString().split('T')[0],
    eventTime: new Date(data.event.event_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
  for (const [key, value] of Object.entries(eventData)) {
    document.querySelector(`[name="${key}"]`).value = value
  }
  eventsModal.classList.add('active')
}
export async function DeleteEvent() {
  const deleteData = new FormData(document.querySelector('.delete-event .delete-form'))
  try {
    const response = await fetch('/delete-event/', {
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