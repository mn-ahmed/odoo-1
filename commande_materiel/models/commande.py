# -*- coding: utf-8 -*-
import ipaddress

from odoo import models, fields, api, tools, _
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
from odoo.exceptions import Warning, UserError


class CommandeMateriel(models.Model):
    _name = 'commande.materiel'
    _description = 'commande materiel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'annuler', 'rejeter'):
                raise Warning(
                    _('Vous ne pouvez pas supprimer une demande qui n\'est pas à l\'état de brouillon ou d\'annulation ou de rejet..'))
        return super(CommandeMateriel, self).unlink()

    name = fields.Char('Commande Numéro', copy=False, default="Nouveau", readonly=True)
    date = fields.Date(string='Date',
                       default=fields.Date.today(),
                       required=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employée',
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True)
    department_id = fields.Many2one('hr.department',
                                    string='Department',
                                    required=True,
                                    copy=True,)
    employee_confirme_par_id = fields.Many2one('hr.employee',
                                          string='Confirmer par',readonly=True,
                                          copy=False)
    employee_accepter_par_id = fields.Many2one('hr.employee',
                                               string='Accepter par', readonly=True,
                                               copy=False)
    employee_rejeter_par_id = fields.Many2one('hr.employee',
                                              string='Rejeter par',
                                              readonly=True,
                                              copy=False, )
    employee_aprouver_par_id = fields.Many2one('hr.employee',
                                              string='Approuver par',
                                              readonly=True,
                                              copy=False, )
    date_confirm = fields.Date(
        string='Date de Confirmation',
        readonly=True,
        copy=False,
    )
    date_accept = fields.Date(
        string='Date d\'Acceptation',
        readonly=True,
        copy=False,
    )
    date_reject = fields.Date(
        string='Date de Rejet',
        readonly=True,
    )
    date_appr = fields.Date(
        string='Date d\'Approbation',
        readonly=True,
        copy=False,
    )
    date_recep = fields.Date(
        string='Date de Réception',
        readonly=True,
        copy=False,
    )
    commande_line_ids = fields.One2many('commande.materiel.line',
                                            'commande_id',
                                            string='Lignes des Commandes',
                                            copy=True,)
    commentaire = fields.Text('commentaire', required=False)
    raison = fields.Text('Raison', required=False)
    satisfaction = fields.Selection(string='Satisfaction',
                                    selection=[('satisfait', 'Satisfait'),
                                               ('non_satisfait', 'Non Satisfait')],
                                    required=False, )

    state = fields.Selection([('draft', 'Nouveau'),
                                ('en_cours', 'En Cours Départ.'),
                                ('accepter','Accepter'),
                                ('approuver', 'Approuver'),
                                ('rejeter', 'Rejeter'),
                                ('recu', 'Reçu'),
                                ('annulee', 'Annuler')],
                             default='draft',
                             track_visibility='onchange', )

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('commande.materiel.seq')
        vals.update({
            'name': name
        })
        res = super(CommandeMateriel, self).create(vals)
        return res

    @api.onchange('employee_id')
    def set_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.sudo().department_id.id

    # confirm button
    def confirme_user(self):
        for rec in self:
            rec.employee_confirme_par_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.date_confirm = fields.Date.today()
            rec.state = 'en_cours'

    def confirme_depart(self):
        for rec in self:
            current_user = rec.env.user
            if rec.department_id.manager_id.user_id == current_user:
                rec.date_accept = fields.Date.today()
                rec.employee_accepter_par_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                rec.state = 'accepter'
            else:
                raise Warning(
                    _('Vous n\'êtes pas autorisé de passer cette action !! Veuillez connecter avec un autre utilisateur'))

    def confirme_manager(self):
        for rec in self:
            current_user = rec.env.user
            if rec.env.user.has_group('commande_materiel.group_commande_materiel_daf') or rec.employee_id.user_id != current_user:
                rec.date_appr = fields.Date.today()
                rec.employee_aprouver_par_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
                rec.state = 'approuver'
            else:
                raise Warning(
                    _('Désolé mais vous ne pouvez pas approuver votre propre demande'))

    def recu_user(self):
        for rec in self:
            user = rec.env.user
            if rec.employee_id.user_id == user or rec.department_id.manager_id.user_id == user:
                rec.date_recep = fields.Date.today()
                rec.state = 'recu'
            else:
                raise Warning(
                    _('Vous n\'êtes pas autorisé de passer cette action !! Veuillez connecter avec un autre utilisateur'))

    def reject_commande(self):
        for rec in self:
            rec.state = 'rejeter'

    def annulee_commande(self):
        for rec in self:
            rec.state = 'annuler'


class CommandeMaterielLine(models.Model):
    _name = "commande.materiel.line"
    _description = 'Commande Materie Lines'

    commande_id = fields.Many2one('commande.materiel', string='Commande',)
    product_id = fields.Many2one('product.product',
                                 string='Product',
                                )
    description = fields.Char(string='Description', required=True,)
    qty = fields.Float(string='Quantity', default=1, required=True,)
    uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True,)
    commande_type = fields.Selection(selection=[('internal', 'Internal Picking'),
                                                ('purchase', 'Purchase Order'),],
                                     string='Requisition Action',)

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            if rec.product_id:

                rec.description = rec.product_id.name
                rec.uom = rec.product_id.uom_id.id

