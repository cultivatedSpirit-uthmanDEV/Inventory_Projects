from django.shortcuts import render, redirect
from .models import Product , Category
from sales.models import Sale
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import ProductForm, RestockForm, SoldForm
from pprint import pprint
from django.db.models import F
import uuid
from django.contrib.auth.decorators import permission_required

# Create your views here.


@permission_required("products.display_products", raise_exception=True)
def display_products(request):
  products = Product.objects.all()
  context = {"products": products}
  return render(request, "products/display_products.html", context)


@permission_required("products.display_products", raise_exception=True)
def category(request):
    categories = Category.objects.all()
    context = {
        "categories" : categories
    }
    return render(request, "products/category.html", context)


@permission_required("products.add_product", raise_exception=True)
def add_product(request):

    form = ProductForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('display')
 
    context = {
            'form': form
        }

    return render(
            request,
            'products/add_products.html',
             context
        )

@permission_required("products.edit_product", raise_exception=True)
def edit_product(request, pk):

    Edit_product = Product.objects.get(pk=pk)

    form = ProductForm(request.POST or None, instance=Edit_product)

    if request.method == 'POST':
            
            if form.is_valid:
                form.save()
                return redirect('display')
    context = {
            'form' : form
        }
    return render(request, 'products/edit_product.html', context)


@permission_required("products.product_actions", raise_exception=True)
def product_actions(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
    }
    return render(request, "products/product_actions.html", context)


@permission_required("products.delete_product", raise_exception=True)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("display")
    context = {
        "product" : product
    }

    return render(request, "products/delete.html", context )


def search_product(request):
    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query))
    else:
        products = Product.objects.all()
    context = {
        "products" : products,
         "query" : query
    }

    return render(request, "products/display_products.html", context)

@permission_required("products.restock", raise_exception=True)
def restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = RestockForm(request.POST)
        if form.is_valid():
            restock_quantity = form.cleaned_data["restock_quantity"]
           # product.stock_quantity += quantity_received
           # product.save()

            # Using F() with update() instead of:
            #   product.stock_quantity += quantity_received
            #   product.save()
            #
            # Why: the old way reads stock_quantity into Python,
            # adds to it, then saves it back. If two requests restock
            # the same product at nearly the same time, both could
            # read the same starting value before either saves —
            # causing one update to silently overwrite the other
            # (a race condition).
            #
            # F("stock_quantity") tells the database to perform the
            # increment using the CURRENT value in the database at
            # the moment of the update, as a single atomic SQL
            # operation: UPDATE ... SET stock_quantity = stock_quantity + X
            # This avoids the race condition entirely.
           
            Product.objects.filter(pk=pk).update(
            stock_quantity=F("stock_quantity") + restock_quantity)
        return redirect("display")
    else:
        form = RestockForm()
    context = {
            "product" : product,
            "form" :  form
        }
    return render(request, "products/restock.html", context)
@permission_required("products.sold_product", raise_exception=True)
def sold_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = SoldForm(request.POST)
        if form.is_valid():
            sold_quantity = form.cleaned_data["sold_quantity"]
            if sold_quantity > product.stock_quantity:
                form.add_error(
                    "sold_quantity",f"there is no enough {product.name} in stock"
                )
            else:
                product.stock_quantity -= sold_quantity
                product.save()
                Sale.objects.create(
                    total_amount=sold_quantity,
                    sold_by=request.user,
                     reference_number=str(uuid.uuid4())[:8].upper(),
                    product= product
                )
                return redirect("display")
                
            
    else:
        form = SoldForm()
    context = {
        "product":product,
        "form" : form
    }

    return render (request, "products/sold_products.html", context)

@permission_required("products.sale_history", raise_exception=True)
def sale_history(request):
    sales = Sale.objects.all().order_by("sold_by")

    context = {
        "sales":sales
    }

    return render(request, "sales/sale_history.html", context)

    

