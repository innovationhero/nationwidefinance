from django.contrib import admin

from nationwidefinance.referrals import models

admin.site.register(models.Organization)
admin.site.register(models.EntityReferral)
admin.site.register(models.EntityProfile)
admin.site.register(models.Country)
admin.site.register(models.ReferrerPoints)
admin.site.register(models.Entity)

