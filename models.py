from app import db
from sqlalchemy.orm import aliased
from sqlalchemy.orm import backref

class Tests(db.Model):
    _tablename_ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(20))
    s_no = db.Column(db.Integer)
    test_name = db.Column(db.String(50))
    tets_field = db.Column(db.String(50))
    test_value = db.Column(db.String(50))
    test_result = db.Column(db.String(10))
    spec_name = db.Column(db.String(50))
    limits_used = db.Column(db.String(50))
    start_time = db.Column(db.String(50))
    stop_time = db.Column(db.String(50))
    comments = db.Column(db.String(50))

    def __init__(self, sn,s_no,test_name,tets_field,test_value,test_result,spec_name,limits_used,start_time,stop_time,comments):
        self.sn = sn
        self.s_no = s_no
        self.test_name = test_name
        self.tets_field = tets_field
        self.test_value = test_value
        self.test_result = test_result
        self.spec_name = spec_name
        self.limits_used = limits_used
        self.start_time = start_time
        self.stop_time = stop_time
        self.comments = comments

    def serialize(self):
        return {
            "id": self.id,
            "sn": self.sn,
            "s_no": self.s_no,
            "test_name": self.test_name,
            "test_field": self.tets_field,
            "test_value": self.test_value,
            "test_result": self.test_result,
            "spec_name": self.spec_name,
            "limits_used": self.limits_used,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "comments": self.comments
        }