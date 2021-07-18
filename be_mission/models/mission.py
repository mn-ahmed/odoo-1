# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import Warning, UserError
from odoo.addons import decimal_precision as dp


class MissionExterne(models.Model):
    _name = 'mission.externe'
    _description = 'Mission Externe'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    date = fields.Date(
        string='Date',
        default=fields.Date.today(),
        required=True, readonly=True)
    person_name = fields.Many2one(
        'res.partner', string="Nom et Prénom", required=True)
    employee_id = fields.Many2one('hr.employee', string='Employée',
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True)
    date_depart = fields.Date(
        string='Date de départ', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expiration', required=False)

    date_arriver = fields.Date(
        string='Date d\'arrivéé', default=fields.Date.context_today, store=True, required=False)

    passport = fields.Char(string='Numéro de Passport', required=False)
    objet = fields.Text(string="Objet Mission", required=False)

    visa = fields.Selection(string='Visa', selection=[('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_visa = fields.Date(string='Date', required=False)
    l_invitation = fields.Selection(string='Lettre d\'invitation', selection=[
        ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_lettre = fields.Date(
        string='Date',
        required=False)

    post_v = fields.Char(string='Fonction voyageur', required=False)
    chauffeur = fields.Boolean(string='Chauffeur', required=False)
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.', required=False)
    responsable = fields.Char(string='Nom personne ressource', required=False)
    post = fields.Char(string='Fonction personne ressource', required=False)

    test_ca = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )

    date_ca = fields.Date(string='Date de test covid', required=False)

    test_cd = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )

    date_cd = fields.Date(string='Date de test covid', required=False)

    hotel = fields.Char(string='Nom de Hotel', required=False)
    duree_s = fields.Char(string='Duree de séjour', required=False)
    duree_h = fields.Char(string='Duree de séjour hotel', required=False)
    autres = fields.Char(
        string='Autres', 
        required=False)
    commentaire = fields.Text(
        string="Commentaire",
        required=False)

    frais_h = fields.Selection(string='Frais de hotel', selection=[(
        'employee', 'Employée'), ('webb', 'Webb Fentaine'),('autres', 'Autres')], required=False, )

    point_equi = fields.Text(string='Point Equipement', required=False)
    satisfact = fields.Selection(string='Satisfaction', selection=[('mauv', 'Mauvaise'),
                                                                   ('pass',
                                                                    'Passable'),
                                                                   ('a_bien',
                                                                    'Assez-bien'),
                                                                   ('bien',
                                                                    'Bien'),
                                                                   ('t_bien',
                                                                    'Trés-bien'),
                                                                   ('excel', 'Excelente'), ], required=False, )

    state = fields.Selection([
        ('draft', 'Nouveau'),
        ('arriver', 'Arriver'),
        ('depart', 'Départ'),
        ('terminer', 'Terminer'),
        ('cancel', 'Annuler')],
        default='draft',
        track_visibility='onchange',)
        

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mission.externe') or _('Nouveau')
        res = super(MissionExterne, self).create(vals)
        return res

    def action_arriver(self):
        for rec in self:
            rec.state = 'arriver'

    def action_depart(self):
        for rec in self:
            rec.state = 'depart'

    def action_terminer(self):
        for rec in self:
            rec.state = 'terminer'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class MissionInterne(models.Model):
    _name = 'mission.interne'
    _description = 'Mission Interne'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    date = fields.Date(
        string='Date',
        default=fields.Date.today(),
        required=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employée', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True)
    date_depart = fields.Date(
        string='Date de départ', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expiration', required=False)

    date_retour = fields.Date(
        string='Date de Retour', default=fields.Date.context_today, store=True, required=False)


    passport = fields.Char(string='Numéro de Passport', required=False)
    objet = fields.Text(string="Objet Mission", required=False)
    o_mission = fields.Selection(string='Ordre de mission', selection=[
                                 ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_mission = fields.Date(
        string='Date de mission',
        required=False)
    billet = fields.Selection(string='Achat Billet d\'avion', selection=[
                              ('oui', 'Oui'), ('non', 'Non')], required=False, )
    visa = fields.Selection(string='Visa', selection=[('oui', 'Oui'), ('non', 'Non')], required=False)
    date_visa = fields.Date(string='Date', required=False)

    l_invitation = fields.Selection(string='Lettre d\'invitation', selection=[
                                    ('oui', 'Oui'), ('non', 'Non')], required=False, )

    date_lettre = fields.Date(string='Date',  required=False)

    vehicule = fields.Selection(string='Besoin de véhicule?', selection=[
                                ('oui', 'Oui'), ('non', 'Non')], required=False, )
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.', required=False)
    responsable = fields.Char(string='Nom de Responsable', required=False)
    post = fields.Char(string='Post de responsable', required=False)

    test_cr = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )
    date_cr = fields.Date(string='Date de test covid', required=False)

    test_cd = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )
    date_cd = fields.Date(string='Date de test covid', required=False)

    frais_m = fields.Selection(string='Frais de Mission', selection=[
                               ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_f = fields.Date(string='Date de frais de mission', required=False)
    p_financier = fields.Selection(string='Point financier?', selection=[
                                   ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_pf = fields.Date(string='Date point financier', required=False)
    commentaire = fields.Text(
        string="Commentaire",
        required=False)

    state = fields.Selection([
        ('draft', 'Nouveau'),
        ('depart', 'Départ'),
        ('retour', 'Retour'),
        ('terminer', 'Terminer'),
        ('cancel', 'Annuler')],
        default='draft',
        track_visibility='onchange', )

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mission.interne') or _('Nouveau')
        res = super(MissionInterne, self).create(vals)
        return res

    def action_depart(self):
        for rec in self:
            rec.state = 'depart'

    def action_retour(self):
        for rec in self:
            rec.state = 'retour'

    def action_terminer(self):
        for rec in self:
            rec.state = 'terminer'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class MissionOrdinaire(models.Model):
    _name = 'mission.ordinaire'
    _description = 'Mission Ordinaire'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Service Number', copy=False, default="Nouveau")
    date = fields.Date(
        string='Date',
        default=fields.Date.today(),
        required=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employée',
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                                                      limit=1),
                                  required=True, copy=True)
    date_depart = fields.Date(
        string='Date de départ', default=fields.Date.context_today, store=True, required=False)
    date_exp = fields.Date(string='Date d\'expiration', required=False)

    date_retour = fields.Date(
        string='Date de Retour', default=fields.Date.context_today, store=True, required=False)

    passport = fields.Char(string='Passeport/CIN', required=False)
    objet = fields.Text(string="Objet Mission", required=False)
    o_mission = fields.Selection(string='Ordre de mission', selection=[
                                 ('oui', 'Oui'), ('non', 'Non')], required=False, )

    date_mission = fields.Date(
        string='Date de mission',
        required=False)
    p_carburant = fields.Selection(string='Carburant', selection=[
        ('oui', 'Oui'), ('non', 'Non')], required=False, )

    date_p_carburant = fields.Date(
        string='Date',
        required=False)

    vehicule = fields.Selection(string='Besoin de véhicule?', selection=[
                                ('oui', 'Oui'), ('non', 'Non')], required=False, )
    n_chauffeur = fields.Char(string='Nom de Chauffeur', required=False)
    chauffeur_cont = fields.Char(string='Contact de Chauffeur', required=False)
    matricule = fields.Char(string='Matricule de Véhicule', required=False)
    duree_b = fields.Char(string='Durée d\'util. de Véhi.', required=False)
    responsable = fields.Char(string='Nom de Responsable', required=False)
    post = fields.Char(string='Post de responsable', required=False)

    test_cr = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )
    date_cr = fields.Date(string='Date de test covid', required=False)

    test_cd = fields.Selection(string='Test COVID', selection=[(
        'oui', 'Oui'), ('non', 'Non')], required=False, )
    date_cd = fields.Date(string='Date de test covid', required=False)

    frais_m = fields.Selection(string='Frais de Mission', selection=[
                               ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_f = fields.Date(string='Date de frais de mission', required=False)
    p_financier = fields.Selection(string='Point financier?', selection=[
                                   ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_pf = fields.Date(string='Date point financier', required=False)

    equipement = fields.Selection(string='Equipement?', selection=[
        ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_eq = fields.Date(string='Date point financier', required=False)

    p_equipement = fields.Selection(string='Point Equipement?', selection=[
        ('oui', 'Oui'), ('non', 'Non')], required=False, )
    date_p_eq = fields.Date(string='Date point Equipement', required=False)

    commentaire_dep = fields.Text(
        string="Commentaire",
        required=False)
    commentaire_ret = fields.Text(
        string="Commentaire",
        required=False)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mission.ordinaire') or _('Nouveau')
        res = super(MissionOrdinaire, self).create(vals)
        return res

    state = fields.Selection([
        ('draft', 'Nouveau'),
        ('depart', 'Départ'),
        ('retour', 'Retour'),
        ('terminer', 'Terminer'),
        ('cancel', 'Annuler')],
        default='draft',
        track_visibility='onchange', )

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'mission.ordinaire') or _('Nouveau')
        res = super(MissionOrdinaire, self).create(vals)
        return res

    def action_depart(self):
        for rec in self:
            rec.state = 'depart'

    def action_retour(self):
        for rec in self:
            rec.state = 'retour'

    def action_terminer(self):
        for rec in self:
            rec.state = 'terminer'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class ReportingTicket(models.Model):
    _name = 'reporting.ticket'
    _description = 'reporting ticket'
    _rec_name = 'name'
    _order = 'name ASC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True,
                       default=lambda self: _('New'), copy=False)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    employee_id = fields.Many2one('hr.employee', string='Employée', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
                                  required=True, copy=True)

    date_v = fields.Date(string='Date de Voyage', store=True, required=False)
    date_r = fields.Date(string='Date retour', required=False)
    trajet = fields.Char(string='Trajet', Required=False)
    nature = fields.Char(string='Nature', required=False)
    montant_b = fields.Float(string='Montant Billet',digits=(12,2))
    montant_bm = fields.Float(string='Montant Billet modifié', digits=(12,2))
    montant_bmt = fields.Float(string='Montant Billet modifié (Trajet)', digits=(12,2))

    montant_total = fields.Float(compute='_compute_montant_total', string='Montant total', digits = (12,2))

    @api.depends('montant_b', 'montant_bm', 'montant_bmt')
    def _compute_montant_total(self):
        for record in self:
            montant_total = 0.0
            montant_b = record.montant_b
            montant_bm = record.montant_bm
            montant_bmt = record.montant_bmt
            record.update({
                'montant_total': record.currency_id.round(montant_b) + record.currency_id.round(montant_bm) + record.currency_id.round(montant_bmt)
            })

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'reporting.ticket') or _('Nouveau')
        res = super(ReportingTicket, self).create(vals)
        return res

