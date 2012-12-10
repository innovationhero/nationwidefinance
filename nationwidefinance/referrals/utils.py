from nationwidefinance.referrals import models

def calculate_points(referred_list, processed=None, value=None):
    referrals = models.EntityReferral.objects.filter(referred__pk__in=referred_list)
    if len(referrals) == 0: return
    referred_list = []
    for referral in referrals:
        referred_list.append(referral.referrer.pk)

        try:
            referral_point = models.ReferrerPoints.objects.get(referrer__pk=referral.referrer.pk)
            referral_point.value += value
        except models.ReferrerPoints.DoesNotExist:
            referral_point = models.ReferrerPoints(referrer=referral.referrer, entity_active=True, value=value)

        referral_point.save()
    if not processed: 
        processed = set([entity['id'] for referral in referrals for entity in referral.referred.values()])
    else: 
        processed|=set([entity['id'] for referral in referrals for entity in referral.referred.values()])
    print processed
    print referred_list

    return calculate_points([referral.referrer.id for referral in referrals if referral.referrer.id not in processed], processed=processed, value=value)