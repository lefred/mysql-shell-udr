def alter_progress(session):
    query = session.sql("""SELECT stmt.THREAD_ID, stmt.SQL_TEXT, stage.EVENT_NAME AS State,
                   stage.WORK_COMPLETED, stage.WORK_ESTIMATED,
                   lpad(CONCAT(ROUND(100*stage.WORK_COMPLETED/stage.WORK_ESTIMATED, 2),"%"),12," ") 
                   AS CompletedPct, 
                   lpad(format_pico_time(stmt.TIMER_WAIT), 10, " ") AS StartedAgo,
                   current_allocated Memory           
            FROM performance_schema.events_statements_current stmt                
            INNER JOIN sys.memory_by_thread_by_current_bytes mt  
                    ON mt.thread_id = stmt.thread_id 
            INNER JOIN performance_schema.events_stages_current stage 
                    ON stage.THREAD_ID = stmt.THREAD_ID""")

    result = query.execute()
    report = [result.get_column_names()]
    for row in result.fetch_all():
        report.append(list(row))

    return {'report': report}

shell.register_report(
    'alter_progress',
    'list',
    alter_progress,
    {
        'brief': 'Shows InnoDB Alter Progressions.',
        'details': ['Needs to have some intruments and consumer enabled.'],
        'argc': '0'
    }
)

