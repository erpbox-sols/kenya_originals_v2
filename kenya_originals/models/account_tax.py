from odoo import _, api, fields, models

class AccountTax(models.Model):
    _inherit = 'account.tax'

    dont_show_on_invoice = fields.Boolean("Don't show on PDF Invoice")

    