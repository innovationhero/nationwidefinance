from django.conf import settings # import the settings file

def paypal_button_image(context):
    return {'PAYPAL_BUTTON_IMAGE': settings.PAYPAL_BUTTON_IMAGE}

def paypal_cc_image(context):
    return {'PAYPAL_CC_IMAGE': settings.PAYPAL_CC_IMAGE}

def paypal_action_url(context):
    return {'PAYPAL_ACTION_URL': settings.PAYPAL_ACTION_URL}