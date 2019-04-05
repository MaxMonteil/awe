<template>
  <div id="app">
    <div id="nav">
      <img alt="AWE logo" src="./assets/logo.png" height="50">
      <span id="nav-links">
        <router-link class="nav-link" to="/">Home</router-link>
        <router-link class="nav-link" to="/visualizer">Visualizer</router-link>
        <router-link class="nav-link" to="/about">About</router-link>
      </span>
    </div>
    <router-view/>
  </div>
</template>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1A1918;
  margin-top: 16px;
  padding: 0 20%;
}

#nav {
  display: flex;
  justify-content: space-between;
}

#nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  margin-left: 32px;
  text-decoration: none;
  font-size: 20px;
  color: #4384F8;
}

.nav-link:hover {
  text-decoration: underline;
}

.nav-link:visited {
  color: gray;
}
</style>
