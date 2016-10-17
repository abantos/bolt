"""
coverage
--------

TBD
"""
import logging
import bolt

def execute_coverage(**kwargs):
    import coverage.control as cov 
    config = kwargs.get('config')
    task_name = config.get('task')
    include_dir = config.get('include')
    out_dir = config.get('output')
    logging.info('Code coverage for {task}. Output at {directory}'.format(task=task_name, directory=out_dir))
    controller = cov.Coverage(auto_data=False, 
        branch=True, source=include_dir)
    controller.start()
    bolt.run_task(task_name)
    controller.stop()
    controller.html_report(directory=out_dir)




def register_tasks(registry):
    registry.register_task('coverage', execute_coverage)
    logging.debug('coverage task registered.')