# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG

class InventoryCoreEdite(models.Model):
    _inherit = 'stock.inventory'

    prod_lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id','=',product_id)]")