import factory
from live_catalogue import models
from flis_metadata.common.models import EnvironmentalTheme, Country


class CategoryFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Category
    FACTORY_DJANGO_GET_OR_CREATE = ('handle', 'title',)

    handle = 'projects'
    title = 'Projects'


class CountryFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Country

    iso = factory.Sequence(lambda n: 'c%d' % n)
    name = factory.Sequence(lambda n: 'country_%d' % n)


class FlisTopicFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.FlisTopic
    FACTORY_DJANGO_GET_OR_CREATE = ('handle', 'title',)

    handle = 'early-warning'
    title = 'Early warning'


class ThemeFactory(factory.DjangoModelFactory):

    FACTORY_FOR = EnvironmentalTheme
    FACTORY_DJANGO_GET_OR_CREATE = ('title',)

    title = 'Air pollution'


class CatalogueFactory(factory.DjangoModelFactory):

    FACTORY_FOR = models.Catalogue

    subject = 'Catalogue'
    description = 'Catalogue description'

    contact_person = 'John Doe'
    email = 'john.doe@eaueweb.ro'
    url = 'http://john.doe.eaudeweb.ro'
    institution = 'EEA'
    country = factory.SubFactory(CountryFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for categ in extracted:
                self.categories.add(categ)

    @factory.post_generation
    def flis_topics(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for flis_topic in extracted:
                self.flis_topics.add(flis_topic)

    @factory.post_generation
    def themes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for theme in extracted:
                self.themes.add(theme)


class NeedFactory(CatalogueFactory):

    kind = models.Catalogue.NEED


class OfferFactory(CatalogueFactory):

    kind = models.Catalogue.OFFER
