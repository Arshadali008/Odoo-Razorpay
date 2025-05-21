# -*- coding: utf-8 -*-
import logging
import requests
import pprint
from odoo import models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('razorpay_plus', "Razorpay Plus")], ondelete={'razorpay_plus': 'set default'}
    )
    razorpay_plus_key_id = fields.Char(
        string="Razorpay Key Id",
        help="The key solely used to identify the account with Razorpay.",
        required_if_provider='razorpay_plus',
    )
    razorpay_plus_key_secret = fields.Char(
        string="Razorpay Key Secret",
        required_if_provider='razorpay_plus',
        groups='base.group_system',
    )
    razorpay_plus_webhook_secret = fields.Char(
        string="Razorpay Webhook Secret",
        groups='base.group_system',
    )

    def _razorpay_make_request(self, endpoint, payload=None, method='POST'):
        """ Make a request to Razorpay API at the specified endpoint."""
        if self.code != 'razorpay_plus':
            return super()._razorpay_make_request(endpoint, payload=payload, method= method)
        self.ensure_one()
        # TODO: Make api_version a kwarg in master.
        api_version = self.env.context.get('razorpay_api_version', 'v1')
        url = f'https://api.razorpay.com/{api_version}/{endpoint}'
        headers = None
        if access_token := self._razorpay_get_access_token():
            headers = {'Authorization': f'Bearer {access_token}'}
        auth = (self.razorpay_plus_key_id, self.razorpay_plus_key_secret) if self.razorpay_plus_key_id else None
        try:
            if method == 'GET':
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    auth=auth,
                    timeout=10,
                )
            else:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    auth=auth,
                    timeout=10,
                )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
                )
                raise ValidationError("Razorpay: " + _(
                    "Razorpay gave us the following information: '%s'",
                    response.json().get('error', {}).get('description')
                ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Razorpay Plus: " + _("Could not establish the connection to the API.")
            )
        return response.json()

