from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import hashlib
import uuid




# Connect to the Database
try:
    conn = psycopg2.connect(database="chatdb",
                            host="10.31.0.252",
                            user="postgres",
                            password="Admin.123",
                            port="5432")
    print("Database connection successful")
except psycopg2.OperationalError as e:
    print(f"connection to server at 10.31.1.1, port 5432 failed: {e}")
    exit(1)

cur = conn.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS users (user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), username varchar, password varchar);")
conn.commit()

# cur.execute("DROP TABLE IF EXISTS users;")
# conn.commit()

# cur.execute("SELECT * FROM users");
# rows = cur.fetchall()
# print(rows)



# # INSERT A SAMPLE USER
# cur.execute("INSERT INTO users (username, password) VALUES ('coddy', 'password');")
# conn.commit()



class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open('html_pages/index.html') as f:
                page = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode('utf-8'))

        elif self.path == "/login":
            with open('html_pages/login.html') as f:
                page = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode('utf-8'))

        elif self.path == "/signup":
            with open('html_pages/register.html') as f:
                page = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode('utf-8'))





    def do_POST(self):
        path = self.path

        if path == "/api/auth/register":
            with open('html_pages/response_page.html') as f:
                page = f.read()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print(body)

            # process the form data and save it to the database
            data = body.decode('utf-8').split("&")
            username = data[0].split("=")[1]
            password = data[1].split("=")[1]

            pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            print(f"password hash: {pass_hash}")

            cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
            rows = cur.fetchall()
            print(rows)
            if len(rows) > 0:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(page.replace("$Title$", "Error").replace("$END$", "User already exists").encode('utf-8'))
                return

            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, pass_hash))
            conn.commit()

            print(f"Added user {username} to the database")

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page.replace("$Title$", "Success").replace("$END$", f"Welcome {username}").encode('utf-8'))

        elif path == "/api/auth/login":
            with open('html_pages/response_page.html') as f:
                page = f.read()

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print(body)

            # process the form data and save it to the database
            data = body.decode('utf-8').split("&")
            username = data[0].split("=")[1]
            password = data[1].split("=")[1]

            pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()


            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (username, pass_hash))
            rows = cur.fetchall()
            print(rows)
            if len(rows) > 0:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(page.replace("$Title$", "Success").replace("$END$", f"Welcome {username}").encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(page.replace("$Title$", "Error").replace("$END$", f"Invalid username or password").encode('utf-8'))


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)

    print("Server running on port 8080")
    server.serve_forever()




