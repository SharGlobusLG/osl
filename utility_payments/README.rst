========================
OSL - Odoo School Lesson
========================

UP - Utility Payments
===========

Module capabilities
-------------------
* Payment types linked to a service catalog.
* Recurring payment template for each apartment.
* Document for recording charges over a given period (with an auto-fill option based on the template).
* Payment record document (with an auto-fill option based on outstanding balances).

Installation
============
To install this module, you need to:

#. Clone repository.
#. Add the repository path to the config file.
#. Update the app list.
#. Install the module.

Authors
-------

* Volodymyr A.

Website
-------

* https://odoo.school/


WORK-MAP
--------

=================== =============================== ====================================================================
Requirement         Where                           What exactly
=================== =============================== ====================================================================
Процесна модель     up_charge.py                    стани draft → approved, переходи кнопками
pivot,graph,
kanban, search      up_charge_view.xml              Різні типи представлений для аналізу
Меню                up_menu.xml                     2 розділи для довідників та документів
Наслідування 1      up_product.py                   Наслідуються від моделі product.product
Наслідування 2      up_custom_external_template.xml Наслідується шаблон external_layout
Візард              up_generate_period_wizard.py    Автоматичне заповнення моделі up.period із контролем унікальності
Звіти               up_payment_report.xml           Документ оплати з усіма рядками
Демо-дані           utility_payments/demo/*         Демо дані для всіх моделей
Права доступу       up_groups.xml                   Група для доступу лише до своїх платежів
Документація        index.html                      Короткий опис модуля
=================== =============================== ====================================================================


Інваріант предметної області
----------------------------
Облік нарахувань та оплат завжди ведеться у розрізі періодів нарахувань.
Таким чином, періоди ніколи не повинні дублюватися.
Для цього зроблений визард, який автоматично створює періоди і доданий контроль унікальності при записі.