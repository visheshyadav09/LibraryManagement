from django import forms
from django.contrib.auth.models import User
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={"rows": 3, "cols": 30})
    )


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ["branch", "student_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student_number"].initial = None


class BookForm(forms.ModelForm):
    number_of_books = forms.IntegerField()

    class Meta:
        model = models.Book
        fields = ["title", "number_of_books"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].initial = None


class IssuedBookForm(forms.Form):
    # to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    book_issued_number = forms.ModelChoiceField(
        queryset=models.Book.objects.filter(is_deleted=False).exclude(
            book_number__in=models.IssuedBook.objects.filter(
                status="Issued"
            ).values_list("book_issued_number", flat=True)
        ),
        empty_label="Name and Book number",
    )
    student_number = forms.ModelChoiceField(
        queryset=models.StudentExtra.objects.filter(is_deleted=False),
        empty_label="Name and Student number",
    )
    return_date = forms.DateField(
        label="Select Date to Return", widget=forms.DateInput(attrs={"type": "date"})
    )

    def __init__(self, *args, **kwargs):
        super(IssuedBookForm, self).__init__(*args, **kwargs)
        self.fields["book_issued_number"].label_from_instance = (
            self.label_from_book_intance
        )
        self.fields["student_number"].label_from_instance = (
            self.label_from_student_instance
        )

    def label_from_book_intance(self, obj):
        return f"{obj.title} ({obj.book_number})"

    def label_from_student_instance(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} ({obj.student_number})"


class UpdateBookDetails(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["title", "bookshelves", "subject"]


class UpdateStudentDetails(forms.ModelForm):
    branch = forms.CharField()

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "username", "branch"]
