# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, api, _
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('request_date_from')
    def _check_leave_limit(self):
        for req in self:
            if req.holiday_status_id.flag_monthly_limit:
                leave_ids = self.env['hr.leave'].search(
                    [('employee_id', '=', req.employee_id.id),
                     ('holiday_status_id', '=', req.holiday_status_id.id),
                     ('state', '=', 'validate')])
                if leave_ids:
                    current_leave_date = req.request_date_from
                    current_leave_year = int(current_leave_date.year)
                    current_leave_month = int(current_leave_date.month)
                    leave_days = 0.00
                    remaining = 0.00
                    for leave in leave_ids:
                        leave_date = leave.request_date_from
                        year = int(leave_date.year)
                        month = int(leave_date.month)
                        if year == current_leave_year and \
                                        month == current_leave_month:
                            leave_days += leave.number_of_days_display
                    remaining = req.holiday_status_id.leave_limit_days - \
                                float(leave_days)
                    if float(req.number_of_days_display) > float(remaining):
                        raise ValidationError(
                            _("You Monthly Leave Limit is : %s\nYou have "
                              "already taken %s leaves in this month\nNow your "
                              "remaining leaves are :  %s") %
                            (req.holiday_status_id.leave_limit_days,
                             float(leave_days),
                             float(remaining)))

    def write(self, values):

        # is_officer = self.env.user.has_group('hr_holidays.group_hr_holidays_user')

        # if not is_officer:
        #     if any(hol.date_from.date() < fields.Date.today() for hol in self):
        #         raise UserError(_('You must have manager rights to modify/validate a time off that already begun'))

        employee_id = values.get('employee_id', False)
        if not self.env.context.get('leave_fast_create'):
            if values.get('state'):
                self._check_approval_update(values['state'])
                if any(holiday.validation_type == 'both' for holiday in self):
                    if values.get('employee_id'):
                        employees = self.env['hr.employee'].browse(values.get('employee_id'))
                    else:
                        employees = self.mapped('employee_id')
                    self._check_double_validation_rules(employees, values['state'])
            if 'date_from' in values:
                values['request_date_from'] = values['date_from']
            if 'date_to' in values:
                values['request_date_to'] = values['date_to']
        result = super(HolidaysRequest, self).write(values)
        if not self.env.context.get('leave_fast_create'):
            for holiday in self:
                if employee_id:
                    holiday.add_follower(employee_id)
                    self._sync_employee_details()
                if 'number_of_days' not in values and ('date_from' in values or 'date_to' in values):
                    holiday._onchange_leave_dates()
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: