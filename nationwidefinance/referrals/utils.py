from nationwidefinance.referrals import models

def calculate_points(referrer_list, count, processed=None):
	referrals = models.EntityReferral.objects.filter(referrer__pk__in = referrer_list)
	if not processed:
		processed = set([referral.referrer.id for referral in referrals])
	else:
		processed|=set([referral.referrer.id for referral in referrals])
	print 'processed = ', processed
	print 'referrals = ', referrals
	if len(referrals) == 0: return count
	count += sum([len(referral.referred.values()) for referral in referrals])
	return calculate_points([entity['id'] for referral in referrals for entity in referral.referred.values() if entity['id'] not in processed],count,processed=processed)