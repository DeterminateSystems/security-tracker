from re import match
from re import search

from wtforms.validators import URL as URLValidator
from wtforms.validators import ValidationError

from tracker import db
from tracker.advisory import advisory_fetch_from_mailman
from tracker.model import Package
from tracker.model.advisory import advisory_regex
from tracker.model.cve import cve_id_regex
from tracker.model.cvegroup import pkgname_regex
from tracker.util import multiline_to_list

ERROR_ISSUE_ID_INVALID = u'Invalid issue.'
ERROR_INVALID_URL = u'Invalid URL {}.'


class ValidAdvisoryReference(object):
    def __call__(self, form, field):
        if not field.data:
            return

        form.advisory_content = advisory_fetch_from_mailman(field.data)
        if not form.advisory_content:
            raise ValidationError('Failed to fetch advisory')

        m = search(advisory_regex[1:-1], form.advisory_content)
        if not m:
            raise ValidationError('Failed to fetch advisory')

        found = m.group(1)
        if found != form.advisory_id:
            raise ValidationError('Advisory mismatched: {}'.format(found))


class ValidPackageName(object):
    def __init__(self):
        self.message = u'Unknown package.'

    def __call__(self, form, field):
        pass


class ValidPackageNames(object):
    def __init__(self):
        self.message = u'Unknown package {}.'

    def fail(self, pkgname):
        raise ValidationError(self.message.format(pkgname))

    def __call__(self, form, field):
        pass


class ValidIssue(object):
    def __init__(self):
        self.message = ERROR_ISSUE_ID_INVALID

    def __call__(self, form, field):
        if not match(cve_id_regex, field.data):
            raise ValidationError(self.message)


class ValidIssues(object):
    def __init__(self):
        self.message = u'Invalid issue {}.'

    def fail(self, issue):
        raise ValidationError(self.message.format(issue))

    def __call__(self, form, field):
        issues = multiline_to_list(field.data)
        for issue in issues:
            if not match(cve_id_regex, issue):
                self.fail(issue)


class ValidURLs(object):
    def __init__(self):
        self.message = ERROR_INVALID_URL
        self.regex = URLValidator().regex

    def fail(self, url):
        raise ValidationError(self.message.format(url))

    def __call__(self, form, field):
        urls = multiline_to_list(field.data)
        for url in urls:
            if not self.regex.match(url):
                self.fail(url)
