import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Tambahkan secret_key
app.config['SECRET_KEY'] = os.urandom(24)  # Menghasilkan key acak setiap kali aplikasi dijalankan

db = SQLAlchemy(app)

# Models
class TipeBarang(db.Model):
    __tablename__ = 'tipebarang'
    id = db.Column(db.Integer, primary_key=True)
    nama_tipe = db.Column(db.String, nullable=False)

    def json(self):
        return {'id': self.id, 'nama_tipe': self.nama_tipe}

class Barang(db.Model):
    __tablename__ = 'barang'
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.String, unique=True, nullable=False)
    nama_barang = db.Column(db.String, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tipe_id = db.Column(db.Integer, db.ForeignKey('tipebarang.id'), nullable=False)

    tipe = db.relationship("TipeBarang")

    def json(self):
        return {
            'id': self.id,
            'id_barang': self.id_barang,
            'nama_barang': self.nama_barang,
            'jumlah': self.jumlah,
            'tipe': self.tipe.json()
        }

# Helper Functions

def detect_tipe_barang_or_id(nama_barang, tipe='id'):
    """
    Detects the type of barang based on its name.
    Returns the ID or name of the tipe_barang.
    """
    tipe_mappings = {
        "handphone": "Handphone",
        "iphone": "Handphone",
        "samsung": "Handphone",
        "macbook": "Laptop",
        "laptop": "Laptop",
        "tablet": "Tablet",
        "ipad": "Tablet",
        "kulkas": "Kulkas",
        "ac": "AC",
        "televisi": "Televisi",
        "tv": "Televisi",
        "meja": "Meja",
        "kursi": "Kursi",
        "peralatan masak": "Peralatan Masak",
        "oven": "Peralatan Masak",
    }
    for keyword, tipe_barang in tipe_mappings.items():
        if keyword in nama_barang.lower():
            result = TipeBarang.query.filter_by(nama_tipe=tipe_barang).first()
            return result.id if tipe == 'id' and result else tipe_barang
    return None

# Routes

# Home
@app.route('/', methods=['GET'])
def home():
    total_barang = Barang.query.count()
    total_tipe_barang = TipeBarang.query.count()
    return render_template('home/index.html', total_barang=total_barang, total_tipe_barang=total_tipe_barang)

# Barang Routes
@app.route('/barang', methods=['GET'])
def get_all_barang():
    """Retrieve all barang or search for specific barang."""
    search = request.args.get('search', '')
    tipe_id = request.args.get('tipe_id', None, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Barang.query
    if search:
        query = query.filter(
            (Barang.nama_barang.ilike(f'%{search}%')) |
            (Barang.id_barang.ilike(f'%{search}%'))
        )
    if tipe_id:
        query = query.filter(Barang.tipe_id == tipe_id)

    barang_list = query.paginate(page=page, per_page=per_page, error_out=False)

    tipe_list = TipeBarang.query.all()
    return render_template('/barang/index.html', barang_list=barang_list, tipe_list=tipe_list)

@app.route('/barang/create', methods=['GET', 'POST'])
def add_barang():
    """Add a new barang."""
    if request.method == 'POST':
        data = request.form
        errors = []

        # Validation
        if not data.get('nama_barang'):
            errors.append("Nama barang is required.")
        if not data.get('tipe_id') or not data['tipe_id'].isdigit():
            errors.append("Tipe ID must be a valid number.")
        if not data.get('jumlah') or int(data.get('jumlah', 0)) <= 0:
            errors.append("Jumlah must be a valid positive number.")

        if errors:
            tipe_list = TipeBarang.query.all()
            return render_template(
                '/barang/create.html',
                tipe_list=tipe_list,
                errors=errors,
                nama_barang=data.get('nama_barang', ''),
                jumlah=data.get('jumlah', ''),
                tipe_id=data.get('tipe_id', '')
            )

        # Jika validasi lolos, tambahkan barang baru
        new_barang = Barang(
            id_barang=str(uuid.uuid4()),
            nama_barang=data['nama_barang'],
            jumlah=int(data['jumlah']),
            tipe_id=int(data['tipe_id'])
        )
        db.session.add(new_barang)
        db.session.commit()
        flash("Barang berhasil ditambahkan.", "success")
        return redirect(url_for('get_all_barang'))

    # GET Request untuk tampilan awal form
    tipe_list = TipeBarang.query.all()
    return render_template('/barang/create.html', tipe_list=tipe_list)

# Fungsi untuk menampilkan form create barang
@app.route('/barang/create', methods=['GET'])
def create_view_barang():
    tipe_list = TipeBarang.query.all()
    return render_template('/barang/create.html', tipe_list=tipe_list)

@app.route('/barang/update/<int:id>', methods=['GET', 'POST'])
def update_barang(id):
    barang = Barang.query.get_or_404(id)
    errors = []
    if request.method == 'POST':
        data = request.form

        # Validasi
        if not data.get('nama_barang'):
            errors.append("Nama barang tidak boleh kosong.")
        if not data.get('jumlah') or int(data.get('jumlah', 0)) <= 0:
            errors.append("Jumlah harus lebih dari 0.")
        if not data.get('tipe_id') or not data['tipe_id'].isdigit():
            errors.append("ID Tipe Barang harus berupa angka.")

        if errors:
            return render_template(
                '/barang/update.html',
                barang=barang,
                errors=errors
            )

        # Update barang
        barang.nama_barang = data['nama_barang']
        barang.jumlah = int(data['jumlah'])
        barang.tipe_id = int(data['tipe_id'])
        db.session.commit()
        flash("Barang berhasil diperbarui.", "success")
        return redirect(url_for('get_all_barang'))

    return render_template('/barang/update.html', barang=barang)

@app.route('/barang/delete/<int:id>', methods=['GET'])
def delete_barang(id):
    """Delete a barang by ID."""
    barang = Barang.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    return redirect(url_for('get_all_barang'))

@app.route('/barang/export', methods=['GET'])
def export_barang():
    """Export barang data to CSV."""
    barang_list = Barang.query.all()
    if not barang_list:
        return jsonify({"message": "No data available to export"}), 400

    csv_data = "ID Barang,Nama Barang,Jumlah Barang,ID Tipe Barang\n"
    for barang in barang_list:
        csv_data += f"{barang.id_barang},{barang.nama_barang},{barang.jumlah},{barang.tipe_id}\n"

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=barang.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# TipeBarang Routes
@app.route('/tipebarang', methods=['GET'])
def get_all_tipe():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    tipe_list = TipeBarang.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Redirect ke halaman terakhir jika page melebihi batas
    if page > tipe_list.pages and tipe_list.pages > 0:
        return redirect(url_for('get_all_tipe', page=tipe_list.pages))

    search = request.args.get('search', '')
    return render_template('/tipebarang/index.html', tipe_list=tipe_list, search=search)

@app.route('/tipebarang/create', methods=['GET', 'POST'])
def add_tipebarang():
    if request.method == 'POST':
        data = request.form
        nama_tipe = data.get('nama_tipe', '').strip()

        # Server-side validation
        if not nama_tipe:
            return render_template('/tipebarang/create.html', errors=['Nama Tipe tidak boleh kosong.'])

        # Add tipe barang
        new_tipebarang = TipeBarang(nama_tipe=nama_tipe)
        db.session.add(new_tipebarang)
        db.session.commit()
        return redirect(url_for('get_all_tipe'))
    return render_template('/tipebarang/create.html', errors=[])

# Fungsi untuk mengupdate tipe barang
@app.route('/tipebarang/update/<int:id>', methods=['GET', 'POST'])
def update_tipebarang(id):
    tipe = TipeBarang.query.get_or_404(id)
    if request.method == 'POST':
        nama_tipe = request.form.get('nama_tipe')
        if not nama_tipe:
            flash("Nama tipe barang tidak boleh kosong.", "danger")
            return redirect(url_for('update_tipebarang', id=id))
        
        tipe.nama_tipe = nama_tipe
        db.session.commit()
        flash("Tipe barang berhasil diperbarui.", "success")
        return redirect(url_for('get_all_tipe'))
    return render_template('/tipebarang/update.html', tipe=tipe)

@app.route('/tipebarang/delete/<int:id>', methods=['GET'])
def delete_tipebarang(id):
    tipebarang = TipeBarang.query.get_or_404(id)
    db.session.delete(tipebarang)
    db.session.commit()
    return redirect(url_for('get_all_tipe'))

@app.route('/tipebarang/export', methods=['GET'])
def export_tipebarang():
    """Export tipe barang data to CSV."""
    tipe_list = TipeBarang.query.all()
    if not tipe_list:
        return jsonify({"message": "No data available to export"}), 400

    csv_data = "ID Tipe,Nama Tipe Barang\n"
    for tipe in tipe_list:
        csv_data += f"{tipe.id},{tipe.nama_tipe}\n"

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=tipebarang.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/tipebarang/bulk_delete', methods=['POST'])
def bulk_delete_tipebarang():
    ids = request.json.get('ids', [])
    if ids:
        TipeBarang.query.filter(TipeBarang.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'message': 'Selected items deleted successfully'}), 200
    return jsonify({'message': 'No items selected'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
