from odoo import models, fields, api
class WorkLocation(models.Model):
    _name = 'work.locations'
    _rec_name = 'name'

    name = fields.Char()

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    work_location_id = fields.Many2one(comodel_name="work.locations", string="Work Location", required=False, )
    treasury_id = fields.Many2one(comodel_name="hr.employee", string="Treasury",)