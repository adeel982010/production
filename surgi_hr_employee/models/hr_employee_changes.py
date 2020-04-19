from odoo import api
from odoo import fields
from odoo import models


class department_fields(models.Model):
    _inherit = 'hr.department'

    department_type = fields.Selection([('department', 'Main Department'), ('section', 'Section')], string='Type',
                                       translate=True)


class employee_fields(models.Model):
    _inherit = 'hr.employee'

    labor_linc_no = fields.Char(string="Labor Linc No.")
    id_from = fields.Char(string="ID From")
    military_status = fields.Selection(string="Military Status",
                                       selection=[('not applicable', 'Not Applicable'), ('postponed', 'Postponed'),
                                                  ('exempted', 'Exempted'), ('completed', 'Completed'),
                                                  ('current', 'Currently serving ')])
    military_number = fields.Char(string="Military Number")
    religion = fields.Selection(string="Religion",
                                selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Others')])
    social_ins_exist = fields.Boolean("Has Social Insurance")
    social_ins_no = fields.Integer(string="Soical Ins No.")
    social_ins_title = fields.Char(string="Social Job Title")
    medical_ins_exist = fields.Boolean("Has Medical Insurance")
    medical_company = fields.Selection(string="Medical Co.", selection=[('inaya', 'Inaya')])
    medical_number = fields.Integer(string="Medical No.")
    mi_date = fields.Date(string="Medical Insurance Date", help='Medical  Insurance Date')
    section_id = fields.Many2one('hr.department', string="Section", domain=[('department_type', '=', 'section')])
    full_employee_name = fields.Char(string="Full Name", translate=True)
    attendance_type = fields.Selection([('in_door', 'IN Door'), ('out_door', 'Out Door')], string='Attendance type')
    in_direct_parent_id = fields.Many2one('hr.employee', 'Indirect Manager')
    # age = fields.Integer(string="Age", compute="_calculate_age", readonly=True)
    start_date = fields.Date(string="Start Working At")
    edu_phase = fields.Many2one(comodel_name="hr.eg.education", string="Education")
    edu_school = fields.Many2one(comodel_name="hr.eg.school", string="School/University/Institute")
    edu_major = fields.Char(string="major")
    edu_grad = fields.Selection([('ex', 'Excellent'), ('vgod', 'Very Good'), ('god', 'Good'), ('pas', 'Pass')],
                                string="Grad")
    grad_year = fields.Date(string="Grad. Year")
    edu_note = fields.Text("Education Notes")
    # experience_y = fields.Integer(compute="_calculate_experience", string="Experience",
    #                               help="experience in our company", store=True)
    # experience_m = fields.Integer(compute="_calculate_experience", string="Experience monthes", store=True)
    # experience_d = fields.Integer(compute="_calculate_experience", string="Experience dayes", store=True)
    payrolled_employee = fields.Boolean("Payrolled Employee", track_visibility='onchange')
    employee_arabic_name = fields.Char(string="Arabic Name")
    private_num = fields.Char(string="Private Number ", required=False, )

    # bank_account_num = fields.Integer(string="Bank Account Number",)

    @api.constrains('in_direct_parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('Error! You cannot create recursive hierarchy of Employee(s).'))

    @api.onchange('section_id')
    def _onchange_department(self):
        self.parent_id = self.section_id.manager_id

    # @api.depends("birthday")
    # def _calculate_age(self):
    #     for emp in self.search([]):
    #         if emp.birthday:
    #             dob = datetime.strptime(emp.birthday, "%Y-%m-%d")
    #             emp.age = int((datetime.today() - dob).days / 365)
    #
    # @api.depends("start_date")
    # def _calculate_experience(self):
    #     for emp in self.search([]):
    #         if emp.start_date:
    #             date_format = '%Y-%m-%d'
    #             current_date = (datetime.today()).strftime(date_format)
    #             d1 = datetime.strptime(emp.start_date, date_format).date()
    #             d2 = datetime.strptime(current_date, date_format).date()
    #             r = relativedelta(d2, d1)
    #             emp.experience_y = r.years
    #             emp.experience_m = r.months
    #             emp.experience_d = r.days
    #
    #
    # @api.model
    # def _cron_employee_age(self):
    #     self._calculate_age()
    #
    # @api.model
    # def _cron_employee_exp(self):
    #     self._calculate_experience()


class dhn_hr__eg_education(models.Model):
    _name = "hr.eg.education"

    name = fields.Char(string="Education", translate=True)
    note = fields.Char(string="Note", required=False, )


class hr_eg_school(models.Model):
    _name = "hr.eg.school"

    name = fields.Char(string="School name", translate=True)
    note = fields.Char(string="Note", required=False, )

