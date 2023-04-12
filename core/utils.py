import logging

from django.test.runner import DiscoverRunner

from rest_framework.test import APIRequestFactory
from drf_spectacular.plumbing import build_mock_request


def build_swagger_mock_request(method, path, view, *args, **kwargs):
    view.request = getattr(APIRequestFactory(), method.lower())(path=path)
    return build_mock_request(method, path, view, *args, **kwargs)


class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        logging.disable(logging.CRITICAL)
        return super().run_tests(test_labels, extra_tests, **kwargs)
