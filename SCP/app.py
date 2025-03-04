from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

DATABASE = "SeniorCapstoneDatabase.db"

def connect_db():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return conn

@app.route('/history', methods=['GET']) #purchase history 
def all_i_feel_is_Ahhhhh():
    conn = connect_db()
    cursor = conn.cursor()
    search = request.args.get('search')
    cursor.execute("SELECT * FROM 'Order' WHERE BuyerID=:search", {"search":search})
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)

@app.route('/data', methods=['GET', 'POST']) #For help desk and test "labled index
def all_i_feel_is_pain():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Product")  # Change 'Product' if incorrect
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        conn.close()
        return jsonify(data)
    elif request.method == 'POST':
        print("heck")
        name = request.form.get('name')
        email = request.form.get('email')
        desc = request.form.get('desc')
        try:
            cursor.execute("INSERT INTO HelpDesk (Name, Email, Description) VALUES (?, ?, ?)", 
                           (name, email, desc))
            conn.commit()
            conn.close()
            return jsonify({'success': 'Ticket added successfully'}), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
            
@app.route('/newlisting', methods=['POST']) # used for create new listing
def all_i_feel_is_sad():
    print("here1")
    conn = connect_db()
    cursor = conn.cursor()            
    supplier = '1'
    name = request.form.get('name')
    price = request.form.get('price')
    quant = request.form.get('quantity')
    desc = request.form.get('description')
    print(desc)
    try:
        cursor.execute("INSERT INTO Product (SupplierID, ProdName, ProdPrice, ProdQuantity, ProdDesc) VALUES (?, ?, ?, ?, ?)", 
         (supplier, name, price, quant, desc))
        conn.commit()
        conn.close()
        return jsonify({'success': 'Product added successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500        
            
@app.route('/search', methods=['GET', 'POST']) #used for search feature
def all_i_feel_is_bad():           
    conn = connect_db()
    cursor = conn.cursor()
    search = request.args.get('search')
    #https://stackoverflow.com/questions/62199521/how-to-properly-use-sql-like-statement-to-query-db-from-flask-application
    cursor.execute("SELECT * FROM Product WHERE ProdName LIKE :search", {"search": '%' + search + '%'}) 
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data)
           
if __name__ == '__main__':
    app.run(debug=True)
