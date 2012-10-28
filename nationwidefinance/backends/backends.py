from nationwidefinance.referrals.models import Entity

class EntityAuthenticationBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            entity = Entity.objects.get(username=username)
            if person.check_password(password):
                return entity
        except Entity.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return Entity.objects.get(pk=user_id)
        except Entity.DoesNotExist:
            return None