import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner
from xadmin.plugins.auth import UserAdmin


class EmailVerifyRecordAdmin(object):
    list_display = ['verify_code', 'email', 'send_type', 'send_time']  # 显示列
    list_filter = ['verify_code', 'email', 'send_type', 'send_time']
    search_fields = ['verify_code', 'email', 'send_type']
    model_icon = 'fa fa-envelope'
    # ordering  排序
    # readonly_fields = [] 只读字段
    # exclude 隐藏字段
    # relfield_style = 'fk-ajax'  搜索式加载数据


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'url', 'index']


# xadmin主题配置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# xadmin全局配置
class GlobalSettings(object):
    # 左上角标题
    site_title = '后台管理'
    # 底部标签
    site_footer = 'KevinPei'
    # 数据表格式
    menu_style = 'accordion'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
