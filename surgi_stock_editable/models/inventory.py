from openerp import models, fields, api,_

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    location_ids = fields.Many2many(
        'stock.location', string='Locations',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)]},
        domain="[]")


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    location_id = fields.Many2one(
        'stock.location', 'Location', check_company=True,
        domain="[]",
        index=True, required=True)

    # @api.model
    # def _domain_location_id(self):
    #     if self.env.context.get('active_model') == 'stock.inventory':
    #         inventory = self.env['stock.inventory'].browse(self.env.context.get('active_id'))
    #         if inventory.exists() and inventory.location_ids:
    #             return "[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit']), ('id', 'child_of', %s)]" % inventory.location_ids.ids
    #     return "[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit'])]"
