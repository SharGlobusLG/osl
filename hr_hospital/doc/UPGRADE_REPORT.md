# Upgrade report

## 1 Prepare database

###  1.1 Create database via cli:

`createdb -U odoo -h localhost hospital_upgrade`

### 1.2  Init database and install HR Hospital

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -i hr_hospital --with-demo --stop-after-init`

### 1.3 Run Odoo and create new record by manual

List of added records:

3 records:  Patient with follow insurance numbers:  
	010101
	B-02
	C-03

4 records:  Apointment

1 record:   Doctor History

1 record:   Doctor

1 record:   Doctor Category

### 1.4 Make database dump: 

`pg_dump -U odoo -h localhost -Fc hospital_upgrade > before.dump`

## 2 Rename field insurance_policy_number

### 2.1 Rename without script

Data was lost for all patients.

For rollback run:

`sudo -u odoo pg_restore -v -d hospital_upgrade /home/odoo/odoo_dev/before.dump`


### 2.2 Rename with script ./pre-10-normalize-policy-number.py

For Update run:

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -u hr_hospital --stop-after-init`

We receive a success message

> 2026-11-24 11:38:17,071 19894 INFO hospital_upgrade odoo.modules.loading: loading 28 modules... 
>
> 2026-11-24 11:38:17,202 19894 INFO hospital_upgrade odoo.modules.loading: Loading module hr_hospital (25/28)
> 
> 2026-11-24 11:38:17,255 19894 INFO hospital_upgrade odoo.modules.migration: module hr_hospital: Running upgrade [>19.0.1.1.0] pre-10-rename-policy-number
> 
> 2026-11-24 11:38:17,262 19894 INFO hospital_upgrade odoo.registry: module hr_hospital: creating or updating database tables 

All three insurance policy numbers have been preserved.

## 3 Change Field Type for insurance_policy_number

### 3.1 Changing the field type and updating the database without using a script

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -u hr_hospital --stop-after-init`

We receive an error message:

>2026-11-24 12:26:39,169 26243 INFO hospital_upgrade odoo.registry: module hr_hospital: creating or updating database tables 
>2026-11-24 12:26:39,182 26243 WARNING hospital_upgrade odoo.modules.loading: Transient module states were reset 
>2026-11-24 12:26:39,182 26243 ERROR hospital_upgrade odoo.registry: Failed to load registry 
>2026-11-24 12:26:39,182 26243 CRITICAL hospital_upgrade odoo.service.server: Failed to initialize database `hospital_upgrade`. 
>Traceback (most recent call last):
>  File "/home/odoo/odoo_dev/odoo/odoo/service/server.py", line 1591, in preload_registries
>    registry = Registry.new(dbname, update_module=update_module, install_modules=config['init'], upgrade_modules=config['update'], reinit_modules=config['reinit'])
>               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/home/odoo/odoo_dev/odoo/odoo/tools/func.py", line 88, in locked
>    return func(inst, *args, **kwargs)
>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/registry.py", line 189, in new
>    load_modules(
>  File "/home/odoo/odoo_dev/odoo/odoo/modules/loading.py", line 466, in load_modules
>    load_module_graph(
>  File "/home/odoo/odoo_dev/odoo/odoo/modules/loading.py", line 196, in load_module_graph
>    registry.init_models(env.cr, model_names, {'module': package.name}, update_operation == 'install')
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/registry.py", line 779, in init_models
>    model._auto_init()
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/models.py", line 3234, in _auto_init
>    new = field.update_db(self, columns)
>          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/fields.py", line 1108, in update_db
>    self.update_db_column(model, column)
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/fields.py", line 1142, in update_db_column
>    self._convert_db_column(model, column)
>  File "/home/odoo/odoo_dev/odoo/odoo/orm/fields.py", line 1146, in _convert_db_column
>    sql.convert_column(model.env.cr, model._table, self.name, self.column_type[1])
>  File "/home/odoo/odoo_dev/odoo/odoo/tools/sql.py", line 391, in convert_column
>    _convert_column(cr, tablename, columnname, columntype, using)
>  File "/home/odoo/odoo_dev/odoo/odoo/tools/sql.py", line 415, in _convert_column
>    cr.execute(query, log_exceptions=False)
>  File "/home/odoo/odoo_dev/odoo/odoo/sql_db.py", line 440, in execute
>    self._obj.execute(query, params)
>psycopg2.errors.InvalidTextRepresentation: invalid input syntax for type integer: "B-02"
>
>2026-11-24 12:26:39,190 26243 INFO hospital_upgrade odoo.service.server: Initiating shutdown 
>2026-11-24 12:26:39,190 26243 INFO hospital_upgrade odoo.service.server: Hit CTRL-C again or send a second signal to force the shutdown. 
>2026-11-24 12:26:39,190 26243 INFO hospital_upgrade odoo.sql_db: ConnectionPool(read/write;used=0/count=0/max=64): Closed 1 connections  

### 3.1 Changing the field type and updating the database WITH migrations script

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -u hr_hospital --stop-after-init`

>2026-11-24 14:04:47,756 37967 INFO hospital_upgrade odoo.modules.loading: loading 28 modules... 
>2026-11-24 14:04:47,898 37967 INFO hospital_upgrade odoo.modules.loading: Loading module hr_hospital (25/28) 
>2026-11-24 14:04:47,946 37967 INFO hospital_upgrade odoo.modules.migration: module hr_hospital: Running upgrade [>19.0.1.2.0] pre-10-normalize-policy-number 
>2026-11-24 14:04:47,968 37967 INFO hospital_upgrade odoo.registry: module hr_hospital: creating or updating database tables 

Each number was split into text and a numeric value.
The text was placed in the "Series" field.
The numeric value was placed in the "Number" field.

## 4 Add column first_visit_date

### 4.1 After changes run the update agine:

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -u hr_hospital --stop-after-init`

>2026-11-24 14:56:35,403 46779 INFO hospital_upgrade odoo.modules.loading: loading hr_hospital/demo/osl_doctor_history.xml 
>2026-11-24 14:56:35,406 46779 INFO hospital_upgrade odoo.modules.migration: module hr_hospital: Running upgrade [19.0.1.3.0>] post-10-fill-first-visit-date 
>2026-11-24 14:56:35,432 46779 INFO hospital_upgrade odoo.modules.loading: Module hr_hospital loaded in 0.51s, 788 queries (+788 other) 
>2026-11-24 14:56:35,518 46779 INFO hospital_upgrade odoo.modules.loading: 28 modules loaded in 0.78s, 788 queries (+788 extra) 
>2026-11-24 14:56:35,674 46779 INFO hospital_upgrade odoo.registry: verifying fields for every extended model 

For each patient who had at least one visit, the date of their earliest visit has been added. 

## 5.Relaunching the full update

### 5.1 drop database and restore database
`sudo -u odoo dropdb hospital_upgrade`
`createdb -U odoo -h localhost hospital_upgrade `
`sudo -u odoo pg_restore -v -d hospital_upgrade /home/odoo/odoo_dev/before.dump`

### 5.2 Full upgrade

`odoo/odoo-bin -c config/odoo.conf -d hospital_upgrade -u hr_hospital --stop-after-init`

No error message !!!