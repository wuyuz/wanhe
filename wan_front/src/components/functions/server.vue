<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>搜索信息</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card :gutter="0">
            <!-- 搜索行 -->
            <el-row>
                <el-form :inline="true">
<!--                    <el-col :span="8"><div class="grid-content bg-purple"></div></el-col>-->
                    <el-col :offset="6" :span="8">
                        <el-input placeholder="请输入你的症状" clearable v-model="queryset.query" class="input-with-select select-input-style" @clear="clearQuery">
                            <el-button type="primary" plain slot="append" icon="el-icon-search" @click="getData"></el-button>
                        </el-input>
                    </el-col>
<!--                    <el-col :span="8"><div class="grid-content bg-purple"></div></el-col>-->
                </el-form>
            </el-row>

            <!-- 表格内容 -->
            <el-row style="margin-top:20px;">
                <el-table :data="res.data" style="width: 100%" border>
                    <el-table-column prop="name" label="方案名" align="center" width="200"></el-table-column>
                    <el-table-column label="治疗病症" width="100" align="center">
                        <template slot-scope="scope" >
                            <span v-html = 'scope.row.illness'></span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="total_sale" label="方案总价" align="center"></el-table-column>
                    <el-table-column prop="detail" label="药品详细" align="center"></el-table-column>
                </el-table>
            </el-row>
        </el-card>

    </div>
</template>

<script>
export default {
    data() {
        return {
            queryset:{
                query: ""
            },
            res: []
        }
    },
    methods: {
        clearQuery () {
            this.queryset.query = "";
            this.res = []
        },
        async getData () {
            if (!this.queryset.query) return this.$message.warning("您什么症状都没有输入");
            const data = await this.$http.get("/search/",{params: this.queryset});
            if (data.status != 200) return this.$message.error("获取数据失败");
            this.res = data.data;
        }
    }
}
</script>

<style scoped>
    .select-input-style {
        width: 800px;
    }
</style>
