<template>
  <div class="home">
    <img alt="AWE logo" src="../assets/logo.png">
    <p>{{ message }}</p>
    <button @click="talkToFlask">Get Message</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'home',
  data() {
    return {
      message: '',
    }
  },
  methods: {
    talkToFlask() {
      const url = 'http://localhost:5000/api/example'

      axios.get(url)
      .then(resp => {
        this.message = resp.data.message
      })
      .catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
