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
    document.getElementById('contactDetailModalTitle').innerHTML =
      `${data.f_name} ${data.l_name}`;
    document.getElementById('contactDetailModalBody').innerHTML = `
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
              <textarea type="text" class="form-control" id="notes" name="notes"
              value="${data.notes ? data.notes : ""}"></textarea>
            </div>
          </div>
        </div>

      </form>`;

    const footer = document.getElementById("contactDetailModalFooter");

    footer.innerHTML = `
      <div class="row">
      
        <div class="col-4">
        <button
          type="button"
          class="btn btn-danger"
          data-bs-toggle='modal'
          data-bs-target='#confirmationModal'
          onclick=deleteContact(${data.contact_id}, ${data.f_name+' '+data.l_name})>
            Delete
        </button>
        </div>
       
        <div id='center' class="col-4">
        <button 
          type="button" 
          class="btn btn-primary" 
          data-bs-toggle='modal' 
          data-bs-target='#contactEditModal'
          id='edit'>
           Edit 
        </button>
        </div>

        <div id='right' class="col-4">
        <button type="button" class="btn btn-success"
            onclick=saveContact(${data.contact_id})>Save</button>
        </div>

      </div>`;
   
      document.getElementById('center').style.textAlign = 'center'
      document.getElementById('right').style.textAlign = 'right'
      footer.style.display = "block";
      document.getElementById("edit").addEventListener("click",()=>editContact(data));
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


function editContact(data) {
  console.log(data)
  const form = document.getElementById('contactEditForm')
  for (const line of form) {
    if (line.type != 'hidden' && line.id in data) line.value = data[line.id]
  }

  document.getElementById('contactEditModalFooter').innerHTML = `
  <button type="button" data-bs-toggle='modal' data-bs-target='#contactDetailModal' 
      data.bs-dismiss='modal' class="btn btn-info" id='cancel'>Cancel</button>
  <button type="button" id='save' class="btn btn-warning" >Save</button>
  `;

  document.getElementById("save").addEventListener("click",
    () => { saveContact(data.contact_id, 'contactEditForm'); });
  document.getElementById("cancel").addEventListener("click",()=>openForm(data));
}

function saveContact(id, past) {
  console.log("save contact")
  const form = document.getElementById(past)
  console.log(form)
  form.action = `/contacts/${id}/edit`
  form.method = 'POST'
  console.log(form)
  form.submit()
  form.reset()
}

function deleteContact(id, fullName) {
  console.log("delete contact")
  
  document.getElementById('confirmationModalTitle')
    .innerHTML = `Delete Contact: "${fullName}"?`
  document.getElementById('confirmationModalBody').innerHTML = `
    <p>Are you sure you want to delete this contact?</p>
    <p>This action cannot be undone.</p>`
  document.getElementById('confirmationModalFooter').innerHTML = `
    <button 
      type="button" 
      class="btn btn-secondary" 
      data-bs-toggle="modal" 
      data-bs-target="#contactDetailModal">
    Cancel
  </button>

  <form action="/contacts/${id}/delete" method="POST">
    <button type="submit" class="btn btn-danger">Delete</button>
  </form>`
}