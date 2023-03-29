
"use strict"


//Initialize page
window.addEventListener("load", async () => {

  let submitform = document.getElementById('regform')
  let submitButton = document.getElementById('regbutton')
  submitButton.addEventListener('click', async (e)=>{
    e.preventDefault()
    document.getElementById('errordiv').textContent = ""

    //Ensure validity in beginning.
    let pwField2 = document.getElementById("confirmPassword")
    pwField2.setCustomValidity("")

    let isValid =  submitform.reportValidity()
    console.log(submitform)
    if (isValid){
      let form = new FormData(submitform)
      let [email, pw, pw2] = form
      if (pw[1]===pw2[1]){
        let msg = {'email': email, 'password': pw}
        let res = await fetch(`/register?email=${email[1]}&password=${pw[1]}`, msg)
        console.log(res.status, "stauscode")
        if (res.status === 201){
          console.log("seur kirj")
          window.open('/login_page')
        } else if (res.status === 401) {
          document.getElementById('errordiv').textContent = "Email probably in use."

        }
          
      
      } else {
        pwField2.setCustomValidity('Passwords do not match.')
        pwField2.reportValidity()
      }
    } 


    

  })

})
