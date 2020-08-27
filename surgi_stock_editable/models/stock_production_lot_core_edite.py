# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    _check_company_auto = False


    _sql_constraints = [
        ('name_ref_uniq', 'unique (name, product_id)', 'The combination of serial number and product must be unique across a company !'),
    ]


    def write(self, vals):
        if 'product_id' in vals and any([vals['product_id'] != lot.product_id.id for lot in self]):
            move_lines = self.env['stock.move.line'].search([('lot_id', 'in', self.ids), ('product_id', '!=', vals['product_id'])])
            if move_lines:
                raise UserError(_(
                    'You are not allowed to change the product linked to a serial or lot number ' +
                    'if some stock moves have already been created with that number. ' +
                    'This would lead to inconsistencies in your stock.'
                ))
        return super(ProductionLot, self).write(vals)