# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EntityProfile.dob'
        db.delete_column('referrals_entityprofile', 'dob')


    def backwards(self, orm):
        # Adding field 'EntityProfile.dob'
        db.add_column('referrals_entityprofile', 'dob',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'referrals.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'referrals.entitycontact': {
            'Meta': {'object_name': 'EntityContact'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'referrals.entityplan': {
            'Meta': {'object_name': 'EntityPlan'},
            'can_add_entity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_use_social_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direct_referal_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_referral_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'max_referrals_allowed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_referrals_for_gift': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'plan_description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'plan_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unlimited_referrals': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'referrals.entityprofile': {
            'Meta': {'object_name': 'EntityProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Country']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'direct_referal_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.EntityContact']"}),
            'entity_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirect_referral_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Industry']", 'null': 'True', 'blank': 'True'}),
            'inherit_from_plan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_referrals_for_gift': ('django.db.models.fields.IntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.EntityPlan']", 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referrals_made': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'referrals.entityreferral': {
            'Meta': {'object_name': 'EntityReferral'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referred': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'referred'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'referrer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referrer'", 'to': "orm['auth.User']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'referrals.industry': {
            'Meta': {'object_name': 'Industry'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'referrals.organizationreferredrelation': {
            'Meta': {'object_name': 'OrganizationReferredRelation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'org_referral'", 'to': "orm['auth.User']"}),
            'referred': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'org_referred_persons'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'referrals.organizationreferrerentity': {
            'Meta': {'object_name': 'OrganizationReferrerEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'org_referred'", 'to': "orm['auth.User']"}),
            'referrers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'org_referrer'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'referrals.referrerpoints': {
            'Meta': {'object_name': 'ReferrerPoints'},
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referrer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['referrals']