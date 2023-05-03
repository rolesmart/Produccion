# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HideMenuUser(models.Model):
    _inherit = 'res.users'

    # Modificado por Staff 03/05/23
    # @api.model
    # def create(self, vals):
    #    self.clear_caches()
    #    return super(HideMenuUser, self).create(vals)
    
    @api.model_create_multi
    def create(self, vals_list):
        self.clear_caches()
        return super(HideMenuUser, self).create(vals_list)


    def write(self, vals):
        res = super(HideMenuUser, self).write(vals)
        for menu in self.hide_menu_ids:
            menu.write({
                'restrict_user_ids': [(4, self.id)]
            })
        self.clear_caches()
        return res

    def _get_is_admin(self):
        for rec in self:
            rec.is_admin = False
            if rec.id == self.env.ref('base.user_admin').id:
                rec.is_admin = True

    hide_menu_ids = fields.Many2many('ir.ui.menu', string="Menu", store=True)
    is_admin = fields.Boolean(compute=_get_is_admin)

class RestrictMenu(models.Model):
    _inherit = 'ir.ui.menu'
    restrict_user_ids = fields.Many2many('res.users')
