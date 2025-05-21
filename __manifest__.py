# -*- coding: utf-8 -*-
{
    'name': "Payment Provider: Razorpay Plus",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A payment provider covering India.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment'],
    'data': [
        'views/payment_razorpay_plus_templates.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
        # Depends on views/payment_razorpay_templates.xml
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_razorpay_plus/static/src/js/razorpay_plus.js',
        ],
    },
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
}
