from django.contrib import admin

# Register your models here.
from goods.models import Commodity, Goods_spu, Unit, Activity, Goods_sku, Album, Wheel_planting, ActivityZone

admin.site.register(Commodity)
admin.site.register(Goods_spu)
admin.site.register(Unit)
admin.site.register(Activity)
admin.site.register(Goods_sku)
admin.site.register(Album)
admin.site.register(Wheel_planting)
admin.site.register(ActivityZone)
