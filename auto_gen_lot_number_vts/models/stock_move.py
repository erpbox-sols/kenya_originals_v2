from odoo import models,api,fields
import datetime
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class stock_move(models.Model):
    _inherit="stock.move"

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        result = super(stock_move, self)._prepare_move_line_vals(quantity,reserved_quant)
        if self.purchase_line_id and not self.picking_id.backorder_id:
            if self.product_id.tracking == 'lot':
                auto_gen_lot_number = self.env['ir.config_parameter'].sudo().get_param('auto_gen_lot_number_vts.auto_generate_lot_configuration')
                if auto_gen_lot_number == 'schedule_date':
                    #scheduled_date = datetime.strptime(self.picking_id.scheduled_date,"%Y-%m-%d %H:%M:%S")
                    date = datetime.strftime(self.picking_id.scheduled_date,'%Y%m%d')
                elif auto_gen_lot_number == 'po_order_date':
                    #po_order_date = datetime.strptime(self.picking_id.purchase_id.date_order,"%Y-%m-%d %H:%M:%S")
                    date = datetime.strftime(self.picking_id.purchase_id.date_order,'%Y%m%d')
                else:
                    date = datetime.now().strftime('%Y%m%d')
                counter = 1
                lot_id_name=date
                lot_ids=self.env['stock.production.lot'].search([('product_id','=',self.product_id.id),('name',"ilike",date)])
                for lot in lot_ids:
                    counter+=1
                    lot_id_name=date+str(counter)
                vals={
                    "product_id":self.product_id.id,
                    "name":lot_id_name,
                    "company_id":self.company_id.id
                    }
                lot_id = self.env['stock.production.lot'].create(vals)
                result = dict(
                            result,
                            lot_id=lot_id.id,
                            qty_done=self.product_uom_qty)
        elif self.purchase_line_id and self.picking_id.backorder_id:
            move_id = self.env['stock.move'].search([('group_id','=',self.group_id.id),('id','!=',self.id)],limit=1)
            lot_id = move_id.move_line_ids.mapped('lot_id')
            result = dict(
                        result,
                        lot_id=lot_id.id,
                        qty_done=self.product_uom_qty)
        return result
