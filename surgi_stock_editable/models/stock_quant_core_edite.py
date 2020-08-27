# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from psycopg2 import OperationalError, Error

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)


class StockQuantCoreEdite(models.Model):
    _inherit = 'stock.quant'

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        ondelete='restrict', readonly=True,
        domain=lambda self: self._domain_lot_id())


