"""
Usage:

python3 test_data_generation.py method_name

method_name should be one of the following:
    insert_users 
    insert_update_users 
    add_column_user 
    delete_all_users
    insert_products

Example:

    python3 test_data_generation.py insert_users

"""
import psycopg2
from faker import Faker
import time
import argparse
import re
import random

class User():

    def __init__(self,username=None,password=None,email=None) -> None:
        if (username is None) and (password is None) and (email is None):
            self.username=self._generate_username()
            self.password=self._generate_password()    
            self.email=self._generate_email()

    def _generate_username(self):
        fake = Faker()
        return fake.name().replace(' ','')

    def _generate_password(self):
        return self.username

    def _generate_email(self):
        return self.username+'@example.com'
    
class Product():
    def __init__(self,) -> None:
        self.product_name=self._generate_product_name()
        self.price=self._generate_price()    

    def _generate_product_name(self):
        fake = Faker()
        return 'product_'+fake.name().replace(' ','')

    def _generate_price(self):
        return random.randint(15,300)/10.0

    
class Database():
    
    def __init__(self,database,host,user,password,port) -> None:
        self.conn = psycopg2.connect(database=database,
                        host=host,
                        user=user,
                        password=password,
                        port=port)

        self.cursor = self.conn.cursor()

    def insert_user(self,user:User):
        sql_insert = """
            INSERT INTO "user" (username, password, email)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        values=(user.username,user.password,user.email)

        self.cursor.execute(sql_insert,values)
        self.conn.commit()
        user_id = self.cursor.fetchone()[0]

        print(f"User with ID {user_id} inserted successfully.")

    def insert_product(self,product):
        sql_insert = """
            INSERT INTO "product" (product_name, price)
            VALUES (%s, %s)
            RETURNING id;
        """
        values=(product.product_name,product.price)

        self.cursor.execute(sql_insert,values)
        self.conn.commit()
        product_id = self.cursor.fetchone()[0]

        print(f"Product with ID {product_id} inserted successfully.")


    def add_column(self,table,new_column_name,new_column_type,defaul_value='teste1'):
        
        alter_query = f"""ALTER TABLE "{table}" ADD COLUMN "{new_column_name}" {new_column_type} DEFAULT '{defaul_value}';"""

        self.cursor.execute(alter_query)
        self.conn.commit()
        print(f"Column '{new_column_name}' added to table '{table}' successfully.")

    def update_users(self,users_list:[User]):
        sql_update="""UPDATE "user" SET 
                        username= %s ,
                        email= %s ,
                        password= %s
                    WHERE
                        username= %s
                    """
        for user in users_list:
            values=(user.username,user.email,user.password,user.username)
            self.cursor.execute(sql_update,values)
        self.conn.commit()

    def delete(self,table,id_list=None):
        if id_list is None:
            sql_delete=f"""delete from  "{table}" ;"""
            self.cursor.execute(sql_delete)
            self.conn.commit()
        else:
            for id in id_list:
                sql_delete=f"""delete from  "{table}" where id=%s;"""
                self.cursor.execute(sql_delete,(id,))
            self.conn.commit()

#----------
DATABASE_CONECTION_ARGS={'database':"testeDB",
                            'host':"localhost",
                            'user':"user",
                            'password':"password",
                            'port':"5434"}
def insert_products():
    db= Database(**DATABASE_CONECTION_ARGS)

    for i in range(10):
        # time.sleep(2)
        new_product=Product()
        db.insert_product(new_product)

def insert_users():
    db= Database(**DATABASE_CONECTION_ARGS)

    for i in range(10):
        # time.sleep(2)
        new_user=User()
        db.insert_user(new_user)

def insert_update_users():
    db= Database(**DATABASE_CONECTION_ARGS)
    users=[]
    for i in range(10):
        # time.sleep(2)
        new_user=User()
        users.append(new_user)
        db.insert_user(new_user)
    
    for user in users:
        user.email = re.sub('@.*','@example2.mm',user.email)
    db.update_users(users)

def add_column_user():
    db= Database(**DATABASE_CONECTION_ARGS)
    integer=random.randint(0,100)
    db.add_column('user',f'column{integer}','VARCHAR')
    pass

def delete_all_users():
    db= Database(**DATABASE_CONECTION_ARGS)
    db.delete('user')
    pass 


if __name__=='__main__':

    from enum import Enum, auto

    class Methods(Enum):
        insert_users = auto()
        insert_update_users = auto()
        add_column_user = auto()
        delete_all_users = auto()
        insert_products = auto()

    METHODS_DICT={
        Methods.insert_users:insert_users,
        Methods.insert_update_users :insert_update_users,
        Methods.add_column_user :add_column_user,
        Methods.delete_all_users :delete_all_users,
        Methods.insert_products: insert_products,
    }

    parser = argparse.ArgumentParser(description="My Command Line Tool")
    parser.add_argument("method", 
                        help="Method to be run against test database",
                        choices=[m.name for m in Methods])

    args = parser.parse_args()

    method = args.method
    print(method)

    METHODS_DICT[Methods[method]]()
    