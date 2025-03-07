from assertpy import assert_that
import pytest


import bolt.project as project


class TestWrap:

    def test_raises_exception_if_accessed_attribute_is_not_found(self):
        obj = project._wrap({})
        with pytest.raises(AttributeError):
            assert_that(obj.foo).raises(AttributeError)

    def test_can_access_contents_as_objects(self):
        obj = project._wrap({
            'foo': 'bar',
            'project': {
                'name': 'baz'
            },
            'authors':[{ 'name': 'author', 'email': 'author@test.com' }],
            'dependencies': ['requests', 'flask']
        })
        assert_that(obj.foo).is_equal_to('bar')
        assert_that(obj.project.name).is_equal_to('baz')
        assert_that(obj.dependencies[1]).is_equal_to('flask')
        assert_that(obj.authors[0].name).is_equal_to('author')
