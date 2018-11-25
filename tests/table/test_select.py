from ..base import DBTestCase
from ..example_project.tables import Band


class TestSelect(DBTestCase):

    def test_query_all_columns(self):
        self.insert_row()

        response = Band.select().run_sync()
        print(f'response = {response}')

        self.assertDictEqual(
            response[0],
            {
                'id': 1,
                'name': 'Pythonistas',
                'manager': 'Ash',
                'popularity': 1000
            }
        )

    def test_query_some_columns(self):
        self.insert_row()

        response = Band.select('name').run_sync()
        print(f'response = {response}')

        self.assertDictEqual(
            response[0],
            {'name': 'Pythonistas'}
        )

    def test_where_like(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            Band.name.like('Python%')
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}]
        )

    def test_where_greater_than(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            Band.popularity > 1000
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Rustaceans'}]
        )

    def test_where_greater_equal_than(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            Band.popularity >= 1000
        ).order_by(
            'name'
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}, {'name': 'Rustaceans'}]
        )

    def test_where_less_than(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            Band.popularity < 1000
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Wizards'}]
        )

    def test_where_less_equal_than(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            Band.popularity <= 1000
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}, {'name': 'Wizards'}]
        )

    def test_where_and(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            (Band.popularity <= 1000) & (Band.name.like('Python%'))
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}]
        )

    def test_where_or(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            (Band.name == 'Rustaceans') | (Band.name == 'Wizards')
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Rustaceans'}, {'name': 'Wizards'}]
        )

    def test_multiple_where(self):
        """
        Test that chaining multiple where clauses works results in an AND.
        """
        self.insert_rows()

        query = Band.select(
            'name'
        ).where(
            Band.name == 'Rustaceans'
        ).where(
            Band.manager == 'Sally'
        )

        response = query.run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Rustaceans'}]
        )
        self.assertTrue(
            'AND' in query.__str__()
        )

    def test_complex_where(self):
        """
        Test a complex where clause - combining AND, and OR.
        """
        self.insert_rows()

        response = Band.select(
            'name'
        ).where(
            ((Band.popularity == 2000) & (Band.manager == 'Sally')) |
            ((Band.popularity == 10) & (Band.manager == 'Gordon'))
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Rustaceans'}, {'name': 'Wizards'}]
        )

    def test_limit(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).order_by(
            'name'
        ).limit(
            1
        ).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}]
        )

    def test_first(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).order_by(
            'name'
        ).first().run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            {'name': 'Pythonistas'}
        )

    def test_order_by_ascending(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).order_by(
            'name'
        ).limit(1).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Pythonistas'}]
        )

    def test_order_by_decending(self):
        self.insert_rows()

        response = Band.select(
            'name'
        ).order_by(
            '-name'
        ).limit(1).run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'Wizards'}]
        )

    def test_count(self):
        self.insert_rows()

        response = Band.select().where(
            Band.name == 'Pythonistas'
        ).count().run_sync()

        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'count': 1}]
        )

    def test_distinct(self):
        self.insert_rows()
        self.insert_rows()

        response = Band.select('name').where(
            Band.name == 'Pythonistas'
        ).distinct().run_sync()

        self.assertTrue(response == [{'name': 'Pythonistas'}])
