from mock import patch

from .base import (
    BaseWebTest,
    user_admin_mock
)

from .factories import (
    CategoryFactory,
    FlisTopicFactory,
    NeedFactory
)


class CatalogueTests(BaseWebTest):

    def setUp(self):
        self.category = CategoryFactory()
        self.flis_topic = FlisTopicFactory()

    @patch('eea_frame.middleware.requests')
    def test_need_add(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'need_urgent': True,
        })
        url = self.reverse('catalogue_add', kind='need')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category.handle,
            flis_topics__exact=self.flis_topic.handle,
            subject=data['subject'],
            description=data['description'],
            contact_person=data['contact_person'],
            email=data['email'],
            url__startswith=data['url'],
            institution=data['institution'],
            country=data['country'],
            need_urgent=True,
            kind='need',
            status='open',
            draft=False,
        )

    @patch('eea_frame.middleware.requests')
    def test_need_add_draft(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        need_factory_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
        })
        data = {'categories': need_factory_data['categories'],
                'flis_topics': need_factory_data['flis_topics'],
                'status': 'open',
                'save': 'draft'}
        url = self.reverse('catalogue_add', kind='need')
        self.app.post(url, self.normalize_data(data)).follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category,
            flis_topics__exact=self.flis_topic,
            draft=True,
            status='draft'
        )

    @patch('eea_frame.middleware.requests')
    def test_need_from_draft_to_open(self, mock_requests):
        mock_requests.get.return_value = user_admin_mock
        need = NeedFactory(categories=[self.category],
                           flis_topics=[self.flis_topic],
                           user_id='admin',
                           draft=True,
                           status='draft')
        need_data = NeedFactory.attributes(extra={
            'categories': [self.category],
            'flis_topics': [self.flis_topic],
            'status': 'draft'
        })
        url = self.reverse('catalogue_edit', kind='need', pk=need.pk)
        resp = self.app.get(url)
        form = resp.forms['catalogue-form']
        self.populate_fields(form, self.normalize_data(need_data))
        form.submit().follow()
        self.assertObjectInDatabase(
            model='Catalogue',
            pk=1,
            categories__exact=self.category,
            flis_topics__exact=self.flis_topic,
            draft=False,
            status='open',
        )
