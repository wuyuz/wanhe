import axios from 'axios'
const MyHttpServer = {}
MyHttpServer.install = (Vue) => {
    axios.defaults.headers.post['Content-type'] = 'application/json'
    axios.defaults.headers['Access-Control-Allow-Origin'] = '*'
    Vue.prototype.$http = axios
    axios.defaults.baseURL = 'http://114.215.84.163:5001/api/v1/'
    axios.interceptors.request.use(function (config) {
        if (config.url !== 'login/') {
            const AUTH_TOKEN = window.sessionStorage.getItem('token')
            config.headers.common['Authorization'] = AUTH_TOKEN
        }
        return config
    }, function (error) {
        return Promise.reject(error)
    })
    // axios.interceptors.response.use(
    //   response => {
    //     // 导出
    //     const headers = response.headers
    //     console.log(response)
    //     return response
    //     // if (headers['responseType'] === 'application/octet-stream;charset=utf-8' || headers['content-type'] === 'application/json'){
    //     //   return response
    //     // }
    //   },
    //   error => {
    //     return Promise.reject(error)
    //   }
    // )
}
export default MyHttpServer
