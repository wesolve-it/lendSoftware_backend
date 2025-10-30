import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import Article, Category, Size, Booked, DrivingProfile


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class DrivingProfileType(DjangoObjectType):
    class Meta:
        model = DrivingProfile


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
    description = graphene.String()


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
    street = graphene.String()
    local = graphene.String()


class Query(graphene.ObjectType):
    articles = graphene.List(ArticleType)
    categories = graphene.List(CategoryType)
    sizes = graphene.List(SizeType)
    bookings = graphene.List(BookedType)
    driving_profiles = graphene.List(DrivingProfileType)

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

    @staticmethod
    def resolve_driving_profiles(root, info, **kwargs):
        return DrivingProfile.objects.all()


class UpdateInvoiceDownloaded(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    booked = graphene.Field(BookedType)

    def mutate(self, info, id):
        try:
            booked = Booked.objects.get(pk=id)
            booked.invoice_downloaded = True
            booked.save()
            return UpdateInvoiceDownloaded(booked=booked)
        except Booked.DoesNotExist:
            raise Exception("Booked entry not found")



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
    local = graphene.String()
    street = graphene.String()
    note = graphene.String()

    class Arguments:
        start_date = graphene.Date()
        end_date = graphene.Date()
        booking_date = graphene.Date()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        size_id = graphene.Int()
        local = graphene.String()
        street = graphene.String()
        note = graphene.String()

    @staticmethod
    def mutate(self, info, start_date, end_date, booking_date, email, first_name, last_name, phone_number, size_id,
               local, street, note):
        booking = Booked(startDate=start_date, endDate=end_date, bookingDate=booking_date, email=email,
                         firstName=first_name, lastName=last_name, phoneNumber=phone_number, size_id=size_id,
                         local=local, street=street, note=note)
        booking.save()

        return CreateBooking(
            id=booking.id,
            startDate=booking.startDate,
            end_date=booking.endDate,
            booking_date=booking.bookingDate,
            first_name=booking.firstName,
            last_name=booking.lastName,
            size_id=booking.size_id,
            local=booking.local,
            street=booking.street,
            note=booking.note
        )


class Mutation(graphene.ObjectType):
    create_booking = CreateBooking.Field()
    update_invoice_downloaded = UpdateInvoiceDownloaded.Field()