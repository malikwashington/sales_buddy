const websocket = new WebSocket(
  "wss://https://5698-74-88-202-161.ngrok-free.app/phone"
);
const Device = require('@twilio/voice-sdk').Device
let device = null

fetch('/token')
  .then((response) => {
    return response.json()
  })
  .then((data) => {
    return device = new Device(data.token)
  })
  .then((device) => {
    device.audio.setInputDevice('default')
    device.audio.setOutputDevice('default')
  })

   


document.getElementById('button').addEventListener('click', () => {
  if (!device) {
    return
  }
  else {
    device.connect()
  }
})