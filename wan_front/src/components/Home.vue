<template>
  <div style="height: 100%;">
    <el-container style="height: 100%;">
      <el-header class="headers">
        <div style="width:180px;height:40px;">
          <img src="@/assets/img/logo.png" alt />
        </div>
        <div style="width:110px;">
          <div>
            <el-avatar style="background-color:#9e688c">{{avatar}}</el-avatar>
          </div>
          <el-button type="info" size="mini" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-container style="height: 100%;">
        <el-aside :width="collapse ? '64px' : '200px'">
          <div class="toggle-btton" @click="toggleCollapse">|||</div>
          <!-- 两层for循环 -->
          <el-menu
            
            background-color="#545c64"
            :unique-opened="true"
            :collapse-transition="true"
            :collapse="collapse"
            :default-active="savePath"
            text-color="#fff"
            router
          >
            <el-submenu :index="'/'+item.id" v-for="item in menuList" :key="item.id">
              <template slot="title">
                <i :class="item.menu_icon"></i>
                <span style="font-size: 16px;">{{ item.title }}</span>
              </template>
              <el-menu-item
                :index="'/'+subitem.url"
                v-for="subitem in item.children"
                :key="subitem.id"
                @click="saveActive('/'+subitem.url)"
              >
                <span slot="title">
                  <i :class="subitem.icon" style="padding-left: 30px;margin-right:0px;"></i>
                  <span style="">{{ subitem.title }}</span>
                </span>
              </el-menu-item>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view @child-event="childMethod"></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuList: [],
      collapse: false,
      savePath: "",
      avatar: ""
    };
  },
  methods: {
    logout() {
      // 注销登录，清除sessionStorge数据
      window.sessionStorage.clear();
      this.$router.push("/login");
    },
    // 获取所有的菜单
    async getMenuList() {
      const { data: res } = await this.$http.get("login/");
      // console.log(res);
      this.menuList = res.data;
      // console.log(this.menuList[1].children);
    },
    toggleCollapse() {
      this.collapse = !this.collapse;
    },
    // 存储菜单栏状态
    saveActive(savepath) {
      window.sessionStorage.setItem("saveActive", savepath);
    },

    //父子传值方法
    childMethod(data) {
      // console.log(data);
      this.savePath = "/" + data;
      window.sessionStorage.setItem("saveActive", this.savepath);
    }
  },
  created() {
    this.getMenuList();
    this.avatar = window.sessionStorage.getItem("username").slice(0, 3);
    this.savePath = window.sessionStorage.getItem("saveActive");
  }
};
</script>

<style lang="less" scoped>
.inner_box {
  width: 300px;
  height: 100px;

  img {
    width: 100%;
    height: 100%;
  }
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: rgb(207, 195, 79);
  margin-right: 6px;
  line-height: 30px;
}

.el-header {
  background-color: #515a6e;
  color: #fff !important;
  text-align: center;
  height: 50px !important;
  line-height: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 10px;

  div {
    width: 180px;
    height: 46px;
    display: flex;
    align-items: center;
    img {
      width: 100%;
      height: 100%;
    }
  }
}

.el-aside {
  background-color: #1d1e23;
  color: #fff;
  text-align: center;
  line-height: 100%;
  .el-menu {
    // 去除边框有一个不对齐问题
    border-right: none;
    i {
      margin-right: 10px;
    }
    // li {
    //   background-color: #101117 !important;
    // }
  }
  span {
    margin-right: 20px;
  }
  .el-menu-item {
    font-size: 14px;
  }
}

.el-menu-item.is-active {
  color: #409eff;
}

.el-main {
  background-color: #e9eef3;
  color: black;
  text-align: center;
  line-height: 100%;
}

body > .el-container {
  margin-bottom: 40px;
  height: 100%;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.toggle-btton {
  background-color: #8091a9;
  font-size: 10px;
  text-align: center;
  line-height: 25px;
  color: #fff;
  letter-spacing: 0.2em;
  cursor: pointer;
}
</style>