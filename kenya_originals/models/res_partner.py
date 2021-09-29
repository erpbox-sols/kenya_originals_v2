# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TradingName(models.Model):
    _name = "trading.name"
    _description = " Trading Name"

    name = fields.Char("Business Name")


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_category_id = fields.Selection([('customer','Customer'),
                                    ('supplier','Supplier'),
                                    ('employee','Employee'),], string="Category", default='customer')
    business_partner_code = fields.Char("Business Partner Code", copy=False)
    business_ids = fields.Many2many("trading.name", string="Business Name", copy=False)
    sale_person_id = fields.Many2one('hr.employee', string="Salesperson", copy=False)
    saleperson_id = fields.Integer("Id", related="sale_person_id.id")
    customer_code_sub = fields.Char("Customer Code Sub", copy=False)
    division_id = fields.Many2one('division.name', string="Division", copy=False)
    region_id = fields.Many2one('region.name', string="Region", copy=False)
    area_id = fields.Many2one('region.areas', string="Area", copy=False)

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if not res.business_partner_code:
            seq = ''
            if res.partner_category_id == 'customer':
                seq = self.env['ir.sequence'].next_by_code('res.partner.customer')
            if res.partner_category_id == 'supplier':
                seq = self.env['ir.sequence'].next_by_code('res.partner.supplier')
            if res.partner_category_id == 'employee':
                seq = self.env['ir.sequence'].next_by_code('res.partner.employee')
            res.business_partner_code = seq
        if res.parent_id and res.type == 'delivery':
            sub_code = self.env['ir.sequence'].next_by_code('res.partner.delivery.child')
            res.business_partner_code = res.parent_id.business_partner_code
            res.customer_code_sub = res.parent_id.business_partner_code + sub_code
        elif res.parent_id and res.type == 'contact':
            res.partner_category_id = res.parent_id.partner_category_id
            seq = ''
            if res.partner_category_id == 'customer':
                seq = self.env['ir.sequence'].next_by_code('res.partner.customer')
            if res.partner_category_id == 'supplier':
                seq = self.env['ir.sequence'].next_by_code('res.partner.supplier')
            if res.partner_category_id == 'employee':
                seq = self.env['ir.sequence'].next_by_code('res.partner.employee')
            res.business_partner_code = seq
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'partner_category_id' in vals:            
            seq = ''
            if self.partner_category_id == 'customer':
                seq = self.env['ir.sequence'].next_by_code('res.partner.customer')
            if self.partner_category_id == 'supplier':
                seq = self.env['ir.sequence'].next_by_code('res.partner.supplier')
            if self.partner_category_id == 'employee':
                seq = self.env['ir.sequence'].next_by_code('res.partner.employee')
            self.business_partner_code = seq
        return res

class Divisions(models.Model):
    _name = "division.name"

    name = fields.Char("Division")

class Regions(models.Model):
    _name = "region.name"

    name = fields.Char("Region")

class RegionAreas(models.Model):
    _name = 'region.areas'
    _description = "Region & Areas"
    _rec_name = "area_id"

    division_id = fields.Many2one('division.name', string="Division")
    region_id = fields.Many2one("region.name", string="Region")
    area_id = fields.Char("Area")

