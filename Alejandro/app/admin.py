from django.contrib import admin
from app.models import User, Historia, Pub, PubComentario, PubLike, Follow

admin.site.register(User)
admin.site.register(Historia)
admin.site.register(Pub)
admin.site.register(PubComentario)
admin.site.register(PubLike)
admin.site.register(Follow)