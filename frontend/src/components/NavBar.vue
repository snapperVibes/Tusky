<template>
  <nav>
    <div id="nav-wrapper">
      <ul>
        <li><div class="stylized-logo">Tusky</div></li>
        <li>
          <div class="welcome" v-show="username">
            Welcome, {{ username }}#{{ number }}
          </div>
        </li>
        <li>
          <div class="elephant-logo">
            <img class="img__elephant" alt="🐘" src="../assets/elephant.jpg" />
          </div>
        </li>
      </ul>
    </div>
  </nav>
  <br />
  <br />
  <br />
</template>

<script>
export default {
  props: {
    username: String,
    number: String,
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li {
  float: left;
  display: block;
  padding: 8px;
}

#nav-wrapper div.stylized-logo {
  font-weight: bold;
}
#nav-wrapper div.welcome {
  /*text-align: right;*/
  float: right;
}
.img__elephant {
  margin-top: -3px;
  margin-left: -10px;
  float: right;
  width: 25px;
  height: auto;
}
</style>
