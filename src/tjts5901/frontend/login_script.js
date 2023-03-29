

"use strict"

//Clear locaStorage. This is used also to finish logout and remove jwt token from memory.
window.localStorage.clear()

//Initialize page
window.addEventListener("load", async () => {

  let submitform = document.getElementById('logform')
  let submitButton = document.getElementById('logbutton')
  submitButton.addEventListener('click', async (e)=>{
    e.preventDefault()
    document.getElementById('errordiv').textContent = ""

    let form = new FormData(submitform)
    let loginReq = {
      method: 'POST',
      body: form
    }
    console.log("fsjdjfkjdsf")
    const response = await fetch('/login', loginReq);
    const res = await response.json();
    console.log(res)

      if (response.status === 200){
        console.log("seur kirj")

        localStorage.setItem('13jwtstore', res.access_token);
        window.open('/')
      } else if (response.status === 401) {
        document.getElementById('errordiv').textContent = "Wrong username or password."

      }
    
  })

})
