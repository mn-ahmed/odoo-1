# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models,api, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class ResPartner(models.Model):
    _inherit = 'res.partner'


    rccm = fields.Char(
        string='RCCM',
        required=False)
    ifu = fields.Char(
        string='numéro ifu',
        required=False)
    entreprise = fields.Boolean(
        string='Entreprise', 
        required=False)
    formulaire_ids = fields.One2many('project.task', 'partner_id', 'e-Formulaire')
    invest = fields.Selection(string='Investisseement',
                            selection=[('20', 'Investissement < 20'),
                                       ('500', 'Investissement < 500'),
                                       ('501', 'Investissement > 500')], default='20',
                            required=False, )
    cout = fields.Char(string='Coût', compute='_compute_cout', store=True, required=False)

    @api.depends('invest')
    def _compute_cout(self):
        for rec in self:
            if rec.invest == '20':
                rec.cout = '30.000 francs cfa'
            elif rec.invest == '500':
                rec.cout = '50.000 francs cfa'
            elif rec.invest == '501':
                rec.cout = '100.000 francs cfa'




