<template>
    <div>
        <h1>This is the visualizer page</h1>
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
