from werkzeug import url_decode
from flask import Flask, render_template, request, redirect, url_for, flash


class MethodRewriteMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)

class Customer(object):
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

@app.route('/customers')
def list_customers():
    customers = [ Customer(id=1, name=u'My First Customer'), Customer(id=2, name=u'My Second Customer')]
    return render_template('list_customers.html', customers=customers)


@app.route('/customers', methods=['POST',])
def create_customer():
    id = request.form['id']
    name = request.form['name']
    customer = Customer(id=id, name=name)
    flash('Customer %s sucessful saved!' % customer.name)
    return redirect(url_for('list_customers'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5000)
