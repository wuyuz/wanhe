<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>药品信息</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card :gutter="0">
            <!-- 搜索行 -->
            <el-row>
                <el-col :span="1">
                    <el-button
                            type="primary"
                            plain
                            @click="addMedicine()"
                            size="mini"
                            style="margin-top: 12px;"
                    >新增</el-button>
                </el-col>
                <el-form :inline="true">
                    <el-col :offset="18" :span="5">
                        <el-input placeholder="请输入内容" v-model="queryset.query" class="input-with-select" clearable @clear="clearQuery">
                            <el-button type="primary" plain slot="append" icon="el-icon-search" @click="getData"></el-button>
                        </el-input>
                    </el-col>
                </el-form>
            </el-row>

            <!-- 表格内容 -->
            <el-row style="margin-top:20px;">
                <el-table :data="res.data" style="width: 100%" border>
<!--                    <el-table-column prop="id" label="序号" align="center" width="100"></el-table-column>-->
                    <el-table-column prop="name" label="药品名" align="center" width="200"></el-table-column>
                    <el-table-column prop="content" label="药品描述" width="1200" align="center"></el-table-column>
                    <el-table-column label="操作" fixed="right" width="120">
                        <template slot-scope="scope">
                            <el-button
                                    type="primary"
                                    size="mini"
                                    plain
                                    icon="el-icon-edit-outline"
                                    @click="editTypeFun(scope.row.id)"
                            ></el-button>
                            <el-button
                                    type="danger"
                                    size="mini"
                                    plain
                                    icon="el-icon-delete"
                                    @click="removeTypeFun(scope.row.id)"
                            ></el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>
            <el-row style="margin-top:20px;">
                <el-pagination
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page.sync="queryset.page"
                        :page-sizes="[10, 30, 50]"
                        :page-size="10"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="res.count"
                ></el-pagination>
            </el-row>
        </el-card>
        <el-dialog title="新增药品类型" :visible.sync="dialogFormVisible" width="50%" @close="closeDialog()">
            <el-form :model="addtypeForm" ref="addFormRef" :rules="rules">
                <el-form-item label="药品类型名" :label-width="formLabelWidth" prop="name">
                    <el-input v-model="addtypeForm.name" autocomplete="off" style="width:80%;"></el-input>
                </el-form-item>
                <el-form-item label="商品描述" :label-width="formLabelWidth" prop="content">
                    <el-input type="textarea" maxlength="400" show-word-limit v-model="addtypeForm.content" autocomplete="off" :rows="8" style="width:80%;"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="closeDialog">取 消</el-button>
                <el-button type="primary" @click="addData">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog title="修改药品类型" :visible.sync="editVisible" width="50%" @close="editDialog()">
            <el-form :model="addsForm" ref="editFormsRef" :rules="rules">
                <el-form-item label="药品名" :label-width="formLabelWidth" prop="name">
                    <el-input v-model="addsForm.name" autocomplete="off" style="width:80%;"></el-input>
                </el-form-item>
                <el-form-item label="药品类型说明" :label-width="formLabelWidth" prop="content">
                    <el-input type="textarea" maxlength="400" show-word-limit v-model="addsForm.content" autocomplete="off" :rows="8" style="width:80%;"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="editDialog()">取 消</el-button>
                <el-button type="primary" @click="editData">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                res: {},
                loading: false,
                queryset: {
                    query: "",
                    page: 1,
                    size: 10
                },
                dialogFormVisible: false,
                editVisible: false,
                formLabelWidth: "100px",
                addtypeForm: {
                    name: "",
                    content: "",
                },
                addsForm: {
                    name: "",
                    id: "",
                    content: "",
                },
                rules: {
                    name: [
                        { required: true, message: "药品类型名称", trigger: "blur" },
                        { min: 2, message: "长度不能少于2个字符", trigger: "blur" }
                    ]
                }
            };
        },
        methods: {
            clearQuery () {
                this.queryset.query = "";
                this.getData()
            },
            addMedicine () {
                this.addtypeForm = {};
                this.dialogFormVisible = true

            },
            // 获取数据函数
            async getData() {
                const data = await this.$http.get("/medicinetype/", {
                    params: this.queryset
                });
                if (data.status != 200) return this.$message.error("获取数据失败");
                // 存储数据
                this.res = data.data;
            },

            // 分页页码数
            async handleSizeChange(newval) {
                this.queryset.size = newval;
                const data = await this.$http.get("/medicinetype/", {
                    params: this.queryset
                });

                if (data.status != 200) return this.$message.error("获取数据失败");
                this.res = data.data;
            },

            // 当前页码变化函数
            async handleCurrentChange(currentpage) {
                this.queryset.page = currentpage;
                const data = await this.$http.get("/medicinetype/", {
                    params: this.queryset
                });

                if (data.status != 200) return this.$message.error("获取数据失败");
                this.res = data.data;
            },

            // 关闭/取消模态框
            closeDialog() {
                this.$refs.addFormRef.resetFields();
                this.dialogFormVisible = false;
            },

            // 关闭取消修改模态框
            editDialog() {
                this.$refs.editFormsRef.resetFields();
                this.editVisible = false;
            },

            // 提交修改按钮函数
            editData() {
                this.$refs.editFormsRef.validate(async valid => {
                    if (!valid) return;
                    const data = await this.$http.put("/medicinetype/", this.addsForm);
                    if (data.data.code != 200) {
                        this.editVisible = false;
                        this.$message.error("修改失败");
                        return;
                    }
                    this.getData();
                    this.editVisible = false;
                    this.$message.success("修改成功");
                    this.$refs.editFormsRef.resetFields();
                });
            },

            // 提交新增数据
            addData() {
                // 先表单验证
                this.$refs.addFormRef.validate(async valid => {
                    if (!valid) return;
                    const data = await this.$http.post("/medicinetype/", this.addtypeForm);
                    if (data.data.code != 200) return this.$message.error(`${data.msg}`);
                    this.dialogFormVisible = false;
                    this.$refs.addFormRef.resetFields();
                    this.$message.success(`${data.data.msg}`);
                    this.getData();
                });
            },

            // 编辑函数
            async editTypeFun(id) {
                const data = await this.$http.get("/medicinetype/", { params: { id: id } });
                if (data.status != 200) return this.$message.error("获取数据失败");
                this.addsForm = data.data.data;
                this.editVisible = true;
            },

            // 删除按钮事件
            async removeTypeFun(id) {
                var msg = await this.$confirm(
                    "此操作将永久删除该命令,是否继续?",
                    "提示",
                    {
                        confirmButtonText: "确定",
                        cancelButtonText: "取消",
                        type: "warning"
                    }
                )
                    //  截获异常和取消
                    .catch(err => err);
                if (msg != "confirm") return this.$message.info("已取消删除");
                const data = await this.$http.delete(`/medicinetype/`, { params: { id: id } });
                if (data.data.code != 200) {
                    return this.$message.error("删除失败");
                }
                this.getData();
                this.$message.success("删除成功");
            }
        },

        created: function() {
            this.getData();
        }
    };
</script>

<style>
    .el-table .warning-row {
        background: oldlace;
    }

    .el-table .success-row {
        background: #f0f9eb;
    }
    .el-form-item__error {
        left: 40% !important;
    }
</style>
