from django.shortcuts import render, redirect
from .models import Product , Category
from sales.models import Sale
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import ProductForm, RestockForm, SoldForm
from pprint import pprint

# Create your views here.

def display_products(request):
  products = Product.objects.all()
  context = {"products": products}
  return render(request, "products/display_products.html", context)

def category(request):
    categories = Category.objects.all()
    context = {
        "categories" : categories
    }
    return render(request, "products/category.html", context)

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


def restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = RestockForm(request.POST)
        if form.is_valid():
            quantity_received = form.cleaned_data["quantity_received"]
            product.stock_quantity += quantity_received
            product.save()
            return redirect("display")
        
    else:
        form = RestockForm()
    context = {
            "product" : product,
            "form" :  form
        }
    return render(request, "products/restock.html", context)

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
                    reference_number= pk
                )
                return redirect("display")
                
            
    else:
        form = SoldForm()
    context = {
        "product":product,
        "form" : form
    }

    return render (request, "products/sold_products.html", context)


def sale_history(request):
    sales = Sale.objects.all().order_by("sold_at")

    context = {
        "sales":sales
    }

    return render(request, "sales/sale_history.html", context)

    

