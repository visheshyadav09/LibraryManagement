import threading
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from library.books import add_books_to_model, get_book_serialized_data


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render("adminlogin")


def add_student(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {"form1": form1, "form2": form2}
    if request.method == "POST":
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            # We are new students extra detail in another table
            user = form1.save()
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create(name="STUDENT")
            my_student_group[0].user_set.add(user)
        messages.success(request, "New Student Added Successfully")
        return HttpResponseRedirect("addstudent")

    return render(request, "library/addstudent.html", context=mydict)


def is_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    else:
        return False


def after_login(request):
    if is_admin(request.user):
        return render(request, "library/adminafterlogin.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def add_book(request):
    # now it is empty book form for sending to html
    form = forms.BookForm()
    if request.method == "POST":
        # now this form have data from html
        form = forms.BookForm(request.POST)
        if form.is_valid():
            book_title = form.cleaned_data["title"]
            num_of_books = form.cleaned_data["number_of_books"]

            # Creating new thread and performing the book import and entry creation on that thread to save time
            task_thread = threading.Thread(
                target=add_books_to_model, args=(num_of_books, book_title)
            )
            task_thread.start()
            return render(request, "library/bookadded.html")
    return render(request, "library/addbook.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def view_book(request):
    books = models.Book.objects.filter(is_deleted=False).prefetch_related("authors")

    # Get serialized data for following books
    serialized_data = get_book_serialized_data(books)

    return render(request, "library/viewbook.html", {"books": serialized_data})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def issue_book(request):
    form = forms.IssuedBookForm()
    if request.method == "POST":
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            # finding the book issued to student and creating entry accordingly
            obj = models.IssuedBook()
            obj.status = "Issued"
            obj.book_issued_number = form.cleaned_data["book_issued_number"].book_number
            obj.student_number = form.cleaned_data["student_number"].student_number

            # finding the number of days book is issued for and charging accordingly
            return_date = form.cleaned_data["return_date"]
            number_of_days_issued_for = (return_date - datetime.now().date()).days
            obj.expirydate = return_date
            obj.save()
            total_charge = number_of_days_issued_for * 15
            models.ChargeIssuedBook.objects.create(
                issuedbook=obj, charge=total_charge, status="Pending"
            )

            return render(request, "library/bookissued.html")
    return render(request, "library/issuebook.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def view_books_issued(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    for ib in issuedbooks:
        issdate = (
            str(ib.issuedate.day)
            + "-"
            + str(ib.issuedate.month)
            + "-"
            + str(ib.issuedate.year)
        )
        expdate = (
            str(ib.expirydate.day)
            + "-"
            + str(ib.expirydate.month)
            + "-"
            + str(ib.expirydate.year)
        )

        # Extracting fine for the issued book
        fine = models.ChargeIssuedBook.objects.get(issuedbook=ib).charge
        books = list(
            models.Book.objects.filter(
                book_number=ib.book_issued_number, is_deleted=False
            )
        )
        students = list(
            models.StudentExtra.objects.filter(
                student_number=ib.student_number, is_deleted=False
            )
        )
        i = 0
        for l in books:
            t = (
                students[i].get_name,
                students[i].student_number,
                books[i].title,
                ", ".join([i["name"] for i in list(books[i].authors.values("name"))]),
                issdate,
                expdate,
                fine,
                ib.status,
                ib.id,
            )
            i = i + 1
            li.append(t)

    return render(request, "library/viewissuedbook.html", {"li": li})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def view_student(request):
    # List of students
    students = models.StudentExtra.objects.filter(is_deleted=False)
    return render(request, "library/viewstudent.html", {"students": students})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def return_book(request, id):
    issued_book = models.IssuedBook.objects.get(id=id)
    student_number = issued_book.student_number
    pending_charge = (
        models.ChargeIssuedBook.objects.filter(
            issuedbook__student_number=student_number, status="Pending"
        )
        .exclude(issued_book=issued_book)
        .aggregate(Sum("charge"))
    )

    # Checking if the user has outstanding debt of more than Rs500
    if pending_charge["charge__sum"] > 500:
        messages.error(request, "User has outstanding debt more than 500")
        return redirect("viewissuedbook")
    else:
        # Updating the status to "Returned" for the issued book
        issued_book.status = "Returned"
        issued_book.save()

        # Charging user for ths charge amount that was entered while issuing the book
        charge_issue_book = models.ChargeIssuedBook.objects.get(
            issuedbook=issued_book, status="Pending"
        )
        charge_issue_book.status = "Paid"
        charge_issue_book.save()
    messages.success(request, "Book has been returned successfully")
    return redirect("viewissuedbook")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_book_view(request, id):
    book_obj = models.Book.objects.filter(id=id)
    if book_obj.exists():
        # Updating the is_deleted boolean to True for specified book
        book_obj = book_obj.first()
        book_obj.is_deleted = True
        book_obj.save()

        messages.success(request, "Book deleted successfully")
        return redirect("viewbook")
    messages.warning(request, "Book does not exist")
    return redirect("viewbook")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_book_view(request, id):
    instance = models.Book.objects.get(id=id)
    if request.method == "POST":
        # Updating the information for specified book
        form = forms.UpdateBookDetails(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Book Updated Successfully")
            return redirect("viewbook")  # Redirect to a success URL
    else:
        form = forms.UpdateBookDetails(instance=instance)
    return render(request, "library/updatebook.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_student_view(request, id):
    student_obj = models.StudentExtra.objects.filter(user_id=id)
    if student_obj.exists():
        # Updating the is_deleted boolean to True for specified Student
        student_obj = student_obj.first()
        student_obj.is_deleted = True
        student_obj.save()
        messages.success(request, "Student deleted successfully")
        return redirect("viewstudent")
    messages.warning(request, "Student does not exist")
    return redirect("viewstudent")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_student_view(request, id):
    instance = models.User.objects.get(id=id)
    student = models.StudentExtra.objects.get(user_id=id)
    if request.method == "POST":
        # Updating the Information of specified Student
        form = forms.UpdateStudentDetails(request.POST, instance=instance)
        if form.is_valid():
            student.branch = form.cleaned_data["branch"]
            student.save()
            form.save()
            messages.success(request, "Student Updated Successfully")
            return redirect("viewstudent")
    else:
        form = forms.UpdateStudentDetails(
            instance=instance, initial={"branch": student.branch}
        )
    return render(request, "library/updatestudent.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def search_book_view(request):
    query = request.GET.get("q")

    if query:
        # Perform search operation (e.g., filter objects based on query)
        results = models.Book.objects.filter(title__contains=query, is_deleted=False)
        authors = models.Author.objects.filter(name__contains=query)

        for author in authors:
            results = results | author.books.filter(is_deleted=False)

        # Adding the details of the Books found from search query
        serialized_data = get_book_serialized_data(results)
        return render(request, "library/viewbook.html", {"books": serialized_data})
    return redirect("viewbook")


def logout_view(request):
    # Logout User
    logout(request)
    return redirect("adminlogin")
