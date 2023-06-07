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
      const l = document.getElementsByClassName("modal-title")[1].innerHTML = `${data.f_name} ${data.l_name}`
      console.log(l)
      document.getElementsByClassName("modal-body")[1].innerHTML = `
      <form id="modal-form">
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="phone">Phone Number</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="phone" name="phone" value="${data.phone ? data.phone : ''}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="email">Email</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="email" name="email" value="${data.email ? data.email : ''}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="company">Company</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="company" name="company" value="${data.company ? data.company : ''}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="linkedin">Linkedin</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="linkedin" name="linkedin" value="${data.linkedin ? data.linkedin : ''}">
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <div class="row">
            <div class="col-4 mt-2">
              <label for="notes">Notes</label>
            </div>
            <div class="col-8">
              <input type="text" class="form-control" disabled=true id="notes" name="notes" value="${data.notes ? data.notes : ''}">
            </div>
          </div>
        </div>

      </form>
      `
      const footer = document.getElementsByClassName("modal-footer")[1]
      
      footer.innerHTML = `
      <button type="button" class="btn btn-primary" onclick=editContact(${data.contact_id})>Edit</button>
      <button type="button" class="btn btn-danger" onclick=deleteContact(${data.contact_id})>Delete</button>
      `
    });
}

function editContact(id) {
  const contactModal = document.getElementById("login");
  document.getElementById("contactModal").ariaModal("false");
  const fields = document.getElementsByClassName("form-control");
  contactForm = document.getElementById("modal-form");
  contactForm.action = `/contacts/${id}/edit`;
  contactForm.method = "POST";
  // modal.modal("toggle")
  
  // const potential = (divName) => {
  //   newDiv = document.createElement("div").className = "form-group";
  //   newDiv.innerHTML = `
  //   <div class="row mb-2">
  //     <div class="col-4">
  //       <label for="${divName.toLowerCase()}">${divName}</label>
  //     </div>
  //     <div class="col-8">

  //   `
  // const urgency = document.createElement("div").className = "form-group";
  // const potential = document.createElement("div").className = "form-group";
  // const opportunity = document.createElement("div").className = "form-group";

  // contactForm.append(urgency, potential, opportunity);
  for(const field of fields) field.disabled = false ;
  document.getElementsByClassName("modal-footer")[0].innerHTML = `
  <button type="button" class="btn btn-info" onclick=openForm(${id})>Cancel</button>
  <button type="button" class="btn btn-warning" onclick=saveContact(${id})>Save</button>
  `
}

function saveContact() {

}

function deleteContact() {


}