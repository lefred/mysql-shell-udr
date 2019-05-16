def locks_info(session):
    query = session.sql("select  engine_transaction_id as trx_id, thread_id,concat(object_schema,'.',object_name) as `table`,lock_type,lock_mode,lock_status,lock_data from performance_schema.data_locks")


    result = query.execute()
    report = [result.get_column_names()]
    for row in result.fetch_all():
        report.append(list(row))

    return {'report': report}

shell.register_report(
    'locks_info',
    'list',
    locks_info,
    {
        'brief': 'Shows Locks.',
        'details': ['You need the SELECT privilege on sys.session view and the '
                    + 'underlying tables and functions used by it.'],
        'argc': '0'
    }
)

