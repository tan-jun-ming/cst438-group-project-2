from app import db

class SampleObject(db.Model):
    __tablename__ = "objects"

    o_id = db.Column(db.Integer, primary_key=True)
    o_name = db.Column(db.String())
    o_num = db.Column(db.Float())
    o_bool = db.Column(db.Boolean())


    def __init__(self, o_name, o_num, o_bool):
        self.o_name = o_name
        self.o_num = o_num
        self.o_bool = o_bool

    
    def serialize(self):
        return {
            'id': self.o_id, 
            'name': self.o_name,
            'num': self.o_num,
            'bool':self.o_bool
        }
