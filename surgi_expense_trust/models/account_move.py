from odoo import models, fields, api,_

class AccountMove(models.Model):
    _inherit = 'account.move'

    expense_id = fields.Many2one(comodel_name="hr.expense.sheet", string="Expenses",readonly=1)


class NewModule(models.Model):
    _inherit = 'sale.order'

    expense_rec_ids = fields.One2many(comodel_name="expense.sales", inverse_name="saleorder_id",)
    total_expense = fields.Float(string="Total", )

    def compute_total_expenses(self):
        print("FFFFFFFFFFFFFFFFFF")
        total = 0.0
        lines = [(5, 0, 0), ]

        for res in self.env['hr.expense'].search([('sale_order2', '=', self.id)]):
            total += res.total_amount

            lines.append((0, 0, {
                'product_id': res.product_id.id,
                'total_amount': res.total_amount,
                'name': res.name,
            }))
        self.total_expense = total
        self.update({'expense_rec_ids': lines})

class NewModule(models.Model):
    _name = 'expense.sales'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    total_amount = fields.Float(string="Total", required=False, )
    saleorder_id = fields.Many2one(comodel_name="sale.order",)

