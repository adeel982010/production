from odoo import models, fields, api,_
class ProductProduct(models.Model):
    _inherit = 'product.product'

    name_1222  = fields.Boolean(string="",compute='comput_nameproduct',store=True)#compute='comput_nameproduct',store=True,
    is_expenses = fields.Boolean(string="Operation Expenses", )

    @api.depends('default_code','name')
    def comput_nameproduct(self):
        print("################")
        for rec in self:
            if rec.default_code or rec.name:
                if '1222' in str(rec.default_code):
                    print("1111111111111111111111")
                    rec.name_1222 = True
                elif '1222' in str(rec.name):
                    rec.name_1222=True
                    print("222222222222222222222222222222")
                else:
                    rec.name_1222=False
            else:
                rec.name_1222 = False


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    is_expenses = fields.Boolean(string="Operation Expenses",  )