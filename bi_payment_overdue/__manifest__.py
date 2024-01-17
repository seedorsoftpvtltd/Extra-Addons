# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
{
    'name': 'Customer Overdue Payments odoo',
    'category': 'Accounting',
    'version' : '14.0.0.0',
    'description': """
    Account overdue, payment overdue, Customer account payment overdue.

    Also shows the payment followup tab which show overdue balance and total amount overdue.
    Print Customer overdue payment, Send overdue payment by email.Calculate overdue balance based on Payment Terms also send payment reminder.Shows partner balance, customer balance, partner leadger, account follow-up.
BrowseInfo developed a new odoo/OpenERP module apps

overdue payment report
late payment report
cutomer late payment reports
delayed payment reports
overdue invoice report

payment overdue report
payments overdue report
    This module use for Print Customer Statement, Print Supplier Statement.Send Customer Statement by email.
    Also shows the payment followup tab which show overdue balance and total amount overdue.
    Print Customer overdue payment, Send overdue payment by email.Calculate overdue balance based on Payment Terms also send payment reminder.Shows partner balance, customer balance, partner leadger, account follow-up.Payment Warning, Payment Reminder.
    Print Customer Statement, Print Supplier Statement .Send Customer Statement by email. Send supplier statement by email .Account Statement,Partner statement, Balance Sheet, ledger Report, Print Account Statement, Accounting Reports, Statement Reports, Customer report, Balance Statement,Customer Balance Report, Customer ledger report, ledger balance.Credit Statement, Debit Statement.Customer Overdue statement.Accounting Statement, Creditor Reports, Debtor Reports.payment followup report, payment follow-up.
    Konto überfällig, Zahlung überfällig, Zahlung des Kundenkontos überfällig.
    Zeigt auch die Registerkarte Zahlungsnachverfolgung an, die überfälliges Guthaben und überfälligen Gesamtbetrag anzeigen.
    Drucken Überfällige Kundenzahlung, Überfällige Zahlung per E-Mail senden.Berechnen des überfälligen Guthabens basierend auf den Zahlungsbedingungen sowie Senden einer Zahlungserinnerung. Zeigt das Partner-Guthaben, den Kundensaldo, den Partner-Leadger, die Kontobewegung.
BrowseInfo entwickelte ein neues odoo / OpenERP Modul Apps
    Dieses Modul verwenden Sie für Print Customer Statement, Drucken Supplier Statement.Send Customer Statement per E-Mail.
    Zeigt auch die Registerkarte Zahlungsnachverfolgung an, die überfälliges Guthaben und überfälligen Gesamtbetrag anzeigen.
    Drucken Überfällige Kundenzahlung, Überfällige Zahlung per E-Mail senden. Überfälliges Guthaben basierend auf den Zahlungsbedingungen berechnen, außerdem eine Zahlungserinnerung senden. Zeigt das Partner-Guthaben, den Kundensaldo, den Partner-Leadger, die Kontobewegung, die Zahlungswarnung und die Zahlungserinnerung an.
    Kundenerklärung drucken, Lieferantenerklärung drucken. Kundenerklärung per E-Mail senden. Versenden Sie die Lieferantenerklärung per E-Mail. Kontoauszug, Partnererklärung, Bilanz, Hauptbuchbericht, Kontoauszug drucken, Kontoauszug, Kontoauszug, Kundenbericht, Kontoauszug, Kontoauszug, Debitorenbuchhaltung, Kontostand. Kreditnachweis, Sollauszug .Customer Überfällige Anweisung. Accounting-Anweisung, Creditor Reports, Debtor Reports.Payment Followup-Bericht, Zahlung Follow-up.

Compte en retard, paiement en retard, paiement du compte client en retard.
    Affiche également l'onglet Suivi des paiements qui indique le solde en souffrance et le montant total en retard.
    Imprimer le paiement en retard du client, envoyer le paiement en retard par e-mail.Calculer solde en souffrance basé sur les termes de paiement envoyer également rappel de paiement.Affiche solde partenaire, solde client, partenaire partenaire, suivi du compte.
BrowseInfo a développé un nouveau module odoo / OpenERP
    Ce module est utilisé pour Imprimer la déclaration du client, Imprimer la déclaration du fournisseur. Envoyer la déclaration du client par courrier électronique.
    Affiche également l'onglet Suivi des paiements qui indique le solde en souffrance et le montant total en retard.
    Imprimer le paiement en retard du client, envoyer le paiement en retard par e-mail.Calculer solde en souffrance basé sur les termes de paiement envoyer également rappel de paiement.Affiche solde du partenaire, solde client, partenaire partenaire, suivi du compte.Avertissement de paiement, rappel de paiement.
    Imprimer la déclaration du client, imprimer la déclaration du fournisseur .Envoyer la déclaration du client par courriel. Envoyer la déclaration du fournisseur par e-mail. Relevé de compte, relevé de partenaire, bilan, relevé de compte, relevé de compte, rapports de comptabilité, relevés de compte, rapport client, relevé de solde, relevé de solde client, relevé de grand livre. .Compte client en retard. Relevé de compte, rapports de créancier, rapports de débiteur, rapport de suivi de paiement, suivi des paiements.

Cuenta vencida, retraso en el pago, vencimiento del pago de la cuenta del cliente.
    También muestra la pestaña de seguimiento de pagos que muestra el saldo vencido y la cantidad total vencida.
    Imprima el pago vencido del cliente, envíe el pago vencido por correo electrónico. Calcule el saldo vencido en función de las condiciones de pago y envíe un recordatorio de pago. Muestra el saldo del socio, el saldo del cliente, el marcador del socio y el seguimiento de la cuenta.
BrowseInfo desarrolló un nuevo módulo odoo / OpenERP
    Este módulo se utiliza para Imprimir la declaración del cliente, Imprimir la declaración del proveedor. Enviar la declaración del cliente por correo electrónico.
    También muestra la pestaña de seguimiento de pagos que muestra el saldo vencido y la cantidad total vencida.
    Imprima el pago vencido del cliente, envíe el pago vencido por correo electrónico. Calcule el saldo vencido basado en las condiciones de pago y envíe un recordatorio de pago. Muestra el saldo del socio, el saldo del cliente, el interlocutor, el seguimiento de la cuenta. Aviso de pago, recordatorio de pago.
    Imprima la declaración del cliente, imprima la declaración del proveedor. Envíe la declaración del cliente por correo electrónico. Enviar declaración de proveedor por correo electrónico. Declaración de cuenta, declaración de socio, balance, informe de contabilidad, estado de cuenta de impresión, informes de contabilidad, informes de cuenta, informe de cliente, estado de cuenta, informe de saldo de cliente, informe de contabilidad de clientes, saldo de libro mayor. Declaración de crédito, declaración de débito . Declaración vencida del cliente. Estado contable, informes de acreedores, informes de deudor. Informe de seguimiento de pagos, seguimiento de pagos.

Achterstallig account, te late betaling, achterstallige betaling klantaccount.
    Toont ook het tabblad met de betalingsupdates dat het achterstallige saldo en het totale achterstallige bedrag laat zien.
    Afdrukken Achterstallige betaling van klant, achterstallige betaling per e-mail verzenden. Bereken achterstallige saldo op basis van betalingsvoorwaarden ook betalingsherinnering. Toon partnerbalans, klantensaldo, partner leadger, account follow-up.
BrowseInfo heeft een nieuwe odoo / OpenERP-module-apps ontwikkeld
    Deze module wordt gebruikt voor Print Customer Statement, Print Supplier Statement. Stuur de klantverklaring per e-mail.
    Toont ook het tabblad met de betalingsupdates dat het achterstallige saldo en het totale achterstallige bedrag laat zien.
    Afdrukken Achterstallige betaling van klant, achterstallige betaling per e-mail verzenden. Bereken achterstallige saldo op basis van betalingsvoorwaarden ook betalingsherinnering. Toont partnerbalans, klantensaldo, partner leadger, account-follow-up. Betalingswaarschuwing, betalingsherinnering.
    Klantverklaring afdrukken, Leverancierverklaring afdrukken. Stuur de klantverklaring per e-mail. Verzend de leveranciersverklaring per e-mail. Accounting, partnerafschrift, balans, grootboekrapport, afdrukrekeningoverzicht, boekhoudrapporten, overzichtsrapporten, klantrapport, balansoverzicht, klantensaldo-rapport, klantgrootboek, grootboeksaldo. Credit Statement, debetoverzicht . Klant achterstallige verklaring. Accountingafrekening, crediteurenrapporten, debiteurenrapporten. Follow-upverslag, betalingsreparatie.

Konto überfällig, Zahlung überfällig, Zahlung des Kundenkontos überfällig.
    Zeigt auch die Registerkarte Zahlungsnachverfolgung an, die überfälliges Guthaben und überfälligen Gesamtbetrag anzeigen.
    Drucken Überfällige Kundenzahlung, Überfällige Zahlung per E-Mail senden.Berechnen des überfälligen Guthabens basierend auf den Zahlungsbedingungen sowie Senden einer Zahlungserinnerung. Zeigt das Partner-Guthaben, den Kundensaldo, den Partner-Leadger, die Kontobewegung.
BrowseInfo entwickelte ein neues odoo / OpenERP Modul Apps
    Dieses Modul verwenden Sie für Print Customer Statement, Drucken Supplier Statement.Send Customer Statement per E-Mail.
    Zeigt auch die Registerkarte Zahlungsnachverfolgung an, die überfälliges Guthaben und überfälligen Gesamtbetrag anzeigen.
    Drucken Überfällige Kundenzahlung, Überfällige Zahlung per E-Mail senden. Überfälliges Guthaben basierend auf den Zahlungsbedingungen berechnen, außerdem eine Zahlungserinnerung senden. Zeigt das Partner-Guthaben, den Kundensaldo, den Partner-Leadger, die Kontobewegung, die Zahlungswarnung und die Zahlungserinnerung an.
    Kundenerklärung drucken, Lieferantenerklärung drucken. Kundenerklärung per E-Mail senden. Versenden Sie die Lieferantenerklärung per E-Mail. Kontoauszug, Partnererklärung, Bilanz, Hauptbuchbericht, Kontoauszug drucken, Kontoauszug, Kontoauszug, Kundenbericht, Kontoauszug, Kontoauszug, Debitorenbuchhaltung, Kontostand. Kreditnachweis, Sollauszug .Customer Überfällige Anweisung. Accounting-Anweisung, Creditor Reports, Debtor Reports.Payment Followup-Bericht, Zahlung Follow-up.


""",
    'author': 'BrowseInfo',
    'summary': 'Apps for print customer statement report print vendor statement payment reminder customer payment followup send customer statement print account statement reports print overdue statement reports send overdue statement print supplier statement reports',
    'website': 'https://www.browseinfo.in',
    'price': 29,
    'currency': "EUR",
    'depends': ['base', 'account', 'sale_management', 'mail', 'sales_team'],
    
    'data': [
            'views/overdue_report.xml',
             'views/report.xml',
             'data/overdue_mail_data.xml',
             'views/account_invoice_view.xml',
             'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "live_test_url":'https://youtu.be/DuMt9in_RaE',
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
