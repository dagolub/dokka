from flask import Flask, request
from flask_restful import Api
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)


class AddressDb(db.Model):
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    point = db.Column(db.String(1), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(10), default="new", nullable=False)
    address = db.Column(db.String(200), default="", nullable=False)


def get():
    sql = """select l.point||r.point as links,
    ST_Distance(
    ST_GeogFromText('SRID=4326;POINT(' || l.latitude || ' ' || l.longitude || ' )')
    , ST_GeogFromText('SRID=4326;POINT(' || r.latitude || ' ' || r.longitude || '  )')
    ) as distance
    from \"Address\" as l
    left join \"Address\" as r on l.point < r.point
    where r.point is not null"""
    # sql = "select * from \"Address\""
    print(sql)
    result = db.engine.execute(sql)
    print(result)
    response = []
    for row in result:
        response.append(row)
    return response

print(get())