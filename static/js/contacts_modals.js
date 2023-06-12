// function call(id) {
//   let number = document.getElementById("phone").innerHTML;
//   number = "+1" + number.replace(/\D/g, "");

//   fetch("/token")
//     .then((response) => {
//       return response.text();
//     })
//     .then((response) => {
//       const token = response;
//       return token;
//     })
//     .then((token) => {
//       Twilio.Device.setup(token);
//     });
// }

function openForm(id) {
  //helper function to populate data, add onclick to delete and add event listener to edit button
  const populateData = (data) => {
    document.getElementById('contactDetailModalTitle').innerHTML =
      `${data.f_name} ${data.l_name}`;
    document.getElementById("contactDetailModalBody").innerHTML = `
      <form
        action='contacts/${data.contact_id}/edit/notes' 
        method='POST' 
        id="contactDetailForm"
      >
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="phone">Phone Number</label>
            </div>
            <div class="col-5">
            <input type="text" class="form-control" disabled=true id="phone" name="phone"
            value="${data.phone ? phoneFormat(data.phone) : ""}">
            </div>
            <div class="col-3">
            <span>
                  <button 
                    type="button" 
                    class="btn 
                    btn-outline-success" 
                    id="phoneBtn"
                    data-bs-toggle="modal"
                    data-bs-target="#modal-call-in-progress">
                    <i class="fas fa-phone no-pointer-events"></i>
                  </button>
                  <button 
                    type="button" 
                    class="btn btn-outline-info" 
                    id="textBtn"
                    data-bs-toggle="modal"
                    data-bs-target="#modalTextBox">
                    <i class="fas fa-comment no-pointer-events"></i>
                  </button>
                </span>
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
              <a 
                ${
                  data.linkedin
                    ? 'target="_blank"'
                    : "style='pointer-events: none; cursor: default; text-decoration: none;'"
                }
                class="form-control" 
                id="linkedin" 
                href="
                ${
                  data.linkedin
                    ? "https://www.linkedin.com/in/" + data.linkedin
                    : "javascript:void(0)"
                }">
                ${data.linkedin ? "/in/" + data.linkedin : "/in/"}
              </a>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row mb-2">
            <div class="col-4 mt-2">
              <label for="last_contacted">Last Contacted</label>
            </div>
            <div class="col-8">
              <p class="mt-2">${
                data.last_contacted ? data.last_contacted : ""
              }</p>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="notes">Notes</label>
            </div>
            <div class="col-8">
              <textarea
                type="text"
                class="form-control"
                id="notes"
                name="notes"
              >${data.notes ? data.notes : ""}</textarea>
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
          id='detailDelete'>
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
        <button type="button" class="btn btn-success" id='detailSave'>Save</button>
        </div>

      </div>`;
      document.getElementById('phoneBtn')
        .addEventListener('click', () => console.log('phone calls coming'));
      document.getElementById('textBtn')
        .addEventListener('click', ()=>textContact(data));
      document.getElementById('center').style.textAlign = 'center'
      document.getElementById('right').style.textAlign = 'right'
      footer.style.display = "block";
      document.getElementById("edit").addEventListener("click",()=>editContact(data));
      document.getElementById("detailSave").addEventListener("click",()=>saveContact(data.contact_id, 'contactDetailForm'));
      document.getElementById("detailDelete").addEventListener("click",()=>deleteContact(data.contact_id, `${data.f_name} ${data.l_name}`));
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

function phoneFormat(input) {
  //helper function to format phone number
  //returns a string in phone number format (###) ###-####
  
  let str = input.replace(/\D/g, "");
  let len = str.length;

  if (str) str = "(" + str;
  if (len > 3) str = str.substring(0, 4) + ") " + str.substring(4);
  if (len > 6) str = str.substring(0, 9) + "-" + str.substring(9);
  if (len > 10) str = str.substring(0, 14);
  return str;
}

function editContact(data) {
  const form = document.getElementById('contactEditForm')

  for (const line of form) {
    if (line.type != 'hidden' && line.id in data) line.value = data[line.id]
    if (line.id == 'linkedin') line.value = data.linkedin ? data.linkedin : ''
    if (line.id == 'phone') {
      line.placeholder = '(123) 456 - 7890'
      line.value = data.phone ? phoneFormat(data.phone) : ''
    }
  }

  form.action = `/contacts/${data.contact_id}/edit`


  document.getElementById("editSave").addEventListener("click",
    () => { saveContact(data.contact_id, 'contactEditForm'); });
  document.getElementById("cancelEdit").addEventListener("click",()=>openForm(data));
}

function saveContact(id, past) {
  const form = document.getElementById(past)
  form.linkedin.value = form.linkedin.value.replace('/in/', '')
  
  form.submit()
}

function deleteContact(id, fullName) {
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

function textContact(data) {
  console.log('texting', data)
  document.getElementById('textContactModalTitle')
    .innerHTML = `<h5 class="m-0 p-0" style="display:inline;">Send A Text To:  </h5><h4 class="m-0 p-0" style="display:inline"> ${data.f_name} ${data.l_name} </h4>`
  document.getElementById('textModalForm').action = `/contacts/${data.contact_id}/text`
  console.log(data.phone)
}