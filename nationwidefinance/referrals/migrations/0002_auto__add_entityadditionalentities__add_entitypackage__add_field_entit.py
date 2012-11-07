# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntityAdditionalEntities'
        db.create_table('referrals_entityadditionalentities', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrals.Entity'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('referrals', ['EntityAdditionalEntities'])

        # Adding model 'EntityPackage'
        db.create_table('referrals_entitypackage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('package_description', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('max_referrals_allowed', self.gf('django.db.models.fields.IntegerField')()),
            ('unlimited_referrals', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_add_entity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_use_social_media', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('referrals', ['EntityPackage'])

        # Adding field 'EntityProfile.package'
        db.add_column('referrals_entityprofile', 'package',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrals.EntityPackage'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'EntityAdditionalEntities'
        db.delete_table('referrals_entityadditionalentities')

        # Deleting model 'EntityPackage'
        db.delete_table('referrals_entitypackage')

        # Deleting field 'EntityProfile.package'
        db.delete_column('referrals_entityprofile', 'package_id')


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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
        'referrals.entity': {
            'Meta': {'object_name': 'Entity'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'dob': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'referrals.entityadditionalentities': {
            'Meta': {'object_name': 'EntityAdditionalEntities'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Entity']"}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'referrals.entitypackage': {
            'Meta': {'object_name': 'EntityPackage'},
            'can_add_entity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_use_social_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_referrals_allowed': ('django.db.models.fields.IntegerField', [], {}),
            'package_description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unlimited_referrals': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'referrals.entityprofile': {
            'Meta': {'object_name': 'EntityProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.EntityPackage']", 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'referrals.entityreferral': {
            'Meta': {'object_name': 'EntityReferral'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referred': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'referred'", 'symmetrical': 'False', 'to': "orm['referrals.Entity']"}),
            'referrer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'referrer'", 'to': "orm['referrals.Entity']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'referrals.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'referrals.referrerpoints': {
            'Meta': {'object_name': 'ReferrerPoints'},
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referrer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Entity']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['referrals']