from django.contrib import admin

from nationwidefinance.referrals import models

admin.site.register(models.EntityReferral)
admin.site.register(models.EntityProfile)
admin.site.register(models.Country)
admin.site.register(models.ReferrerPoints)
admin.site.register(models.EntityPlan)
admin.site.register(models.EntityContact)
admin.site.register(models.Industry)
admin.site.register(models.FacebookPostMessage)
#admin.site.register(models.OrganizationReferrerEntity)
#admin.site.register(models.OrganizationReferredRelation)

