# BACKWOOD: E-commerce project 

`git clone https://github.com/sg-source/backwood.git && cd ./backwood `

`docker-compose up --build -d`
###### If you run docker on localhost, move on `http://127.0.0.1:8080/`, otherwise `http://virtual-machine-ip:8080/`

###### Admin user is available as `admin@admin.com:admin` right after running

### Welcome

( ![Backwood]&#40;/web/GH/backwood.png&#41;)

![Backwood](/wev/GH/backwood.png)


### What was done
- User registration & authentication
- Implementation all views according to CBV
- Advanced work with products:
    - Filtering (with ajax)
    - Using mixins
    - Work with products cart (with ajax)
    - Possibility to place an order (and getting invoice)
    - Implementation coupons and getting discount for order (with ajax)
    - Search bar (with ajax)
- Product cart is implemented based on sessions
- Favourites product is implemented based on sessions
- There is recently viewed products as context processor(based on sessions as well)
- Advanced work with ORM:
    - Queries optimization
    - Deleting duplicated and similar queries
    - Selecting only the required fields for each certain case and the other
- There is limit on products quantity in the cart and showing exception, if a product is no longer in stock in desired quantity 

and much more


### TODO
- **TEST COVERAGE**
- Improve profile page:
    - Reset user password
    - Showing user order details(now it displays just a list)
- Optimize queries in getting invoice after successful checkout(the rest is already optimized)
- Improve working with different time zones
- REST interaction (React.js - in the long run)
- Finish sorting products in filter
- Switching to Postgres(in particular "union" doesn't work with "order_by('?')" in SQLite
- Using caching (Redis)
- Build the project as microservices (Nginx+Docker+Gunicorn+Redis+Postgres)
- Deploy on Kubernetes

## Short apps description
- **authapp**
    - Authentication user app
    - BaseUserManager is overridden 
    - Custom model user is inherited from (AbstractBaseUser, PermissionsMixin)
- **cart**
  - Implementation product cart, which allows add/remove/update cart products without page reloading
  - Quick and comfortable cart interaction
  - Represented as context processor
- **coupon**
  - Coupon app for getting discount
  - A simple model for with necessary field
  - It exists in session after activation
- **favourites**
  - Similarly to cart it is implemented based on sessions
- **order**
  - Work with order checkout with possibility to pay it(there is a test payment process)
  - Represented as two models (the first is main with all necessary information, the second is like inline model, which references to main product model - **main.Product**)
  - After successful checkout and payment it updates a product quantity in stock
- **main**
  - Main app in the project with common templates and major logic
  - Individual components are represented as small rendered parts for including to the general html
