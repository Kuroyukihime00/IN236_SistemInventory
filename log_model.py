
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LogBarang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.String, nullable=False)
    jumlah_perubahan = db.Column(db.Integer, nullable=False)
    alasan = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
