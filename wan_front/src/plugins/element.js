import Vue from 'vue'
import 'element-ui/lib/theme-chalk/index.css'
import {
    Button,
    Form,
    FormItem,
    Input,
    Message,
    Container,
    Header,
    Aside,
    Main,
    Menu,
    Submenu,
    MenuItem,
    Breadcrumb,
    BreadcrumbItem,
    Card,
    Row,
    Col,
    Table,
    TableColumn,
    Pagination,
    Option,
    Dialog,
    Select,
    MessageBox,
    Cascader,
    Tag,
    Steps,
    Step,
    Alert,
    Tabs,
    TabPane,
    Avatar,
    Transfer
} from 'element-ui'


Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Pagination)
Vue.use(Option)
Vue.use(Dialog)
Vue.use(Select)
Vue.use(Cascader)
Vue.use(Tag)
Vue.use(Steps)
Vue.use(Step)
Vue.use(Alert)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Avatar)
Vue.use(Transfer)

Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm