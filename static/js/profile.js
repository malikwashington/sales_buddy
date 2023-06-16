

(function () {
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
  
  let phone = document.getElementById('profileFormPhone')
  let profilePhone = document.getElementById('profilePhone')
  phone.oninput = () => phone.value = phoneFormat(phone.value)
  profilePhone.innerHTML = phoneFormat(profilePhone.innerHTML)
  phone.value = phoneFormat(phone.value)
  console.log(phone)
}
)()