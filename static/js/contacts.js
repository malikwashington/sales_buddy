function searchTable() {
  let found = false;
  const input = document.getElementById("searchTable");
  let filter = input.value.toUpperCase();
  const table = document.getElementById("myTable2");
  const tr = table.getElementsByTagName("tr");
  for (let i = 1; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName("td");
    for (let j = 0; j < td.length; j++) {
      if (td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
        found = true;
      }
    }
    if (found) {
      tr[i].style.display = "";
      found = false;
    } else {
      tr[i].style.display = "none";
    }
  }
}


function openForm(id) {
  //opens the contact detail modal
  
  
  //helper function to populate data into contact detail modal, 
  //add onclick to delete and add event listener to edit button
  const populateData = (data) => {
    document.getElementById('contactDetailModalTitle').innerHTML =
      `${data.f_name} ${data.l_name}`;
    document.getElementById("contactDetailForm")
      .action = `/contacts/${data.contact_id}/edit/notes`;
      
    document.getElementById("phoneNumber")
      .value=data.phone ? phoneFormat(data.phone) : "";

    document.getElementById("email").value = data.email ? data.email : "";
    document.getElementById("company").value = data.company ? data.company : "";
    const linkedin = document.getElementById("linkedin")

    linkedin.innerHTML = data.linkedin ? "/in/" + data.linkedin : "/in/"
    linkedin.href = data.linkedin ? "https://www.linkedin.com/in/" + data.linkedin : "javascript:void(0)"           
    linkedin.target = data.linkedin ? "_blank" : ""
    linkedin.style = data.linkedin ? "" : "pointer-events: none; cursor: default; text-decoration: none;" 

    document.getElementById("notes").value = data.notes ? data.notes : "";
    document.getElementById("last_contacted")
      .innerHTML = data.last_contacted ? data.last_contacted : ""
      
    const footer = document.getElementById("contactDetailModalFooter");

    footer.innerHTML = `
      <div class="row">
      
        <div class="col-4">
        <button
          type="button"
          class="btn btn-danger buttons"
          data-bs-toggle='modal'
          data-bs-target='#confirmationModal'
          id='detailDelete'>
            Delete
        </button>
        </div>
       
        <div id='center' class="col-4">
        <button 
          type="button" 
          class="btn btn-primary buttons" 
          data-bs-toggle='modal' 
          data-bs-target='#contactEditModal'
          id='edit'>
           Edit 
        </button>
        </div>

        <div id='right' class="col-4">
        <button type="button" class="btn buttons btn-success" id='detailSave'>Save</button>
        </div>

      </div>`;
    document.getElementById('textBtn')
      .addEventListener('click', ()=>textContact(data));
    document.getElementById('emailBtn')
      .addEventListener('click', ()=>emailContact(data));
    document.getElementById('center').style.textAlign = 'center'
    document.getElementById('right').style.textAlign = 'right'
    footer.style.display = "block";
    document.getElementById("edit").addEventListener("click",()=>editContact(data));
    document.getElementById("detailSave").addEventListener("click",()=>saveContact(data.contact_id, 'contactDetailForm'));
    document.getElementById("detailDelete").addEventListener("click",()=>deleteContact(data.contact_id, `${data.f_name} ${data.l_name}`));
  
    const emailContainer = document.getElementById('email-history-container')
    const callContainer = document.getElementById('call-history-container')
    const textContainer = document.getElementById('text-history-container')
    emailContainer.innerHTML = ''
    callContainer.innerHTML = ''
    textContainer.innerHTML = ''
    
    if (data.email_history.length > 0) {
      data.email_history.forEach((email,i) => {
        emailContainer.innerHTML = `
        <div class="row">
          <div class="col-5">
            <p>#${i+1}</p>
          </div>
          <div class="col-7">
            <p>${email.email_time}</p>
          </div> 
        </div>
        <div class="row">
          <div class="col-12">
            <p>To: ${email.to}</p>
            <p>Message:</p>
            <p>${email.email_body}</p>
          </div>
        </div>
        <hr>` + emailContainer.innerHTML
      })
    } else { emailContainer.innerHTML = '<p>No email history</p>' }

    if (data.text_history.length > 0) {
      data.text_history.forEach((text,i) => {
        textContainer.innerHTML = `
        <div class="row">
          <div class="col-5">
            <p>#${i+1}</p>
          </div>
          <div class="col-7">
            <p>${text.text_time}</p>
          </div> 
        </div>
        <div class="row">
          <div class="col-12">
            <p>Message:</p>
            <p>${text.text_body}</p>
          </div>
        </div>
        <hr>` + textContainer.innerHTML
      })
    } else { textContainer.innerHTML = '<p>No text history</p>' }
    

    if (data.call_history.length > 0) {
      data.call_history.forEach((call,i) => {
        callContainer.innerHTML = `
        <div class="row">
          <div class="col-5">
            <p>#${i+1}</p>
          </div>
          <div class="col-7">
            <p>${call.call_time}</p>
          </div> 
        </div>
        <div class="row">
          <div class="col-12">
            <p>To: ${call.to}</p>
          </div>
        </div>
        <hr>` + callContainer.innerHTML
      })
    } else { callContainer.innerHTML = '<p>No call history</p>' }


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

  //select the contact detail tab on click
  document.getElementById("contactDetailsTab").click();
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
  const linkedin = document.getElementById('linkedin')
  linkedin.value = linkedin.value ? linkedin.value.replace('/in/', '') : '';
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
      class="btn btn-secondary buttons" 
      data-bs-toggle="modal" 
      data-bs-target="#contactDetailModal">
    Cancel
  </button>

  <form action="/contacts/${id}/delete" method="POST">
    <button type="submit" class="btn buttons btn-danger">Delete</button>
  </form>`
}

function textContact(data) {
  document.getElementById('text-body').value = ''
  document.getElementById('textContactModalTitle')
    .innerHTML = `<h5 class="m-0 p-0" style="display:inline;">Send A Text To:  </h5><h4 class="m-0 p-0" style="display:inline"> ${data.f_name} ${data.l_name} </h4>`
  document.getElementById('textModalForm').action = `/contacts/${data.contact_id}/text`
}

function emailContact(data) {
  document.getElementById('email-body').value = ''
  document.getElementById('emailContactModalTitle')
    .innerHTML = `<h5 class="m-0 p-0" style="display:inline;">Send An Email To:  </h5><h4 class="m-0 p-0" style="display:inline"> ${data.f_name} ${data.l_name} </h4>`
  document.getElementById('textModalForm').action = `/contacts/${data.contact_id}/email`
}