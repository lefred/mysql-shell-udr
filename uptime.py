def uptime(session):
    result = session.run_sql("SELECT TIME_FORMAT(SEC_TO_TIME(VARIABLE_VALUE ),'%Hh %im %ss') AS Uptime FROM performance_schema.global_status WHERE VARIABLE_NAME='Uptime';")
    report = [result.get_column_names()]
    for row in result.fetch_all():
        report.append(list(row))

    return {'report': report}

shell.register_report(
    'uptime',
    'list',
    uptime,
    {
        'brief': 'Shows Server Uptime.',
        'details': ['You need the SELECT privilege on performance_schema.global_status.'],
        'argc': '0'
    }
)

