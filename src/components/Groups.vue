<template lang='jade'>
  .groups
    router-link(to='/') Home
    div(v-for='group in groups')
      p {{ group[0] }}
</template>

<script>
export default {
  name: 'Groups',
  data () {
    return {
      groups: []
    }
  },
  mounted () {
    console.log('mounted')
    this.$http.get('http://localhost:8080/static/data/parsed-data.json')
      .then(response => {
        return response.json()
      }, response => {
        console.log(response)
      })
      .then(data => {
        this.groups = data.groups
      })
      .catch(err => {
        debugger
        console.log(err)
      })
  }
}
</script>
