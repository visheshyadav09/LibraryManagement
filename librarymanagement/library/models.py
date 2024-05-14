from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=40)
    student_number = models.CharField(max_length=100, unique=True, default="123456")
    is_deleted = models.BooleanField(default=False)

    # used in issue book
    def __str__(self):
        return self.user.first_name + "[" + str(self.student_number) + "]"

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=False, default=0)
    death_year = models.IntegerField(null=False, default=0)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=100, default="Title")
    book_number = models.CharField(max_length=100, unique=True, default="123456")
    authors = models.ManyToManyField(Author, related_name="books")
    subject = models.TextField(null=True)
    bookshelves = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title) + "[" + str(self.book_number) + "]"


def get_expiry():
    pass


class IssuedBook(models.Model):
    statuschoice = [
        ("Issued", "Issued"),
        ("Returned", "Returned"),
    ]
    book_issued_number = models.CharField(max_length=100, default="123456")
    student_number = models.CharField(max_length=100, default="123456")
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField()
    status = models.CharField(max_length=20, choices=statuschoice, default="Issued")

    def __str__(self):
        return self.book_issued_number


class ChargeIssuedBook(models.Model):
    statuschoice = [("Paid", "Paid"), ("Pending", "Pending")]
    issuedbook = models.ForeignKey(
        IssuedBook, on_delete=models.CASCADE, related_name="issuesbook"
    )
    charge = models.IntegerField(default=0, null=False)
    status = models.CharField(max_length=20, choices=statuschoice, default="Pending")
