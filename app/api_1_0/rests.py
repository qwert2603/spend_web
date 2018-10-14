import datetime
import uuid

from flask import request, jsonify, abort
from sqlalchemy import or_, and_

from app import db
from app.api_1_0 import api_1_0
from app.api_1_0.json_utils import record_to_json
from app.models import Record
from app.utils import get_records_types_ids, now_millis


@api_1_0.route('/get_updates')
def get_updates():
    millis = request.args.get('last_update', type=int, default=0)
    uuid = request.args.get('last_uuid', type=str, default='')
    count = request.args.get('count', type=int, default=10)
    records = Record.query \
        .filter(or_(Record.updated > millis, and_(Record.updated == millis, Record.uuid > uuid))) \
        .order_by(Record.updated.desc(), Record.uuid.desc()) \
        .limit(count) \
        .all()
    return jsonify([record_to_json(record) for record in records])


@api_1_0.route('/delete_records', methods=['DELETE'])
def delete_records():
    uuids = request.json.get('uuids')
    if uuids is None or not isinstance(uuids, list): abort(400)
    not_found_uuids = []
    for uuid in uuids:
        record = Record.query.get(str(uuid))
        if record is not None:
            record.deleted = True
        else:
            not_found_uuids.append(uuid)
    return jsonify(not_found_uuids=not_found_uuids)


@api_1_0.route('/save_records', methods=['POST'])
def save_records():
    records_types_ids = get_records_types_ids()
    records = request.json.get('records')
    if records is None or not isinstance(records, list): abort(400)
    for record in records:
        try:
            record_uuid = record.get('uuid')
            uuid.UUID(record_uuid)
            type_id = int(record.get('type_id'))
            if type_id not in records_types_ids: abort(400)
            date = datetime.datetime.strptime(record.get('date'), "%Y-%m-%d").date()
            kind = record.get('kind').strip()
            if len(kind) == 0: abort(400)
            value = record.get('value')
            if value <= 0: abort(400)
            record = Record.query.get(record_uuid)
            if record is None:
                db.session.add(Record(uuid=record_uuid, record_type_id=type_id, date=date, kind=kind, value=value))
            else:
                if record.deleted: continue
                record.record_type_id = type_id
                record.date = date,
                record.kind = kind
                record.value = value
                record.updated = now_millis()
        except Exception:
            abort(400)

    return 'ok'
