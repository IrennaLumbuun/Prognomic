<template>
  <div class="app-wrapper">
    <!-- <div v-if="device==='mobile'&&sidebar.opened" class="drawer-bg" @click="handleClickOutside" /> -->
    <!-- <sidebar class="sidebar-container" /> -->
    <div class="main-container">
      <!-- <div :class="{'fixed-header':fixedHeader}">
        <navbar />
      </div> -->
      <div class="navbar">
        <img src="../img/logo.jpeg" class="logo">
        <p style="float: right; margin-right: 20px"> {{ username }} | <a @click="logout" style="color: blue">Log out</a></p>
      </div>
      <app-main />
      <div class="footer">
        <div class="footer-item">Site map</div>
        <div class="footer-item">Terms</div>
        <div class="footer-item">Privacy</div>
        <div class="footer-item">Contact us</div>
        <div class="footer-item">About us</div>
      </div>
    </div>
  </div>
</template>

<script>
// import { Navbar, Sidebar, AppMain } from './components'
import { AppMain } from './components'
import ResizeMixin from './mixin/ResizeHandler'
// import { mapGetters } from 'vuex'

export default {
  name: 'Layout',
  components: {
    // Sidebar,
    AppMain
  },
  mixins: [ResizeMixin],
  computed: {
    // sidebar() {
    //   return this.$store.state.app.sidebar
    // },
    // device() {
    //   return this.$store.state.app.device
    // },
    // fixedHeader() {
    //   return this.$store.state.settings.fixedHeader
    // },
    // classObj() {
    //   return {
    //     hideSidebar: !this.sidebar.opened,
    //     openSidebar: this.sidebar.opened,
    //     withoutAnimation: this.sidebar.withoutAnimation,
    //     mobile: this.device === 'mobile'
    //   }
    // },
    // ...mapGetters([
    //   'name'
    // ]),
    username() {
      console.log(this.$store.state.user.name)
      return this.$store.state.user.name
    }
  },
  methods: {
    // handleClickOutside() {
    //   this.$store.dispatch('app/closeSideBar', { withoutAnimation: false })
    // },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "~@/styles/mixin.scss";
  @import "~@/styles/variables.scss";

  .app-wrapper {
    @include clearfix;
    position: relative;
    height: 100%;
    width: 100%;
    &.mobile.openSidebar{
      position: fixed;
      top: 0;
    }
  }
  .drawer-bg {
    background: #000;
    opacity: 0.3;
    width: 100%;
    top: 0;
    height: 100%;
    position: absolute;
    z-index: 999;
  }

  .fixed-header {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 9;
    // width: calc(100% - #{$sideBarWidth});
    transition: width 0.28s;
  }

  .hideSidebar .fixed-header {
    // width: calc(100% - 54px)
    width: 100%
  }

  .mobile .fixed-header {
    width: 100%;
  }
  .navbar {
    height: 50px;
    overflow: hidden;
    position: relative;
    background: #fff;
    box-shadow: 0 1px 4px rgba(0,21,41,.08);

    .logo {
      float: left;
      height: 50px;
      width: 50px;
      margin-left: 15px;
    }
    .el-button {
      float: right;
      margin-right: 15px;
      margin-top: 5px;
    }
  }
  .footer {
    color: white;
    background-color: black;
    height: 50px;
    // position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    line-height: 50px;
    display: flex;
    .footer-item {
      flex: 1;
      text-align: center;
    }
  }
  .main-container {
    display: block;
    position: relative;
  }
</style>
