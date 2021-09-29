# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    division_id = fields.Many2one('division.name', string="Division", copy=False)
    region_ids = fields.Many2many('region.name', string="Regions", copy=False)
    area_ids = fields.Many2many('region.areas', string="Areas", copy=False)
