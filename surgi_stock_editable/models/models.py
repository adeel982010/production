from odoo import models, fields, api,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError



# '|',('company_id', '=', company_id),(company_id, 'in', 'zzallowed_companiess.ids')


class NewModule(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('product_id','lot_id','location_dest_id')
    def filter_lot_id(self):
        domain = "[('product_id', '=', parent.product_id),]"
        for rec in self:
            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            lines=[]
            for lot in self.env['stock.production.lot'].search([('product_id','=',rec.picking_id.product_id.id)]):
                if self.env.user.company_id ==lot.company_id or self.env.user.company_id in lot.allowed_companies.ids:
                    lines.append(lot.id)
            print(lines,'33333333333333333333333')
            return{
                'domain': {'lot_id': [('id', 'in', lines)]}

            }

    @api.constrains('lot_id', 'product_id')
    def _check_lot_product(self):
        for line in self:
            pass
            # if 1!=1:
            #     raise ValidationError(_('This lot %s is incompatible with this product %s'))


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'


    company_id = fields.Many2one('res.company', 'Company', required=False, stored=False, index=False)
    # allowed_companies = fields.Many2one('res.company', 'Allowed Companies',)
    allowed_companies = fields.Many2many(comodel_name="res.company",string="Allowed Companies", )

    _sql_constraints = [
        ('name_ref_uniq', 'check(1=1)', 'The combination of serial number and product must be unique across a company !'),
    ]



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

