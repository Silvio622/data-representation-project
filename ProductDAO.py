# Python database connection
# Author: Silvio Dunst


# Import database configuration file from "dbconfig.py"
import dbconfig as cfg 
import mysql.connector

class Productdb:  

    '''
    # Code for creating database if not already in MySQL installed
    db = '' #create a variable db for database
  
    # Check if the Database "productsdb" is already installed if not install the database "productsdb"
    def __init__(self,hostname,username,userpassword):
        self.db = mysql.connector.connect(
            host = hostname,
            user = username,
            password = userpassword
            )

        cursor = self.db.cursor()

        # Check if the database "productsdb" is already created when not created create the database "productsdb"
        cursor.execute("SHOW DATABASES") # show all databases and put it in the variable cursor

        # loop through the databases variable cursor
        for database in cursor:
            if database == ('productsdb',):# check if the productsdb database is available
                found = True
                break
            else:
                found = False
            #print(database)

        # if the productsdb database is not available create the database    
        if found == False:  
            cursor.execute("CREATE DATABASE productsdb") # create a new database if not already in the database
            cursor.execute("USE productsdb") # use the database productsdb

            # create a new table 
            createtable = "CREATE TABLE producttb (productid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, productname VARCHAR(250), manufacturer VARCHAR(250), price float, vendorid VARCHAR(250))"
            cursor.execute(createtable)
            #print("Not Found")

#checkdb = Productdb(hostname='localhost',username='root', userpassword='root')
    '''
    
    db = '' # Create a variable db for database
    
     # Database connection
    def connectToDatabase(self):
        self.db = self.db = mysql.connector.connect(
            host = cfg.mysql['host'],
            user = cfg.mysql['user'],
            password = cfg.mysql['password'],
            database = cfg.mysql['database'],
            )

  
    # Initialize database connections
    def __init__(self):
        self.connectToDatabase()


    # Get the database cursor
    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDatabase()
        return self.db.cursor
    
    
    # Create a new product in the database
    def create(self,product):
        cursor = self.db.cursor()
        sql = "insert into producttb (productid, productname, manufacturer, price, vendorid) values (%s,%s,%s,%s,%s)" 
        values = [
            product['productid'],
            product['productname'],
            product['manufacturer'],
            product['price'],
            product['vendorid']
        ] 
        cursor.execute(sql,values)
        self.db.commit()
        nextid = cursor.lastrowid + 1
        cursor.close()
        return cursor.lastrowid


    # Get all products from the database
    def getAll(self):
        cursor = self.db.cursor()
        sql = "select * from producttb"
        cursor.execute(sql)
        results = cursor.fetchall() 
        returnArray = []
                
        for result in results:
            resultAsDict = self.convertToDict(result) 
            returnArray.append(resultAsDict) 
        cursor.close()
        return returnArray 


    # Find a product by the id in the database  
    def findbyId(self,productid):
        cursor = self.db.cursor()
        sql = "select * from producttb where productid = %s"
        values = [productid] 
        cursor.execute(sql,values)
        result = cursor.fetchone() 
        cursor.close()
        return self.convertToDict(result)
        

    # Update a product in the database
    def update(self,product):
        cursor = self.db.cursor()
        sql = "update producttb set price = %s, productname = %s, manufacturer = %s, vendorid = %s where productid = %s" 
        values = [
            product["price"],
            product['productname'],
            product['manufacturer'],
            product['vendorid'],
            product['productid']
        ] 
        cursor.execute(sql,values)
        self.db.commit()
        cursor.close()
        return product


    # Delete a product from the database
    def delete(self,productid):
        cursor = self.db.cursor()
        sql = "delete from producttb where productid = %s" 
        values = [productid]
        cursor.execute(sql,values)
        self.db.commit()
        cursor.close()
        return {} 


    # Create a dictionary for products
    def convertToDict(self,result):
        columnames = ["productid", "productname", "manufacturer", "price", "vendorid" ]
        products = {} 

        if result:
            for index, columname in enumerate(columnames): 
                value = result[index]
                products[columname] = value 
        return products 

productdb = Productdb()

