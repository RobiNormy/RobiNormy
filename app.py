from flask import *

#Start
app=Flask(__name__)
app.secret_key = "keyCxzcnzisasd.dff09s8fajcjcdfhhffdfddd-s=sdf"

@app.route('/')
def home():
    import pymysql
    connection=pymysql.connect(host='localhost', user='root', password='', database='mbuni_flask_db')

    # create the cursor: Execute SQL 
    cursor= connection.cursor()
    sql="select * from product where product_category = 'Electronics'"
    cursor.execute(sql)
    data = cursor.fetchall()

    # Fashion
    sql_fashion="select * from product where product_category = 'fashion'"
    cursor.execute(sql_fashion)
    data_fashion= cursor.fetchall()
    
    # Furniture
    sql_furniture="select * from product where product_category = 'Furnitures'"
    cursor.execute(sql_furniture)
    data_furniture= cursor.fetchall()

    # Furniture
    sql_groceries="select * from product where product_category = 'Groceries'"
    cursor.execute(sql_groceries)
    data_groceries= cursor.fetchall()

    # end home
    return render_template('home.html', electronics = data, fashion = data_fashion, furniture = data_furniture, groceries = data_groceries)

@app.route('/upload',methods=['POST','GET']) 
def upload():
    if request.method=='POST':
        product_name=request.form["product_name"]
        product_desc=request.form["product_desc"]
        product_cost=request.form["product_cost"]
        product_category=request.form["product_category"]
        product_image_name=request.files["product_image_name"]

        #step 1:save img file to static/images/
        product_image_name.save('static/images/'+ product_image_name.filename)

        #connect to the database --> mbuni_flask_db
        import pymysql
        connection=pymysql.connect(host='localhost', user='root', password='', database='mbuni_flask_db')

        #create cursor(): execute sql

        cursor=connection.cursor()
        data=(product_name,product_desc,product_cost,product_category,product_image_name.filename)

        #sql to insert data to a table product
        sql="insert into product(product_name,product_desc,product_cost,product_category,product_image_name) values(%s,%s,%s,%s,%s)"

        #use the cursor to execute sql,then pass data
        cursor.execute(sql,data)
        connection.commit()
        return render_template('upload.html',message='Uploaded Successfully')
    
    else:
        return render_template('upload.html', message='Please Add Product Here')
    
@app.route('/single/<product_id>')
def single(product_id):
        import pymysql
        connection=pymysql.connect(host='localhost', user='root', password='', database='mbuni_flask_db')

        # Step 2: Create Cursor()
        cursor = connection.cursor()

        # Step 3: SQL Query -> product_id from URL
        sql = "select * from product where product_id = %s"
        cursor.execute(sql, product_id)
        data = cursor.fetchone()
        return render_template('single.html', single= data)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form["username"]
        phone = request.form["phone"]
        email = request.form["email"]
        confirm = request.form["confirm"]
        user_image_name =request.files["user_image_name"]
        password = request.form["password"]
        

        import pymysql
        connection=pymysql.connect(host='localhost',user='root',password='',database='mbuni_flask_db')
        cursor =connection.cursor()
        data = (username,phone,email,user_image_name.filename ,password)
        if password != confirm:
            return render_template('register.html',error="PASSWORD DONT MATCH")
        elif len(password)< 8:
         return render_template('register.html',error='YOUR PASSWORD IS INSECURE MUST EXCEEED 8 CHARACTERS')
        else:
         sql = "insert into user(username,phone,email,user_image_name, password)values(%s,%s,%s,%s,%s)"
        cursor.execute(sql, data)
        connection.commit()
        from sms import send_sms
        send_sms(phone, f"Thank you {username}, Karibu Sana!")
        return render_template('register.html', success = 'Welcome!')

    else:
        return render_template('register.html',message ='please register your information')
    
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST': 
        username = request.form["username"]
        password = request.form["password"]
        
        import pymysql
        connection = pymysql.connect(host = 'localhost', user= 'root', password = '', database='mbuni_flask_db')
        data = (username, password)
        sql = "select * from user where username = %s and password = %s"
        cursor = connection.cursor()
        cursor.execute(sql, data)
        #  cursor.rowcount = returns the number of records
        if cursor.rowcount == 0:
            return render_template('login.html', message = 'Login Here', warning = 'Invalid Credentials')
        else:
            user= cursor.fetchone()
            print(user)
            session ["key"] = user[1]
            session ["phone"] = user[2]
            session ["image"] = user[4]
            return redirect('/')
    else:
        return render_template('login.html', message = 'Login Here')
    
@app.route('/logout')
def logout():
    if "key" in session:
        session.clear()
        return redirect('/login')
    
@app.route('/mpesa', methods = ['POST'])
def mpesa():
    phone = request.form["phone"]
    amount = request.form["amount"]

    from mpesa import stk_push
    stk_push(phone, amount)
    return "Please Check Your Phone to Complete Payment...."

@app.route('/vendor', methods = ['POST', 'GET'])
def vendors():
    if request.method=='POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        county = request.form["county"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        email = request.form["email"]

        import pymysql
        connection = pymysql.connect(host = 'localhost', user= 'root', password = '', database='mbuni_flask_db')
        data = (firstname, lastname, county, password, email)
        cursor = connection.cursor()
        if password != confirm:
            return render_template('vendors.html', error="PASSWORD DO NOT MATCH")
        elif len(password) < 8:
            return render_template('vendors.html', error="PASSWORD MUST EXCEED 8 CHARACTERS")
        else:
         sql = "insert into vendors(firstname, lastname, county, password, email) values(%s,%s,%s,%s,%s)"
        cursor.execute(sql, data)
        connection.commit()
        return render_template('vendors.html', success = 'Welcome!')

    else:
        return render_template('vendors.html', message='Create Vendor Account')
    

@app.route('/vlogin', methods = ['POST', 'GET'])
def vlogin():
    if request.method == 'POST': 
        email = request.form["email"]
        password = request.form["password"]
        
        import pymysql
        connection = pymysql.connect(host = 'localhost', user= 'root', password = '', database='mbuni_flask_db')
        data = (email, password)
        sql = "select * from vendors where email = %s and password = %s"
        cursor = connection.cursor()
        cursor.execute(sql, data)
        #  cursor.rowcount = returns the number of records
        if cursor.rowcount == 0:
            return render_template('vlogin.html', message = 'Login Here', warning = 'Invalid Credentials')
        else:
            user= cursor.fetchone()
            print(user)
            session ["key"] = user[4]
           
            return redirect('/')
    else:
        return render_template('vlogin.html', message = 'Login Here')
    
        
    
    


app.run(debug=True)
#End