from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_uom_qty = fields.Float('Quantity', digits='Manufacturing',
        default=1.0, required=True, states={'done': [('readonly', True)]},
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_available = fields.Float(
        'Quantity On Hand', compute='_compute_quantities', search='_search_qty_available',
        compute_sudo=False, digits='Manufacturing')

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Manufacturing', required=True)
    