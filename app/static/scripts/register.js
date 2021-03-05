const api = "http://localhost:8000/api/v1/"

function register(event) {
    event.preventDefault()
    let username, email, password, confirm_password;
    username = document.getElementById("username").value
    password = document.getElementById("password").value
    email = document.getElementById("email").value
    confirm_password = document.getElementById("confirm_password").value
    if (password !== confirm_password){
        alert("Passwords do not match")
        document.getElementById("password").value = ""
        document.getElementById("confirm_password").value = ""
        return
    }
    fetch(api + "user/create", {
        method: "POST",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "name": username,
            "password": password,
            "email": email
        })
    }).then(
        (resp) => resp.json()
    ).then(
        (obj) => console.log(obj)
    )
}
