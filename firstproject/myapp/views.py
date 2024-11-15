from django.http import HttpResponse
from django.shortcuts import render
from .models import Details
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
#index
def index(request):
    return render(request, 'index.html')

#home
def home(request):
    return render(request,'home.html')

#registration
def register(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        umail=request.POST.get('umail')
        upsw=request.POST.get('upsw')
        udob=request.POST.get('udob')
        uano=request.POST.get('uano')
        if Details.objects.filter(account_number=uano).exists() or Details.objects.filter(password=upsw).exists():
            return HttpResponse("account number or password already exists.Please choose a different one.")
        data=Details(username=uname,password=upsw,email=umail,date_of_birth=udob,account_number=uano)
        data.save()
        return HttpResponse("registration is done")
    else:
        return render(request,'register.html')
    
#login

def login(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        upsw=request.POST.get('upsw')
        try:
            data=Details.objects.get(username=uname,password=upsw)
            return render(request,'home.html')
        except ObjectDoesNotExist: 
            return render(request,'login.html',{'message':'invalid username or password'})
    else:
        return render(request,'login.html')
    
#viewalldata
def viewalldata(request):
    alldetails=Details.objects.all()
    return render(request,'viewalldata.html',{'alldetails':alldetails} )


#viewspecificdata
def viewspecificdata(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        upsw = request.POST.get('upsw')
        
        if not uname or not upsw:
            return render(request, 'viewspecificdata.html', {'message': 'Username and password are required.'})
        
        try:
            user_details = Details.objects.get(username=uname, password=upsw)
            return render(request, 'viewspecificdatadetails.html', {'user_details': user_details})
        except ObjectDoesNotExist:
            return render(request, 'viewspecificdata.html', {'message': 'Invalid username or password'})
    else:
        return render(request, 'viewspecificdata.html')
    
#withdraw
def withdraw(request):
    if request.method == 'POST':
        account_number= request.POST.get('account_no')
        password = request.POST.get('password')
        amount = request.POST.get('amount')
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")
        
        if not account_number or not password or not amount:
            return HttpResponse("All fields are required.")
        
        if amount <= 0:
            return HttpResponse("Amount should be positive.")
        
        try:
            account = Details.objects.get(account_number=account_number)

            if account.password != password:
                return HttpResponse("Invalid password for the account.")
            
            if account.balance < amount:
                return HttpResponse("Insufficient balance in the account.")
            
            account.balance = account.balance - amount
            account.save()

            return HttpResponse(f"Withdraw {amount} successfully. New balance: {account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'withdraw.html')
    


from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse
from .models import Details, Transaction
#transfer
def transfer(request):
    if request.method == 'POST':
        source_account_no = request.POST.get('source_account_no')
        target_account_no = request.POST.get('target_account_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        
        try:
            amount = Decimal(amount)  # Convert amount to Decimal
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")
        
        if not source_account_no or not target_account_no or not amount or not password:
            return HttpResponse("All fields are required.")
        
        if amount <= 0:
            return HttpResponse("Amount should be positive.")

        try:
            source_account = Details.objects.get(account_number=source_account_no)
            target_account = Details.objects.get(account_number=target_account_no)

            if source_account.password != password:
                return HttpResponse("Invalid password for the source account.")
            
            if source_account.balance < amount:
                return HttpResponse("Insufficient balance in the source account.")
            
            source_account.balance = source_account.balance - amount
            target_account.balance = target_account.balance + amount

            source_account.save()
            target_account.save()

            # Create transaction entries
            Transaction.objects.create(
                source_account=source_account_no,
                transaction_type='DEBIT',
                amount=amount
            )
            Transaction.objects.create(
                source_account=target_account_no,
                transaction_type='CREDIT',
                amount=amount
            )

            return HttpResponse(f"Transferred successfully from account {source_account_no} to account {target_account_no}. New balance: {source_account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("One or both account numbers do not exist.")
    else:
        return render(request, 'transfer.html')
    
#deposit
def deposit(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_no')
        amount = request.POST.get('amount')
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")

        if not account_number or amount <= 0:
            return HttpResponse("Please provide a valid account number and a positive amount.")

        try:
            details = Details.objects.get(account_number=account_number)
            details.balance = details.balance + amount
            details.save()
            return HttpResponse(f"Deposited {amount} successfully. New balance: {details.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'deposit.html')


#balance
def balance(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_no')  # Ensure this matches your form field name
        password = request.POST.get('password')
        
        if not account_number or not password:
            return HttpResponse("Both account number and password are required.")
        
        try:
            # Use the correct field name `account_number` based on the model
            account = Details.objects.get(account_number=account_number)
            
            if account.password != password:
                return HttpResponse("Invalid password for the account.")
            
            return HttpResponse(f"Current balance: {account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'balance.html')
