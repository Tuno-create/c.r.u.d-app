from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'store_inventory'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, price, quantity, description) VALUES (%s, %s, %s, %s)", 
                   (name, price, quantity, description))
        mysql.connection.commit()
        cur.close()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        
        cur.execute("UPDATE products SET name=%s, price=%s, quantity=%s, description=%s WHERE id=%s", 
                   (name, price, quantity, description, id))
        mysql.connection.commit()
        cur.close()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()
    
    return render_template('edit_product.html', product=product)

@app.route('/view_product/<int:id>')
def view_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()
    return render_template('view_product.html', product=product)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)