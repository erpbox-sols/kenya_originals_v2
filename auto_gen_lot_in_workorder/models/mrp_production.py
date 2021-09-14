from odoo import fields,models,api,_
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import math
from datetime import datetime
import time

class MrpProductionWorkcenterLine(models.Model):
    _inherit = "mrp.workorder"

    def _next(self, continue_production=False):
        self.ensure_one()
        if self.test_type in ('register_byproducts'):
            if self.component_tracking != 'none' and not self.lot_id and self.qty_done != 0:
                counter = 1
                auto_gen_lot_number = self.env['ir.config_parameter'].sudo().get_param(
                    'auto_gen_lot_number_in_mo.auto_generate_mo_lot_based_on')
                if auto_gen_lot_number == 'production_date':
                    #production_date = datetime.strptime(order.date_planned_start,"%Y-%m-%d %H:%M:%S")
                    #date = datetime.strftime(production_date,'%Y%m%d')
                    date = datetime.strftime(self.date_planned_start,'%Y%m%d')
                else:
                    date = datetime.now().strftime('%Y%m%d')
                lot_ids = self.env['stock.production.lot'].search(
                    [('product_id', '=', self.component_id.id), ('name', "ilike", date)])
                if lot_ids:
                    for lot in lot_ids:
                        counter += 1
                    lot_id_name = date + str(counter)
                else:
                    lot_id_name = date
                vals = {
                    "product_id": self.component_id.id,
                    "name": lot_id_name,
                    "company_id": self.company_id.id
                }
                finished_lot_id = self.env['stock.production.lot'].create(vals)
                self.lot_id = finished_lot_id.id
        result = super(MrpProductionWorkcenterLine, self)._next(continue_production=continue_production)

        return result

class mrp_production_al(models.Model):
    _inherit="mrp.production"
    
    lot_id=fields.Many2one('stock.production.lot', string='Lot',copy=False)
    
    def button_plan(self):
        super(mrp_production_al, self).button_plan()
        for order in self:
            auto_gen_lot_number = self.env['ir.config_parameter'].sudo().get_param('auto_gen_lot_number_in_mo.auto_generate_mo_lot_based_on')
            if auto_gen_lot_number == 'production_date':
                date = datetime.strftime(self.date_planned_start,'%Y%m%d')
            else:
                date = datetime.now().strftime('%Y%m%d')
            for workorder in order.workorder_ids.filtered(lambda wk:wk.state == 'ready'):
                counter=1
                if workorder.finished_lot_id:
                    super(mrp_production_al,self).button_plan()
                else:
                    lot_id_name = date
                    lot_ids=self.env['stock.production.lot'].search([('product_id','=',order.product_id.id),('name',"ilike",date)])
                    if lot_ids:
                        for lot in lot_ids:
                            counter+=1
                        lot_id_name=date+str(counter)
                    else:
                        lot_id_name=date
                    vals={
                            "product_id":order.product_id.id,
                            "name":lot_id_name,
                            "company_id":order.company_id.id
                            }
                    finished_lot_id = self.env['stock.production.lot'].create(vals)
                    workorder.finished_lot_id = finished_lot_id.id
            # for move_line in order.move_byproduct_ids:
            #     lot_name = date
            #     lot_ids = self.env['stock.production.lot'].search(
            #         [('product_id', '=', move_line.product_id.id), ('name', "ilike", lot_name)])
            #     if lot_ids:
            #         for lot in lot_ids:
            #             counter += 1
            #         lot_name = date + str(counter)
            #     else:
            #         lot_name = date
            #     vals = {
            #         "product_id": move_line.product_id.id,
            #         "name": lot_name,
            #         "company_id": order.company_id.id
            #     }
            #     byprd_lot_id = self.env['stock.production.lot'].create(vals)
            #     vals = move_line._prepare_move_line_vals()
            #     vals.update({'lot_id':byprd_lot_id.id,'qty_done':1})
            #     self.env['stock.move.line'].create(vals)

    def open_produce_product(self):
        #if self.product_id.tracking == 'lot':
        auto_gen_lot_number = self.env['ir.config_parameter'].sudo().get_param('auto_gen_lot_number_in_mo.auto_generate_mo_lot_based_on')
        if auto_gen_lot_number == 'production_date':
            #production_date = datetime.strptime(self.date_planned_start,"%Y-%m-%d %H:%M:%S")
            date = datetime.strftime(self.date_planned_start,'%Y%m%d%H')
        else:
            date = datetime.now().strftime('%Y%m%d')
        
        if self.lot_id:
            res= super(mrp_production_al,self).open_produce_product()
        else:
            counter=1
            lot_id_name = date
            lot_ids=self.env['stock.production.lot'].search([('product_id','=',self.product_id.id),('name',"ilike",date)])
            if lot_ids:
                for lot in lot_ids:
                    counter+=1
                lot_id_name=date+"000"+str(counter)
            else:
                lot_id_name=date+"0001"
            vals={
                    "product_id":self.product_id.id,
                    "name":lot_id_name
                    }
            self.lot_id = self.env['stock.production.lot'].create(vals)
        return super(mrp_production_al,self).open_produce_product()
