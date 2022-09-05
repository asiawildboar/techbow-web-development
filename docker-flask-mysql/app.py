from flask import Flask, Response, request, abort
from flask import jsonify
from flaskext.mysql import MySQL
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)
log = logging.getLogger()

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'techbow'
app.config['MYSQL_DATABASE_HOST'] = 'mysql-host'
mysql.init_app(app)


@app.route("/")
def hello():
    return Response("Hi from your Flask app running in your Docker container!")


@app.route("/user/<int:user_id>", methods=['GET'])
def get_email_by_user_id(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email from user where id = {user_id}".format(user_id=user_id))
    user_info = cursor.fetchone()
    conn.close()
    return jsonify({'user_id': user_id, 'user_info': user_info})


@app.route('/user', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    conn = mysql.connect()
    cursor = conn.cursor()
    log.info("name: " + request.json['name'] + " email: " + request.json['email'])
    insert_stmt = (
        "INSERT INTO user (name, email) "
        "VALUES (%s, %s)"
    )
    data = (request.json['name'], request.json['email'])
    cursor.execute(insert_stmt, data)
    # By default Connector/Python turns autocommit off
    # The commit() function allows the data to be saved permanently.
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    user_id = cursor.fetchone()[0]
    conn.close()
    return jsonify({'user_id': user_id, 'name': request.json['name'], 'email': request.json['email']})


@app.route('/product', methods=['POST'])
def create_product():
    if not request.json or not 'productName' in request.json:
        abort(400)
    conn = mysql.connect()
    cursor = conn.cursor()
    log.info("productName: " + request.json['productName'] + " supplier: " + request.json['supplier'] + " price: " + str(request.json['price']))
    insert_stmt = (
        "INSERT INTO product (product_name, supplier, price) "
        "VALUES (%s, %s, %s)"
    )
    data = (request.json['productName'], request.json['supplier'], request.json['price'])
    cursor.execute(insert_stmt, data)
    # By default Connector/Python turns autocommit off
    # The commit() function allows the data to be saved permanently.
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    product_id = cursor.fetchone()[0]
    conn.close()
    return jsonify({'product_id': product_id, 'product_name': request.json['productName'], 'supplier': request.json['supplier'], 'price': request.json['price']})


@app.route("/user/<int:user_id>", methods=['POST'])
def add_to_cart(user_id):
    if not request.json or not 'productId' in request.json:
        abort(400)
    conn = mysql.connect()
    cursor = conn.cursor()
    insert_stmt = (
        "INSERT INTO user_product (user_id, product_id) "
        "VALUES (%s, %s)"
    )
    data = (user_id, request.json['productId'])
    cursor.execute(insert_stmt, data)
    # By default Connector/Python turns autocommit off
    # The commit() function allows the data to be saved permanently.
    conn.commit()
    conn.close()
    return jsonify({'user_id': user_id, 'product_id': request.json['productId']})


@app.route("/user/<int:user_id>/cart/all", methods=['GET'])
def view_my_cart(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id from user_product where user_id = {user_id}".format(user_id=user_id))
    product_id_all = cursor.fetchall()
    conn.close()
    return jsonify({'user_id': user_id, 'product_id_all': product_id_all})


@app.route("/user/<int:user_id>/cart/allinfo", methods=['GET'])
def view_all_my_cart(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """
            select p.product_name, p.supplier, p.price, u.name, u.email
            from product p
            join user_product up
            on p.id = up.product_id
            join user u
            on u.id = up.user_id
            where u.id = {user_id}
        """
        .format(user_id=user_id))
    product_info_all = cursor.fetchall()
    conn.close()
    return jsonify({'user_id': user_id, 'product_info_all': product_info_all})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
