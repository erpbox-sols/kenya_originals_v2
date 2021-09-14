# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    apply_manual_currency_exchange = fields.Boolean(string='Apply Manual Currency Exchange')
    manual_currency_exchange_rate = fields.Float(string='Manual Currency Exchange Rate', store=True)
    active_manual_currency_rate = fields.Boolean('Active Manual Currency', default=False)

    @api.onchange('company_id','currency_id')
    def onchange_currency_id(self):
        if self.company_id or self.currency_id:
            if self.company_id.currency_id != self.currency_id:
                self.active_manual_currency_rate = True
            else:
                self.active_manual_currency_rate = False
        else:
            self.active_manual_currency_rate = False


    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):

        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        self.purchase_vendor_bill_id = False

        if not self.purchase_id:
            return

        # Copy partner.
        self.partner_id = self.purchase_id.partner_id
        self.fiscal_position_id = self.purchase_id.fiscal_position_id
        self.invoice_payment_term_id = self.purchase_id.payment_term_id
        self.currency_id = self.purchase_id.currency_id
        self.apply_manual_currency_exchange = self.purchase_id.apply_manual_currency_exchange
        self.manual_currency_exchange_rate = self.purchase_id.manual_currency_exchange_rate

        # Copy purchase lines.
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        new_lines = self.env['account.move.line']
        for line in po_lines.filtered(lambda l: not l.display_type):
            new_line = new_lines.new(line._prepare_account_move_line(self))
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line
        new_lines._onchange_mark_recompute_taxes()

        # Compute invoice_origin.
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))

        # Compute ref.
        refs = set(self.line_ids.mapped('purchase_line_id.order_id.partner_ref'))
        refs = [ref for ref in refs if ref]
        self.ref = ','.join(refs)

        # Compute _invoice_payment_ref.
        if len(refs) == 1:
            self._invoice_payment_ref = refs[0]

        self.purchase_id = False
        self._onchange_currency()

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    
        
    debit = fields.Monetary(string='Debit', default=0.0, currency_field='company_currency_id',compute='_constraint_amount_currency_exchange',store=True)
    credit = fields.Monetary(string='Credit', default=0.0, currency_field='company_currency_id',compute='_constraint_amount_currency_exchange',store=True)
    

    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):

        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1
        price_subtotal *= sign
        if currency and currency != company.currency_id:
            # Multi-currencies.
            if self.move_id.apply_manual_currency_exchange:
                balance = price_subtotal * self.move_id.manual_currency_exchange_rate
            else:
                balance = currency._convert(price_subtotal, company.currency_id, company, date)
            return {
                'amount_currency': price_subtotal,
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
            }
        else:
            # Single-currency.
            return {
                'amount_currency': 0.0,
                'debit': price_subtotal > 0.0 and price_subtotal or 0.0,
                'credit': price_subtotal < 0.0 and -price_subtotal or 0.0,
            }

     
    @api.onchange('amount_currency')
    def _onchange_amount_currency_exchange(self):
        
        for line in self:
            
            if line.currency_id and line.currency_id != line.company_id.currency_id:
                
            # Multi-currencies.
                if line.move_id.apply_manual_currency_exchange:                    
                    balance = line.amount_currency * line.move_id.manual_currency_exchange_rate
#                     raise ValidationError((balance))
#                 else:
#                     balance = line.amount_currency._convert(price_subtotal, company.currency_id, company, date)
                    line.update({
    #                     'amount_currency': 0.0,
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                    })
#                     raise ValidationError((line.debit))

    

    @api.depends('amount_currency')
    def _constraint_amount_currency_exchange(self):
         
        for line in self:
            
            if line.currency_id and line.currency_id != line.company_id.currency_id:
                
            # Multi-currencies.
                if line.move_id.apply_manual_currency_exchange:                    
                    balance = line.amount_currency * line.move_id.manual_currency_exchange_rate
#                     raise ValidationError((balance))
#                 else:
#                     balance = line.amount_currency._convert(price_subtotal, company.currency_id, company, date)
                    line.update({
    #                     'amount_currency': 0.0,
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                    })
#                     raise ValidationError((line.debit))

    
