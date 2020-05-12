<template>
  <div class="login_container">
    <div class="login_box">
      <!-- ref 是将起变为一个vue属性,rules是制定表单规则，model表示制定的的模型 -->
      <el-form
        label-width="0px"
        ref="loginFormRef"
        :rules="loginFormRules"
        :model="loginForm"
        class="login_form"
      >
        <div class="avatar_box" style="text-align:center">
          <!-- <img src="@/assets/img/logo1.png" alt="logo" /> -->
          <h3> 药库系统 </h3>
        </div>
        <el-form-item prop="username">
          <el-input placeholder="用户名" prefix-icon="el-icon-s-custom" v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="密码"
            prefix-icon="el-icon-s-flag"
            v-model="loginForm.password"
          ></el-input>
        </el-form-item>
        <el-form-item class="btns">
          <el-button round @click="rest">重置</el-button>
          <el-button type="primary" round @click="login">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        username: "admin",
        password: "0pen.Wanhe.Admin"
      },
      loginFormRules: {
        username: [
          {
            required: true,
            message: "请输入用户名",
            trigger: "blur"
          },
          {
            min: 3,
            max: 10,
            message: "长度在3到10个字符",
            trigger: "blur"
          }
        ],
        password: [
          {
            required: true,
            message: "请输入登录密码",
            trigger: "blur"
          },
          {
            min: 4,
            max: 30,
            message: "长度在6到15个字符",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    rest() {
      // 重置，首先需要给表单对象使用ref,标识为一个vue对象，才好重置
      this.$refs.loginFormRef.resetFields();
    },
    login() {
      // 登录之前先进行表单预校验,会返回一个值，合格则为true,不合格为false
      this.$refs.loginFormRef.validate(async valid => {
        if (!valid) return;
        // 将data结构成res
        const { data: res } = await this.$http.post("login/", this.loginForm);
        // console.log(res)
        if (res.code !== 200) return this.$message.error("登录失败");
        this.$message.success("登录成功");

        // 将登录成功后的token进行保存到，客户端的sessionStorge中
        window.sessionStorage.setItem("token", res.token);
        window.sessionStorage.setItem("username", res.username);
        // 通过编程式导航到主页
        this.$router.push("/home");
      });
    }
  }
};
</script>

<style lang="less" scoped>
.login_container {
  background-color: #2b4b6b;
  height: 100%;
}

.login_box {
  width: 500px;
  height: 350px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgb(83, 124, 158);
}

.login_form {
  position: absolute;
  bottom: 0px;
  width: 100%;
  padding: 0 60px;
  box-sizing: border-box;
}

.avatar_box {
  position: relative;
  width: 280px;
  height: 65px;
  transform: translate(13%, -50%);

  img {
    width: 100%;
    height: 100%;
  }
}

.btns {
  margin-top: 50px;
  display: flex;
  justify-content: flex-end;
}
</style>