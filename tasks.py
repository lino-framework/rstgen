from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), # "rstgen",
    revision_control_system='git')
