# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    trading_id = fields.Many2one("trading.name", string="Trading Name", copy=False)


    @api.onchange('partner_id')
    def onchange_partner_shipping_id(self):
        if self.partner_id:
            return {'domain': {'trading_id': [('id', 'in', self.partner_id.business_ids.ids)]}}



