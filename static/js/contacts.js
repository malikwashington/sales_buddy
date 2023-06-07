function call(id) {
  let number = document.getElementById("phone").innerHTML;
  number = "+1" + number.replace(/\D/g, "");

  fetch("/token")
    .then((response) => {
      return response.text();
    })
    .then((response) => {
      const token = response;
      return token;
    })
    .then((token) => {
      Twilio.Device.setup(token);
    });
}

function openForm(id) {
  fetch(`/contacts/${id}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // console.log(data);
      document.getElementById("sidebar").innerHTML = `
        <div class="card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">${data.f_name} ${data.l_name}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${data.company}</h6>
            <p class="card-text">${data.email}</p>
            <p onclick=call(id) id="phone" class="card-text">${data.phone}</p>
            <a href="#" class="card-link">Edit</a>
            <a href="#" class="card-link">Delete</a>
          </div>
        </div>
        `;
    });
}
