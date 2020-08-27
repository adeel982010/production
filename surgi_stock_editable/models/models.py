from odoo import models, fields, api,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    company_id123 = fields.Many2one('res.company', string='Company')

    _sql_constraints = [
        ('name_ref_uniq', 'check(1=1)', 'The combination of serial number and product must be unique across a company !'),
    ]


    @api.onchange('company_id123')
    def send_company_id(self):
        if self.company_id123:
            self.company_id=self.company_id123


    def write(self, vals):
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        # return super(ProductionLot, self).write(vals)





    @api.constrains('name')
    def validation_constran(self):

        # for res in self:
        for rec in self.search([('id','!=',self.id)]):
            print('1111111111111111111111111111111111111111')
            if self.name==rec.name:
                raise UserError('The combination of serial number and product must be unique across a company !')

