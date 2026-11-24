Changelog
=========

19.0.1.1.0
----------
* The field `insurance_policy_number` is being renamed to `insurance_number`.
* The script prevents data loss during the renaming process.

19.0.1.2.0
----------
* The `insurance_number` field is split into two fields: Series and Number.
* The script moves all letters into the "Series" field, and converts all digits into a number.

19.0.1.3.0
----------
* A `first_visit_date` field is being added.
* The script searches for the patient's earliest visit and takes the date from this visit to fill in the field.

OLD Changelog
=========

19.0.6.1
----------------
* Testing and adding documentation.

19.0.5.2
----------------
* Creating reports.

19.0.4.0
----------------
* Creating list views, forms, form filters, Kanban views, and more.

19.0.3.3
----------------
* Creating model classes.

19.0.2.1
----------------
* Creating the module folder structure and adding a README file.

19.0.1.0
----------------
* Init version.