const calendar = document.querySelector('.calendar')
const eventsModal = document.querySelector('.modal-background.events')

calendar.addEventListener('click', async (event) => {
  if (event.target.closest('.edit-button')) {
    EditEvent(parseInt(event.target.closest('.day-content').dataset.eventId))
  } else if (event.target.closest('.delete-button')) {
    document.querySelector('.confirm-delete').dataset.eventId = event.target.closest('.delete-button').dataset.eventId
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
  console.log(eventData)
  for (const [key, value] of Object.entries(eventData)) {
    document.querySelector(`[name="${key}"]`).value = value
  }
  eventsModal.classList.add('active')
}


// const eventForm = document.querySelector('.event-form')
// eventForm.addEventListener('submit', async (event) => {
//   event.preventDefault()
//   const eventData = new FormData(eventForm)
//   let data = {}
//   for (const [key, value] of eventData.entries()) {
//     data[key] = value
//   }
//   let db = await openDatabase('EventDB')
//   data.id = parseInt(data.id)
//   if (data.id && data.id != '') {
//     await editData(db, data.id, data)
//   } else {
//     delete data.id
//     await writeData(db, data)
//   }
//   SetDates(document.querySelector('.date-input').value)
//   document.querySelector('.modal-background.events').classList.remove('active')
//   document.querySelector('[name="id"]').value = null
//   eventForm.reset()
// })

// function openDatabase(dbName, version = 1) {
//   return new Promise((resolve, reject) => {
//     let request = indexedDB.open(dbName, version)

//     request.onerror = (event) => {
//         console.error("Error opening IndexedDB", event)
//         reject(event)
//     }

//     request.onsuccess = (event) => {
//         // console.log("Database opened successfully")
//         resolve(event.target.result)
//     }

//     request.onupgradeneeded = (event) => {
//       // console.log("Database upgrade needed")
//       let db = event.target.result
      
//       if (!db.objectStoreNames.contains('storeName')) {
//           let store = db.createObjectStore('storeName', { keyPath: 'id', autoIncrement: true })
//           store.createIndex('eventDateIndex', 'eventDate', { unique: false })
//       } else {
//           let store = event.target.transaction.objectStore('storeName')
//           if (!store.indexNames.contains('eventDateIndex')) {
//               store.createIndex('eventDateIndex', 'eventDate', { unique: false })
//           }
//       }
//     }
//   })
// }

// function writeData(db, data) {
//   return new Promise((resolve, reject) => {
//       let transaction = db.transaction(['storeName'], 'readwrite')
//       let store = transaction.objectStore('storeName')
//       let request = store.add(data)

//       request.onsuccess = (event) => {
//           // console.log("Data written successfully", event)
//           resolve(event.target.result)
//       }

//       request.onerror = (event) => {
//           console.error("Error writing data", event)
//           reject(event)
//       }
//   })
// }

// function editData(db, id, updatedData) {
//   return new Promise((resolve, reject) => {
//       let transaction = db.transaction(['storeName'], 'readwrite')
//       let store = transaction.objectStore('storeName')
//       let request = store.get(id)

//       request.onsuccess = (event) => {
//           let data = event.target.result
//           if (data) {
//               Object.assign(data, updatedData)
//               let updateRequest = store.put(data)
//               updateRequest.onsuccess = () => {
//                   resolve(data)
//               }
//               updateRequest.onerror = (event) => {
//                   console.error("Error updating data", event)
//                   reject(event)
//               }
//           } else {
//               reject("No entry found with id: " + id)
//           }
//       }

//       request.onerror = (event) => {
//           console.error("Error fetching data", event)
//           reject(event)
//       }
//   })
// }

// function getWeekData(db, startDate, endDate) {
//   return new Promise((resolve, reject) => {
//       let transaction = db.transaction(['storeName'], 'readonly')
//       let store = transaction.objectStore('storeName')
//       let index = store.index('eventDateIndex')

//       let range = IDBKeyRange.bound(startDate, endDate, false, false)

//       let request = index.openCursor(range)
//       let results = []

//       request.onsuccess = (event) => {
//           let cursor = event.target.result
//           if (cursor) {
//               results.push(cursor.value)
//               cursor.continue()
//           } else {
//               resolve(results)
//           }
//       }

//       request.onerror = (event) => {
//           console.error("Error fetching events", event)
//           reject(event)
//       }
//   })
// }

// function getEvent(db, id) {
//   return new Promise((resolve, reject) => {
//       let transaction = db.transaction(['storeName'], 'readonly')
//       let store = transaction.objectStore('storeName')
//       let request = store.get(id)

//       request.onsuccess = (event) => {
//           if (event.target.result) {
//               resolve(event.target.result)
//           } else {
//               resolve(null)
//           }
//       }

//       request.onerror = (event) => {
//           console.error("Error fetching event by ID", event)
//           reject(event)
//       }
//   })
// }

// function deleteEvent(db, id) {
//   return new Promise((resolve, reject) => {
//     let transaction = db.transaction(['storeName'], 'readwrite')
//     let store = transaction.objectStore('storeName')
//     let request = store.delete(id)

//     request.onsuccess = () => {
//       resolve(true)
//     }

//     request.onerror = (event) => {
//       console.error("Error deleting event", event)
//       reject(event)
//     }
//   })
// }