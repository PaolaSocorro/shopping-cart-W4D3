"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, session, redirect, url_for, escape, request, render_template, redirect, flash
import jinja2

import model


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    # print session
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    # print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""
    
    # print "HERE'S ALL THE ITEMS IN YOUR SESSION: ", session

    """Point to key of cart in the session. retrieve values 
    for that key. it will be a list of melon ids.
    Pass list of melons ids to template.
    iterate over list in template. 
    use class to find each melon by id in database. 
    use jinja to iterate over it and display melons. """


    # cart_items_by_id = session['cart'] 
    cart_ids = session['cart'] 
    print "HELLO", cart_ids
    #make a dictionary counting number of times each melon id appears in the list. 
    #The keys will be the id numbers and the values will be the qty.
    cart_quantity = {}
    for ids in cart_ids:
        if ids in cart_quantity:
            cart_quantity[ids]+=1
        else:
            cart_quantity[ids] = 1 

    print "FIND ME",cart_quantity

    ids_list = list(cart_quantity.keys())

    for values in ids_list:
        melon = model.Melon.get_by_id(values)
        amount = cart_quantity[values]
        print melon    

    return render_template("cart.html",our_melon=melon,quantity=amount)



@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """


    if "cart" not in session:
        session["cart"]=[]

    session["cart"].append(id) 
    
    flash("Your item has been added to the cart!")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    login_id = email,password

    if login_id:
        session['login_id'] = login_id
    

    return redirect("/melons")




@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
