<template>
    <div id="visualizer">
        <h1 class="title">AWE Visualizer</h1>

        <form id="url-form" @submit.prevent="">
            <input v-model="targetUrl" type="url" name="url" id="target-url-input" placeholder="Paste URL here">
            <div class="form-buttons">
                <button @click="crawlURL" class="vis-button crawlButton">Crawl Site</button>
                <button @click="analyzeURL" class="vis-button analyzeButton">Analyze Site</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'home',
  data() {
    return {
      targetUrl: '',
      result: '',
    }
  },
  methods: {
    crawlURL() {
        console.log('crawl')
      if (this.targetUrl === '')
          return

      const endpoint = 'http://localhost:5000/api/crawl'

      axios.get(`${endpoint}?url=${this.targetUrl}`)
      .then(resp => {
        this.result = resp.data
      })
      .catch(err => {
        console.log(err)
      })
    },
    analyzeURL() {
        console.log('analyze')
      if (this.targetUrl === '')
          return

      const endpoint = 'http://localhost:5000/api/analyze'

      axios.get(`${endpoint}?url=${this.targetUrl}`)
      .then(resp => {
        this.result = resp.data
      })
      .catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style scoped>
#visualizer {
    display: flex;
    flex-direction: column;
    margin-top: 64px;
}

#url-form {
    display: flex;
    flex-direction: column;
}

.title {
    align-self: center;
    margin-bottom: 32px;
}

#target-url-input {
    display: block;
    width: 80%;
    align-self: center;
    height: 32px;
    padding: 8px;
    border: 1px solid lightgray;
    border-radius: 2px;
}

.form-buttons {
    align-self: center;
}
.vis-button {
    width: 128px;
    height: 40px;
    font-size: 16px;
    margin: 0 16px;
    margin-top: 32px;
    border-radius: 2px;
    border: none;
    outline: none;
}

.vis-button:active {
    background-color: gray;
}

.crawlButton {
    background-color: #F45D01;
    color: white;
}

.analyzeButton {
    background-color: #4384F8;
    color: white;
}
</style>