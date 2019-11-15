# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import

class IvtsError(Exception):
    """A custom core Ivts exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(IvtsError, self).__init__(message)


class IvtsDomainError(IvtsError):
    """Exception for invalid domain
    """
    def __init__(self, message=None):
        message = 'Bad domain' \
            if not message else message

        super(IvtsDomainError, self).__init__(message)


class IvtsNonConvergentDomainError(IvtsError):
    """Exception for domain invalid because of CDF nonconvergence
    """
    def __init__(self, message=None):
        message = 'Domain does not allow CDF convergence' \
            if not message else message

        super(IvtsNonConvergentDomainError, self).__init__(message)


class IvtsNotImplemented(IvtsError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(IvtsNotImplemented, self).__init__(message)


class IvtsAPIError(IvtsError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Ivts API'
        else:
            message = 'Http response error from Ivts API. {0}'.format(message)

        super(IvtsAPIError, self).__init__(message)


class IvtsApiAuthError(IvtsAPIError):
    """A custom exception for API authentication errors"""
    pass


class IvtsMissingDependency(IvtsError):
    """A custom exception for missing dependencies."""
    pass


class IvtsWarning(Warning):
    """Base warning for Ivts."""


class IvtsUserWarning(UserWarning, IvtsWarning):
    """The primary warning class."""
    pass


class IvtsSkippedTestWarning(IvtsUserWarning):
    """A warning for when a test is skipped."""
    pass


class IvtsDeprecationWarning(IvtsUserWarning):
    """A warning for deprecated features."""
    pass
