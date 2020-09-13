<template>
  <div class="home-container">
    <div class="page-item">
      <router-link to="/upload">Upload photos</router-link>
    </div>
    <div class="page-item">
      <router-link to="/upload">View exported links</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style lang="scss" scoped>
.home-container {
  display: flex;
  flex-flow: column;
  align-items: center;
  justify-content: center;
  // background-color: yellow;
  padding: 50px 100px;
}
.page-item {
  width: 300px;
  height: 100px;
  line-height: 100px;
  margin: 30px 0px;
  text-align: center;
  // background-color: green;
  border: 2px solid #002a5a;
  border-radius: 10px;
  &:hover {
    cursor: pointer;
  }
}
</style>
