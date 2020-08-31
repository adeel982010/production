# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare

class StockScrapCoreEdite(models.Model):
    _inherit = 'stock.scrap'

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        states={'done': [('readonly', True)]}, domain="[('product_id', '=', product_id)]")


