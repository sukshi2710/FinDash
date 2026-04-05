from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .models import FinancialRecord
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth # Required for monthly trends

# Create your views here.
# Role Checks
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_analyst(user):
    return user.groups.filter(name__in=['Admin', 'Analyst']).exists()


from django.shortcuts import render
from django.db.models import Sum, Q  # Q is used for the Search enhancement
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator  # Used for Pagination enhancement
from django.contrib.auth.decorators import login_required
from .models import FinancialRecord

@login_required
def dashboard_home(request):
    # 1. Identity & Role Logic (Requirement 1 & 4)
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if "Admin" in user_groups:
        role = "Admin"
    elif "Analyst" in user_groups:
        role = "Analyst"
    else:
        role = "Viewer"

    # 2. Base Queryset (Enhancement: Soft Delete Protection)
    # We only fetch records where is_deleted is False
    records = FinancialRecord.objects.filter(is_deleted=False)

    # 3. Search Support (Enhancement: Dynamic Filtering)
    # Checks if the user typed anything in the search bar
    query = request.GET.get('q')
    if query:
        records = records.filter(
            Q(category__icontains=query) | 
            Q(type__icontains=query)
        )
    
    # 4. Global Aggregation (Requirement 3 - Available to all)
    # Calculations based on the filtered/active records
    total_income = records.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = records.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': total_income - total_expense,
        'user_role': role,
        'search_query': query, # Passed back to keep the search term in the input box
    }

    # 5. Advanced Aggregated Analytics (Requirement 3 & 4 - Restricted to Admin/Analyst)
    if role in ["Admin", "Analyst"]:
        # Category-wise Totals: Grouped spending
        context['category_totals'] = records.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        # Monthly Trends: Time-series aggregation
        context['monthly_trends'] = records.annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total=Sum('amount')
        ).order_by('-month')

        # 6. Pagination (Enhancement: Scalability)
        # Instead of a simple list, we use a Paginator to show 5 records per page
        paginator = Paginator(records.order_by('-date'), 5)
        page_number = request.GET.get('page')
        context['recent_activity'] = paginator.get_page(page_number)

    return render(request, 'dashboard/index.html', context)

@user_passes_test(is_admin)
def add_record(request):
    if request.method == "POST":
        try:
            # 1. Capture data
            amount = request.POST.get('amount')
            category = request.POST.get('category')
            record_type = request.POST.get('type')
            date = request.POST.get('date')

            # 2. Validation: Check for missing fields (Incomplete Input)
            if not all([amount, category, record_type, date]):
                messages.error(request, "All fields are required.")
                return redirect('dashboard_home')

            # 3. Validation: Proper Numeric handling (Incorrect Input)
            amount_val = float(amount)
            if amount_val <= 0:
                messages.error(request, "Amount must be a positive value.")
                return redirect('dashboard_home')

            # 4. Protection against invalid operations (Database Integrity)
            FinancialRecord.objects.create(
                user=request.user,
                amount=amount_val,
                type=record_type,
                category=category,
                date=date
            )
            messages.success(request, "Record added successfully!")

        except ValueError:
            # This triggers if 'amount' is not a valid number (e.g., "abc")
            messages.error(request, "Invalid data type: Amount must be a number.")
        except Exception as e:
            # Generic error response for unexpected issues
            messages.error(request, f"An unexpected error occurred: {e}")
            
    return redirect('dashboard_home')

@user_passes_test(is_admin)
def delete_record(request, record_id):
    record = get_object_or_404(FinancialRecord, id=record_id)
    record.delete()
    messages.success(request, "Record deleted successfully.")
    return redirect('dashboard_home')