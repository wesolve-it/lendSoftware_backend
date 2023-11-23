import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import Article, Category, Size, Booked


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class SizeType(DjangoObjectType):
    class Meta:
        model = Size


class BookedType(DjangoObjectType):
    class Meta:
        model = Booked


class ArticleInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    category_id = graphene.Int()


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    category_name = graphene.String()


class SizeInput(graphene.InputObjectType):
    id = graphene.ID()
    value = graphene.Int()
    label = graphene.String()
    pricePerDay = graphene.Decimal()
    serialNumber = graphene.String()
    article_id = graphene.Int()


class BookedInput(graphene.InputObjectType):
    id = graphene.ID()
    startDate = graphene.Date()
    endDate = graphene.Date()
    bookingDate = graphene.Date()
    firstName = graphene.String()
    lastName = graphene.String()
    email = graphene.String()
    phoneNumber = graphene.String()
    size_id = graphene.Int()


class Query(graphene.ObjectType):
    articles = graphene.List(ArticleType)
    categories = graphene.List(CategoryType)
    sizes = graphene.List(SizeType)
    bookings = graphene.List(BookedType)

    @staticmethod
    def resolve_articles(root, info, **kwargs):
        return Article.objects.all()

    @staticmethod
    def return_categories(root, info, **kwargs):
        return Category.objects.all()

    @staticmethod
    def resolve_sizes(root, info, **kwargs):
        return Size.objects.all()

    @staticmethod
    def resolve_bookings(root, info, **kwargs):
        return Booked.objects.all()


class CreateBooking(graphene.Mutation):
    id = graphene.Int()
    startDate = graphene.Date()
    end_date = graphene.Date()
    booking_date = graphene.Date()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    size_id = graphene.Int()

    class Arguments:
        startDate = graphene.Date()
        end_date = graphene.Date()
        booking_date = graphene.Date()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        size_id = graphene.Int()

    @staticmethod
    def mutate(self, info, startDate, end_date, booking_date, email, first_name, last_name, phone_number, size_id):
        booking = Booked(startDate=startDate, endDate=end_date, bookingDate=booking_date, email=email,
                         firstName=first_name, lastName=last_name, phoneNumber=phone_number, size_id=size_id)
        booking.save()

        return CreateBooking(
            id=booking.id,
            startDate=booking.startDate,
            end_date=booking.endDate,
            booking_date=booking.bookingDate,
            first_name=booking.firstName,
            last_name=booking.lastName,
            size_id=booking.size_id
        )


class Mutation(graphene.ObjectType):
    create_booking = CreateBooking.Field()
