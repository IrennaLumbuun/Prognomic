<template>
  <div class="login-container">
    <div class="navbar">
      <img src="../../img/logo.jpeg" class="logo">
      <el-button
        type="primary"
        @click="isSignIn = !isSignIn">{{isSignIn ? "Register" : "Sign In"}}</el-button>
    </div>
    <div class="main">
      <div class="login-background" :hidden="!isSignIn"></div>
      <div class="login-form">
        <el-form
          ref="loginForm"
          :hidden="!isSignIn"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          auto-complete="on"
          label-position="left"
        >
          <!-- <div class="title-container">
            <h3 class="title">Sign In</h3>
          </div> -->
          <el-form-item prop="username">
            <span class="svg-container">
              <svg-icon icon-class="user" />
            </span>
            <el-input
              ref="username"
              v-model="loginForm.username"
              placeholder="Username"
              name="username"
              type="text"
              tabindex="1"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item prop="password">
            <span class="svg-container">
              <svg-icon icon-class="password" />
            </span>
            <el-input
              :key="passwordType"
              ref="password"
              v-model="loginForm.password"
              :type="passwordType"
              placeholder="Password"
              name="password"
              tabindex="2"
              auto-complete="on"
              @keyup.enter.native="handleLogin"
            />
            <span class="show-pwd" @click="showPwd">
              <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </el-form-item>
          <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">Submit</el-button>
          <p>Don't have an account? <a style="color: blue" @click="isSignIn=false">Register</a></p>
          <!-- <div class="tips">
            <span style="margin-right:20px;">username: admin</span>
            <span> password: any</span>
          </div> -->
        </el-form>
        <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="login-form" auto-complete="on" label-position="left" :hidden="isSignIn">
          <!-- <div class="title-container">
            <h3 class="title">Register</h3>
          </div> -->
          <el-form-item prop="username">
            <span class="svg-container">
              <svg-icon icon-class="user" />
            </span>
            <el-input
              ref="username"
              v-model="registerForm.username"
              placeholder="Username"
              name="username"
              type="text"
              tabindex="1"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item prop="email">
            <span class="svg-container">
              <svg-icon icon-class="mail" />
            </span>
            <el-input
              ref="email"
              v-model="registerForm.email"
              placeholder="Email"
              name="email"
              type="text"
              tabindex="2"
              auto-complete="on"
            />
          </el-form-item>
          <el-form-item prop="password">
            <span class="svg-container">
              <svg-icon icon-class="password" />
            </span>
            <el-input
              :key="passwordType"
              ref="password"
              v-model="registerForm.password"
              :type="passwordType"
              placeholder="Password"
              name="password"
              tabindex="3"
              auto-complete="on"
            />
            <span class="show-pwd" @click="showPwd">
              <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </el-form-item>
          <el-form-item prop="cpassword">
            <span class="svg-container">
              <svg-icon icon-class="password" />
            </span>
            <el-input
              :key="passwordType"
              ref="cpassword"
              v-model="registerForm.cpassword"
              :type="passwordType"
              placeholder="Confirm Password"
              name="cpassword"
              tabindex="4"
              auto-complete="on"
            />
            <span class="show-pwd" @click="showPwd">
              <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </el-form-item>
          <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleRegister">Submit</el-button>
          <p style="text-align: center">Have an account? <a @click="isSignIn=true" style="color: blue">Login</a></p>
          <!-- <div class="tips">
            <span style="margin-right:20px;">username: admin</span>
            <span> password: any</span>
          </div> -->
        </el-form>
      </div>
    </div>
    <div class="footer">
      <div class="footer-item">Site map</div>
      <div class="footer-item">Terms</div>
      <div class="footer-item">Privacy</div>
      <div class="footer-item">Contact us</div>
      <div class="footer-item">About us</div>
    </div>
  </div>
</template>

<script>
import { validUsername, validEmail } from '@/utils/validate'
export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    const validateCpassword = (rule, value, callback) => {
      console.log(this.registerForm)
      if (this.registerForm.password !== value) {
        callback(new Error('Passwords don\'t match'))
      } else {
        callback()
      }
    }
    const validateEmail = (rule, value, callback) => {
      if (value.length == 0 || validEmail(value)) {
        callback()
      } else {
        callback(new Error('Invalid email'))
      }
    }
    return {
      isSignIn: true,
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      registerRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        cpassword: [{ required: true, trigger: 'blur', validator: validateCpassword }],
        email: [{ trigger: 'blur', validator: validateEmail }]
      },
      registerForm: {
        username: '',
        password: '',
        email: ''
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('login error')
          return false
        }
      })
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true
          console.log('start')
          this.$store.dispatch('user/register', this.registerForm).then(() => {
            this.$router.go()
            console.log('start2')
            // this.$router.push({ path: '/login' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('Register error')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
// $light_gray:#fff;
$light_gray:black;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    // height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      // height: 47px;
      // caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
// $light_gray:#eee;
$light_gray: black;

.login-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: stretch;
  min-height: 100%;
  width: 100%;
  // background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    // height: 100vh;
    // min-height: 100%;
    // width: 520px;
    max-width: 520px;
    padding: 40px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: black;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
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
  .main {
    flex: 1;
    display: flex;
    // overflow: auto;
    .login-background {
      flex: 5;
      background-image: url('../../img/image_landing.jpg');
      background-position: center;
      background-repeat: no-repeat;
      // background-size: cover;
      background-size: 88%;
    }
    .login-form {
      flex: 2;
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
}
</style>
