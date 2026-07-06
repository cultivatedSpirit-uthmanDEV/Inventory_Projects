from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from sales.models import Sale
from django.db.models import Sum

# Create your views here.
def home_view(request):
  return render(request, 'core/Home.html')

@login_required
def dashboard(request):
    total_products = Product.objects.filter(is_active=True).count()
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('total_amount')
    )['total']
    low_stock_products = Product.objects.filter(
    stock_quantity__lt=5,
    is_active=True
    )
    recent_sales = Sale.objects.order_by(
        '-created_at'
    )[:5]
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
    }

    return render(
        request,
        'core/dashboard.html',
        context
    )

    


    return render(request, "core/dashboard.html")
