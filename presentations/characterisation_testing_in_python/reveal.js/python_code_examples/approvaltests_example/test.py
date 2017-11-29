from unittest import main, TestCase

from approvaltests import verify
from approvaltests.reporters import GenericDiffReporterFactory


class TestFormat(TestCase):
    def test_format(self):
        received_string = 'Hello {}'.format('World!')
        reporter = GenericDiffReporterFactory().get('meld')
        verify(received_string, reporter)


if __name__ == '__main__':
    main()
