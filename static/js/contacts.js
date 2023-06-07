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
  console.log(id)
  //helper function to populate data, add onclick to delete and add event listener to edit button
  const populateData = (data) => {
    document.getElementsByClassName("modal-title")[1].innerHTML =
      `${data.f_name} ${data.l_name}`;
    document.getElementsByClassName("modal-body")[1].innerHTML = `
      <form id="modal-form" name='modal-form'>
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="phone">Phone Number</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="phone" name="phone"
              value="${data.phone ? data.phone : ""}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="email">Email</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="email" name="email"
              value="${data.email ? data.email : ""}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="company">Company</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="company" name="company"
              value="${data.company ? data.company : ""}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="linkedin">Linkedin</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="linkedin" name="linkedin"
              value="${data.linkedin ? data.linkedin : ""}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="last_contacted">Last Contacted</label>
            </div>
            <div class="col-8">
              <p class="mt-2">${data.last_contacted ? data.last_contacted : ""}</p>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="notes">Notes</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" id="notes" name="notes"
              value="${data.notes ? data.notes : ""}">
            </div>
          </div>
        </div>

      </form>`;
    
    const form = document.getElementById("modal-form");
    const footer = document.getElementsByClassName("modal-footer")[1];
    footer.innerHTML = `
      <div class="row">
      
        <div class="col-4">
        <button type="button" class="btn btn-danger" onclick=deleteContact(${data.contact_id})>Delete</button>
        </div>
       
        <div id='center' class="col-4">
        <button type="button" class="btn btn-primary" data-bs-toggle='modal' data-bs-target='#login'
         data-bs-dismiss='modal' id='edit'> Edit </button>
        </div>

        <div id='right' class="col-4">
        <button type="button" class="btn btn-success" onclick=saveContact(${data.contact_id})>Save</button>
        </div>

      </div>
      `;
   
      document.getElementById('center').style.textAlign = 'center'
      document.getElementById('right').style.textAlign = 'right'
    footer.style.display = "block";
    document.getElementById("edit").addEventListener("click", () => {
      editContact(data);
      });
  }

//uses the + operator to convert id variable to a number, if it is not a number, it is full contact data
  if (isNaN(+id)) {
    return populateData(id)
  }

  //otherwise we make an api call to get contact data
  fetch(`/contacts/${id}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        return populateData(data);
    });
}
function editContact(data, count=0) {
  document.getElementsByClassName("modal-title")[0].innerHTML = 'Edit Contact'
  const form = document.getElementById('login-form')
  for (const line of form) {
    if (line.type != 'hidden' && line.id in data) line.value = data[line.id]
  }

  document.getElementsByClassName("modal-footer")[0].innerHTML = `
  <button type="button" data-bs-toggle='modal' data-bs-target='#contactModal' 
      data.bs-dismiss='modal' class="btn btn-info" id='cancel'>Cancel</button>
  <button type="button" id='save' class="btn btn-warning" >Save</button>
  `;

  document.getElementById("save").addEventListener("click", () => { saveContact(data.contact_id, 'login-form');});
  document.getElementById("cancel").addEventListener("click", () => { openForm(data); });
}

function saveContact(id, past='modal-form') {
  console.log("save contact")
  const form = document.getElementById(past)
  console.log(form)
  form.action = `/contacts/${id}/edit`
  form.method = 'POST'
  console.log(form)
  form.submit()
  form.reset()
}

function deleteContact() {
  console.log("delete contact")

}