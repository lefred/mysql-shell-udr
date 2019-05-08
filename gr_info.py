def gr_info(session):
    query = session.sql("select concat(member_host,':',member_port) as server, member_role as 'role', member_version as 'version', sys.gr_member_in_primary_partition() as 'quorum',  Count_Transactions_Remote_In_Applier_Queue as 'tx behind', Count_Transactions_in_queue as 'tx to cert', count_transactions_remote_applied as 'remote tx', count_transactions_local_proposed as 'local tx' from performance_schema.replication_group_member_stats t1 join  performance_schema.replication_group_members t2 on t2.member_id = t1.member_id")

    result = query.execute()
    report = [result.get_column_names()]
    for row in result.fetch_all():
        report.append(list(row))

    return {'report': report}

shell.register_report(
    'gr_info',
    'list',
    gr_info,
    {
        'brief': 'Shows Group Replication Status.',
        'details': ['You need the SELECT privilege on sys.session view and the '
                    + 'underlying tables and functions used by it.'],
        'argc': '0'
    }
)

