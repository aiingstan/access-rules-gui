<template lang='jade'>
  u
    li
      router-link(to="/groups") Groups
    li
      router-link(to="/paths") Repositories / Paths
    li
      router-link(to="/help") Help
</template>

<script>
export default {
  name: 'Navigation'
}
</script>

