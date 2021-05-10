<template>
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

ol.tusky__answers {
  list-style-type: lower-alpha;
}
.tusky__disabled-explanation {
  color: grey;
}
.tusky__edit-box {
  display: flex;
  flex: 1;
  flex-direction: row;
}
</style>
