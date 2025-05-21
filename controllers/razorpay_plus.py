# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing


class PaymentPostProcessingInherit(PaymentPostProcessing):

    @http.route('/payment/status', type='http', auth='public', website=True, sitemap=False)
    def display_status(self, **kwargs):
        """ Fetch the transaction and display it on the payment status page."""
        if self._get_monitored_transaction().provider_code == 'razorpay_plus':
            monitored_tx = self._get_monitored_transaction()
            print(monitored_tx.payment_method_id.read())
            if monitored_tx.state == 'draft' and monitored_tx.provider_id.state == 'test':
                monitored_tx.state = 'done'
        return super().display_status(**kwargs)