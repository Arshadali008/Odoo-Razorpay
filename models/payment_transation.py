# -*- coding: utf-8 -*-
from odoo import models

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """ Override of `payment` to return razorpay-specific processing values."""
        if self.provider_code != 'razorpay_plus':
            return super()._get_specific_processing_values(processing_values)
        if self.operation in ('online_token', 'offline'):
            return {}
        customer_id = self._razorpay_create_customer()['id']
        order_id = self._razorpay_create_order(customer_id)['id']
        return {
            'razorpay_key_id': self.provider_id.razorpay_plus_key_id,
            'razorpay_public_token': self.provider_id._razorpay_get_public_token(),
            'razorpay_customer_id': customer_id,
            'is_tokenize_request': self.tokenize,
            'razorpay_order_id': order_id,
            'transaction_id': self.id,
        }