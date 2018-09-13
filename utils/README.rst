===============
Utility Scripts
===============

----------------------------------------
Engineerng Reference Groups and Policies
----------------------------------------

Script: :file:`create_engr_class_policies.py`

Can optionally create:

* Class Year reference group (e.g. `ref:student:class2022`).  These have
  associated Grouper-loader jobs.
* Create the class year engineering basis groups (e.g. 
  `ref:engineering:basis:ece_major_minor`). These are composites.
* Create the Engineering policies for the Spaces app.

The script created groups for ENGU by default, but this can be suppressed.

-----------------------
Event Management System
-----------------------

Script: :file:`csv2student_orgs.py`

This script takes a CSV file which must include columns "Club" and "Email"
and created reference groups in stem `app:ems:ref:club`.  The email address
must be a Lafayette email as it is used to determine the NetID for subjects.

Script: :file:`create_ems_hrtk_policies.py`

This script can create the policy groups and any required intermediate
basis groups for those policies from either departmental reference groups
(`app:ems:ref:dept`) or student organization reference groups
(`app:ems:ref:club`).

