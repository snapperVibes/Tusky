<template>
  <h1>Learning WebSockets</h1>
  <form @submit.prevent="sendMessage">
    <label for="messageText" />
    <input type="text" id="messageText" autocomplete="off" />
    <button>Send</button>
  </form>
  <ul id="messages" />
</template>

<script>
export default {
  name: "Hello",
  setup(props) {
    const ws = new WebSocket("ws://localhost:8000/session/get_responses");
    ws.onmessage = function (event) {
      const messages = document.getElementById("messages");
      const message = document.createElement("li");
      var content = document.createTextNode(event.data);
      message.appendChild(content);
      messages.appendChild(message);
    };
    return {
      ws: ws,
    };
  },
  methods: {
    sendMessage(submitEvent) {
      var input = submitEvent.target[0];
      this.ws.send(input.value);
      input.value = "";
    },
  },
};
</script>

<style scoped></style>
