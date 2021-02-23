console.log("Client script started")

const socket = new WebSocket("ws://localhost:8000/ws")

socket.onopen = ( event ) => {
    socket.send("Hello for the client");
};

socket.onmessage = ( event ) => {
    console.log(event.data);
};
