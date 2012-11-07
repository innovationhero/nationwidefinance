# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('referrals_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('referrals', ['Country'])

        # Adding model 'Organization'
        db.create_table('referrals_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('referrals', ['Organization'])

        # Adding model 'Entity'
        db.create_table('referrals_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('org_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('referrals', ['Entity'])

        # Adding model 'EntityReferral'
        db.create_table('referrals_entityreferral', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referrer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='referrer', to=orm['referrals.Entity'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('referrals', ['EntityReferral'])

        # Adding M2M table for field referred on 'EntityReferral'
        db.create_table('referrals_entityreferral_referred', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entityreferral', models.ForeignKey(orm['referrals.entityreferral'], null=False)),
            ('entity', models.ForeignKey(orm['referrals.entity'], null=False))
        ))
        db.create_unique('referrals_entityreferral_referred', ['entityreferral_id', 'entity_id'])

        # Adding model 'ReferrerPoints'
        db.create_table('referrals_referrerpoints', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referrer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrals.Entity'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('referrals', ['ReferrerPoints'])

        # Adding model 'EntityProfile'
        db.create_table('referrals_entityprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referrals.Country'])),
        ))
        db.send_create_signal('referrals', ['EntityProfile'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table('referrals_country')

        # Deleting model 'Organization'
        db.delete_table('referrals_organization')

        # Deleting model 'Entity'
        db.delete_table('referrals_entity')

        # Deleting model 'EntityReferral'
        db.delete_table('referrals_entityreferral')

        # Removing M2M table for field referred on 'EntityReferral'
        db.delete_table('referrals_entityreferral_referred')

        # Deleting model 'ReferrerPoints'
        db.delete_table('referrals_referrerpoints')

        # Deleting model 'EntityProfile'
        db.delete_table('referrals_entityprofile')


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
        'referrals.entityprofile': {
            'Meta': {'object_name': 'EntityProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referrals.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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