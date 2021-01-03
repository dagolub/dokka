from .app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class AddressModel(db.Model):
    __tablename__ = "Address"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = db.Column(UUID(as_uuid=True))
    point = db.Column(db.String(1), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(10), default="new", nullable=False)
    address = db.Column(db.String(200), default="", nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_result(self, request_id=False):
        sql = self.get_sql(request_id)
        return db.engine.execute(sql)

    def get_all_points(self, request_id=False):
        return db.engine.execute('SELECT * FROM "Address"')

    def get_sql(self, request_id=False):
        sql = """select l.point||r.point as links,
                        ST_Distance(
                        ST_SetSRID(ST_MakePoint(l.longitude, l.latitude), 4267)::geography,
                        ST_SetSRID(ST_MakePoint(r.longitude, r.latitude), 4267)::geography
                        ) as distance
                        from \"Address\" as l
                        left join \"Address\" as r on l.point < r.point
                        where r.point is not null"""

        if request_id:
            sql += " and request_id = '" + request_id + "'"

        return sql
