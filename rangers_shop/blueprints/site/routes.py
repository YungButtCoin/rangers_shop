from flask import Blueprint, render_template, request, flash, redirect

#internal imports
from rangers_shop.models import Product, Order, Customer, db, product_schema, products_schema 
from rangers_shop.forms import ProductForm



#we need to instantiate our Blueprint object
site = Blueprint('site', __name__, template_folder='site_templates') #telling your blueprint where to load the html files 



#create our first route
@site.route('/')
def shop():

    shop = Product.query.all()
    #shop = Product.query.filter(Product.user_id).all()
    customers = Customer.query.all()
    orders = Order.query.all()

    shop_stats = {
        'products': len(shop),
        'sales': sum([order.order_total for order in orders]), #order totals was total cost of that specifc order 
        'customers': len(customers)
    }

    return render_template('shop.html', shop=shop, stats=shop_stats) #basically displaying our shop.html page

#create our CREATE route
@site.route('/shop/create', methods=['GET','POST'])
def create():

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():

        try:
            name = createform.name.data
            desc = createform.description.data
            image = createform.image.data
            price = createform.price.data
            quantity = createform.quantity.data

            shop = Product(name, price, quantity, image, desc)

            db.session.add(shop)
            db.session.commit()

            flash(f'You have successfully added {name}!', category='success')
            return redirect('/')
        except:
            flash('We were unable to process your request.  Please try again', category='warning')
            return redirect('/shop/create')
        
    return render_template('create.html', form=createform)

#Create our UPDATE route
@site.route('/shop/update/<id>', methods=['GET','POST'])
def update(id):

    updateform = ProductForm()
    product = Product.query.get(id) #Essentially a WHERE clause, WHERE product.prod_id == id

    if request.method == 'POST' and updateform.validate_on_submit():

        try:
            product.name = updateform.name.data
            product.desciption = updateform.description.data
            product.set_image(updateform.image.data, updateform.name.data) #calling upon that set_image method to set our image!
            product.price = updateform.price.data
            product.quantity = updateform.quantity.data

            db.session.commit() #commits the changes

            flash(f'You have successfully updated {product.name}!', category='success')
            return redirect('/')
        
        except:
            flash('We were unable to process your request.  Please try again', category='warning')
            return redirect('/shop/create')
        
    return render_template('update.html', form=updateform, product=product)


@site.route('/shop/delete/<id>')
def delete(id):

    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return redirect('/')