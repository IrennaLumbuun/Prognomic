<template>
  <div class="app-container">
    <h3>
      Upload Photo
    </h3>
    <el-upload
      ref="uploadField"
      class="upload-demo"
      drag
      action='http://techack.pythonanywhere.com/api/eye-abnormality'
      :auto-upload="false"
      :show-file-list="false"
      :on-change="onChange"
      :hidden="isUploaded"
      :on-success="onSuccess"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">Upload photos</div>
    </el-upload>
    <div class="preview" :hidden="!isUploaded">
      <!-- Your image preview -->
      <img ref="imgPreview" alt="" />
    </div>
    <div :hidden="!isUploaded" style="margin-top: 30px">
      <el-button size="medium" @click="onCancel">
        Cancel
      </el-button>
      <el-button size="medium" type="primary" @click="onSubmit">
        Submit
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isUploaded: false,
      fileList: []
    }
  },
  methods: {
    onSuccess(response, file, fileList) {
      this.$router.push('/')
    },
    onSubmit() {
      // 'http://localhost:5000/api/eye-abnormality'
      this.$refs.uploadField.submit()
    },
    onCancel() {
      this.isUploaded = false
      this.fileList = []
    },
    onChange(file, fileList) {
      if (file) {
        console.log(file)
        this.isUploaded = true
        this.fileList = [file]
        const reader = new FileReader()
        const imgPreview = this.$refs.imgPreview
        reader.onload = function(e) {
          imgPreview.src = e.target.result
        }
        reader.readAsDataURL(file.raw)
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  /* display: flex;
  flex-direction: center; */
  text-align: center;
}
.line{
  text-align: center;
}
.preview {
  max-width: 240px;
  max-height: 240px;
  margin: 10px auto 0px auto;
}
img {
  width: 100%;
  height: 100%;
}
</style>

