from django.contrib import admin

# Register your models here.
from .models import user_meta,parts_model,channel_model,favorite_model,afirieito_model,categories_model,like_model,event_model,event_img_model,footer_model,footer_cat_model,tech_tube_model,tube_movie_model,tech_teaching_model,teaching_movie_model,bee_cate_model,bee_story_model

admin.site.register(user_meta)
admin.site.register(parts_model)
admin.site.register(channel_model)
admin.site.register(favorite_model)
admin.site.register(afirieito_model)
admin.site.register(categories_model)
admin.site.register(like_model)
admin.site.register(event_model)
admin.site.register(event_img_model)
admin.site.register(footer_cat_model)
admin.site.register(footer_model)
admin.site.register(tech_tube_model)
admin.site.register(tube_movie_model)
admin.site.register(tech_teaching_model)
admin.site.register(teaching_movie_model)
admin.site.register(bee_cate_model)
admin.site.register(bee_story_model)
