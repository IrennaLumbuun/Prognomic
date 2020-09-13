import request from '@/utils/request'

export function upload(params) {
  console.log(params)
  return request({
    url: '/api/eye-abnormality',
    method: 'post',
    params,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
