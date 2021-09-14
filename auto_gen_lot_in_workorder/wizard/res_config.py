from odoo import fields,models,api

class res_config(models.TransientModel): 
    _inherit='res.config.settings'
        
    auto_generate_mo_lot_based_on = fields.Selection([('today_date','Today Date'),('production_date','Production Date')],default='today_date',string='Lot No Generate Based On')
    
    @api.model
    def get_values(self):
        res = super(res_config, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(                    
                    auto_generate_mo_lot_based_on = params.get_param('auto_gen_lot_in_workorder.auto_generate_mo_lot_based_on',default='today_date')
                   )
        return res
    
    def set_values(self):
        super(res_config,self).set_values()
        ir_parameter = self.env['ir.config_parameter'].sudo()        
        ir_parameter.set_param('auto_gen_lot_in_workorder.auto_generate_mo_lot_based_on', self.auto_generate_mo_lot_based_on)
        
