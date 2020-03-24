class Pagination(object):
    """
    自定义分页
    """

    def __init__(self, current_page, total_count, base_url, params, per_page_count=10, max_pager_count=11):
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        self.current_page = current_page
        # 数据总条数
        self.total_count = total_count

        # 每页显示10条数据
        self.per_page_count = per_page_count

        # 页面上应该显示的最大页码
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        self.max_page_num = max_page_num

        # 页面上默认显示11个页码（当前页在中间）
        self.max_pager_count = max_pager_count
        self.half_max_pager_count = int((max_pager_count - 1) / 2)

        self.base_url = base_url

        # request.GET
        # import copy
        # params = copy.deepcopy(params)
        # get_dict = params.to_dict()
        #
        # self.params = get_dict
        if not params:
            params = ""
        self.params = params

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def count(self):
        return self.max_page_num

    @property
    def prev(self):
        if self.current_page > 1:
            return self.base_url + "?page=" + str(
                self.current_page - 1) + "&query=" + self.params + "&size=" + str(self.per_page_count)

    @property
    def next(self):
        if self.current_page < self.max_page_num:
            return self.base_url + "?page=" + str(
                self.current_page + 1) + "&query=" + self.params + "&size=" + str(self.per_page_count)
