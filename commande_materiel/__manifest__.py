# -*- coding: utf-8 -*-
{
    'name': "Commande MaterièlsL",

    'summary': """
        """,

    'description': """
        Module pour des commande de materiel interne par employéee
    """,

    'author': "Ahmed Mnasri",
    'website': "",
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['stock',
                'hr',
                ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/commande_sequence.xml',
        'views/commande.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
