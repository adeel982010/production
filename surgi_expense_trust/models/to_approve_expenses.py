from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

class HRExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('traged', 'Treasury'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True,
        help='Expense Report State')
    # state = fields.Selection(selection_add=[('traged', 'Traged')])

    trust_id = fields.Many2one(comodel_name="hr.expense", string="Trust" )

    def action_sheet_traged(self):
        self.state='traged'

    def action_sheet_move_create(self):
        if any(sheet.state != 'traged' for sheet in self):
            raise UserError(_("You can only generate accounting entry for treasury expense(s)."))

        if any(not sheet.journal_id for sheet in self):
            raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

        expense_line_ids = self.mapped('expense_line_ids')\
            .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
        res = expense_line_ids.action_move_create()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",res,self.account_move_id)
        self.account_move_id.expense_id=self.id

        if not self.accounting_date:
            self.accounting_date = self.account_move_id.date

        if self.payment_mode == 'own_account' and expense_line_ids:
            self.write({'state': 'post'})
        else:
            self.write({'state': 'done'})
        self.activity_update()
        return res

    @api.model
    def filters_employee_treasury(self):
        print("ssssssssssssssssssssssssssssssssssssssssssssssssssss")

        list_obj = []
        for rec in self.env['hr.expense.sheet'].search([]):
            if rec.state=='traged':
                if rec.employee_id.treasury_id.id == self.env.user.employee_id.treasury_id.id:
                    list_obj.append(rec.id)
                    print(rec.employee_id.name)
        return {
            'name': _('Accounting Overview'),
            'res_model': 'hr.expense.sheet',
            'view_mode': 'tree,form',
            # 'view_id': '',
            'domain': [('id', 'in', list_obj)],
            'type': 'ir.actions.act_window',
        }


class HRExpense(models.Model):
    _inherit = 'hr.expense'

    expense_report_ids = fields.Many2many(comodel_name="hr.expense.sheet",)
    is_expense_report = fields.Boolean(string="Get Trust",  )

    trust_net = fields.Float(string="Trust Net",compute='compute_expense_report_total',store=True)#compute='compute_expense_report',store=True,
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact",)
    event_id = fields.Many2one(comodel_name="event.event", string="Event",)
    is_trust = fields.Boolean(related='product_id.name_1222' )

    sale_order2 = fields.Many2one(comodel_name="sale.order", string="SaleOrder", )
    is_expenses = fields.Boolean(string="", store=True, compute='compute_is_expenses')

    @api.depends('product_id')
    def compute_is_expenses(self):
        for rec in self:
            rec.is_expenses = rec.product_id.is_expenses

    # @api.depends('is_expense_report')
    def compute_expense_report(self):
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        # for res in self:
        lines = []
        # if s.is_expense_report==True:
        for rec in self.env['hr.expense.sheet'].search([('trust_id','=',self.id)]):
            print("11111111111111111111111111111111")
            lines.append(rec.id)
        self.update({'expense_report_ids':lines,})

    @api.model
    def filters_employee_work_location(self):
        print("ssssssssssssssssssssssssssssssssssssssssssssssssssss")


        list_obj = []
        for rec in self.env['hr.expense'].search([]):
            if rec.employee_id.work_location_id.id == self.env.user.employee_id.work_location_id.id:
                list_obj.append(rec.id)
                print(rec.employee_id.name)
        return {
            'name': _('Accounting Overview'),
            'res_model': 'hr.expense',
            'view_mode': 'tree,form',
            # 'view_id': '',
            'domain': [('id', 'in', list_obj)],
            'type': 'ir.actions.act_window',
        }

    # @api.model
    # def action_journal_entry(self):
    #     # """
    #     # this function used in server actions.
    #     # :return: journals that current user have access right on it.
    #     # """
    #     # journals = []
    #     #
    #     # for rec in self.env['account.journal'].search([]):
    #     #     if self.env.user in rec.users_ids:
    #     #         journals.append(rec.id)
    #
    #     return {
    #         'name': _('Accounting Overview'),
    #         'res_model': 'account.journal',
    #         'view_mode': 'kanban',
    #         'view_id': self.env.ref('account.account_journal_dashboard_kanban_view').id,
    #         'domain': [('id', 'in', journals)],
    #         'type': 'ir.actions.act_window',
    #     }




    @api.depends('expense_report_ids','unit_amount')
    def compute_expense_report_total(self):
        for res in self:
            total=0.0
            for rec in self.expense_report_ids:
                total+=rec.total_amount
            print(total,'111111111111111111')
            if total>0:
                res.trust_net=res.unit_amount-total
            else:
                res.trust_net = res.unit_amount


    def action_submit_expenses(self):
        if any(expense.state != 'draft' or expense.sheet_id for expense in self):
            raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('employee_id')) != 1:
            raise UserError(_("You cannot report expenses for different employees in the same report."))
        if any(not expense.product_id for expense in self):
            raise UserError(_("You can not create report without product."))

        todo = self.filtered(lambda x: x.payment_mode=='own_account') or self.filtered(lambda x: x.payment_mode=='company_account')

        # print("TTTTTTTTTTTTTTTTTTTTTTTTTT",todo,expense)
        # todo.

        return {
            'name': _('New Expense Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'context': {
                'default_expense_line_ids': todo.ids,
                # 'default_trust_id': todo.id,
                'default_company_id': self.company_id.id,
                'default_employee_id': self[0].employee_id.id,
                'default_name': todo[0].name if len(todo) == 1 else ''
            }
        }
