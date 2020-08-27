from collections import Counter

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round, float_compare, float_is_zero

class StockMoveLineCoreEdite(models.Model):
    _inherit = 'stock.move.line'

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id)]")


