from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import get_object_or_404
from .forms import ProductForm

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

    Edit_product = get_object_or_404(Product, pk=pk)

    form = ProductForm(request.POST or None, instance=Edit_product)

    if request.method == 'POST':
            
            if form.is_valid:
                form.save()
                return redirect('display/')
    context = {
            'form' : form
        }
    return redirect(request, 'edit_product.html', context)

