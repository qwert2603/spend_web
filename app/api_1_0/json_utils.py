def record_to_json(record):
    return {
        'uuid': record.uuid,
        'type': record.record_type_id,
        'date': record.date.strftime("%Y-%m-%d"),
        'kind': record.kind,
        'value': record.value,
        'updated': record.updated,
        'deleted': record.deleted,
    }
