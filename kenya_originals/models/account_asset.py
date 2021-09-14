from odoo import _, api, fields, models

class AccountAsset(models.Model):
	_inherit = "account.asset"


	parent_asset_id = fields.Many2one("account.asset", string="Parent Asset")