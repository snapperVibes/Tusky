ws = new WebSocket("ws://localhost:8000/ws");
const roomApi = "http://localhost:8000/api/v1/room/"
// ws.onmessage = function (event) {
//     var notice = document.getElementById("notice").innerHTML = event.data
// };
function joinRoom(event) {
    var roomcode = document.getElementById("roomCode").value.toUpperCase()
    fetch(roomApi + "details/" + roomcode).then(
        (resp) => resp.json()
    ).then(
        function (obj) {
            if (obj.active) {
                window.open("http://localhost:8000/room/" + roomcode, name="_top")
            }
            else {
                ws.send("Room " + roomcode + " does not exist.")
            }
        }
    )
    event.preventDefault()
}
function createRoom(event) {
    var roomcode = document.getElementById("createRoom").value.toUpperCase()
    fetch(roomApi + "create/").then(
        (resp) => resp.json()
    ).then(
        (obj) => window.open(obj.room_url)
    )
    event.preventDefault()
}

    // var username = document.getElementById("username").value
    // // var resp = window.open("http://localhost:8000/room/ABCDE", name="_top")
    //
    // ws.send(roomcode + ":" + username)
    // event.preventDefault()




// function connect(event) {
//     var room = document.getElementById("roomCode")
//     var name = document.getElementById("username")
//     ws = new WebSocket("ws://localhost:8000/ws");
//     ws.onmessage = function (event) {
//         var messages = document.getElementById("messages")
//         var message = document.createElement("li")
//         var content = document.createTextNode(room)
//         message.appendChild(content)
//         messages.appendChild(message)
//         console.log(content)
//     };
//     event.preventDefault();
// }
// function sendMessage(event) {
//     var code = document.getElementById("messageText")
//     ws.send(input.value)
//     input.value = ""
//     event.preventDefault()
// }

