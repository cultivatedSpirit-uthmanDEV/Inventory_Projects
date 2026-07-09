from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import ProductForm, RestockForm

# Create your views here.

def display_products(request):
  products = Product.objects.all()
  context = {"products": products}
  return render(request, "products/display_products.html", context)



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
    products = get_object_or_404(Product, pk)
    if request.method == "POST":
        form = RestockForm(request.POST)
        if form.is_valid:
            products.stock_quantity += "Quantity Received"
    

