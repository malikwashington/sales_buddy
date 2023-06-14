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
    console.log('token', data.token, typeof data.token)
    return device = new Device(data.token)
  })
  .then((device) => {
    device.audio.setInputDevice('default')
    device.audio.setOutputDevice('default')
  })

   


document.getElementById('button').addEventListener('click', () => {
  if (!device) {
    console.log('device not initialized')
    return
  }
  else {
    console.log('button clicked')
    device.connect()
  }
})