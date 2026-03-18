# Copyright (c) 2016 Cisco Systems
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from requests import exceptions as rexc

from aim.agent.aid.universes.aci import error
from aim.agent.aid.universes import errors
from aim.tests import base

from apicapi import exceptions


class TestACIError(base.BaseTestCase):

    def setUp(self):
        super(TestACIError, self).setUp()
        self.apic_handler = error.APICAPIErrorHandler()
        self.base_handler = error.APICErrorHandler()

    def test_analyze_exception_no_cookie(self):
        self.assertEqual(
            errors.SYSTEM_CRITICAL,
            self.apic_handler.analyze_exception(
                exceptions.ApicResponseNoCookie(request='')))

    def test_analyze_exception_no_response(self):
        self.assertEqual(
            errors.SYSTEM_TRANSIENT,
            self.apic_handler.analyze_exception(
                exceptions.ApicHostNoResponse(url='')))

    def test_analyze_exception_invalid_transaction(self):
        self.assertEqual(
            errors.OPERATION_CRITICAL,
            self.apic_handler.analyze_exception(
                exceptions.ApicInvalidTransactionMultipleRoot()))

    def test_analyze_exception_mo_not_supported(self):
        self.assertEqual(
            errors.OPERATION_CRITICAL,
            self.apic_handler.analyze_exception(
                exceptions.ApicManagedObjectNotSupported(mo_class='')))

    def test_analyze_exception_session_not_logged_in(self):
        self.assertEqual(
            errors.SYSTEM_TRANSIENT,
            self.apic_handler.analyze_exception(
                exceptions.ApicSessionNotLoggedIn()))

    def test_analyze_exception_not_ok(self):
        for err_code in self.base_handler.APIC_OBJECT_CRITICAL:
            self.assertEqual(
                errors.OPERATION_CRITICAL,
                self.apic_handler.analyze_exception(
                    exceptions.ApicResponseNotOk(
                        request='', status='400', reason='',
                        err_text='', err_code=str(err_code))))

        for err_code in self.base_handler.APIC_OBJECT_TRANSIENT:
            self.assertEqual(
                errors.OPERATION_TRANSIENT,
                self.apic_handler.analyze_exception(
                    exceptions.ApicResponseNotOk(
                        request='', status='400', reason='',
                        err_text='', err_code=str(err_code))))

        for err_code in self.base_handler.APIC_SYSTEM_TRANSIENT:
            self.assertEqual(
                errors.SYSTEM_TRANSIENT,
                self.apic_handler.analyze_exception(
                    exceptions.ApicResponseNotOk(
                        request='', status='400', reason='',
                        err_text='', err_code=str(err_code))))

        self.assertEqual(
            errors.OPERATION_CRITICAL,
            self.apic_handler.analyze_exception(
                exceptions.ApicResponseNotOk(
                    request='', status='403', reason='',
                    err_text='', err_code='')))

        self.assertEqual(
            errors.SYSTEM_TRANSIENT,
            self.apic_handler.analyze_exception(
                exceptions.ApicResponseNotOk(
                    request='', status='500', reason='',
                    err_text='', err_code='')))

        self.assertEqual(
            errors.UNKNOWN,
            self.apic_handler.analyze_exception(
                exceptions.ApicResponseNotOk(
                    request='', status='300', reason='',
                    err_text='', err_code='')))

    def test_analyze_exception_permission_denied(self):
        # APIC returns "user <name> does not have domain access to config Mo"
        # as HTTP 400 with code 170, not 403, so the 403 branch never sees it.
        # Transient, not critical, on purpose: OPERATION_CRITICAL would take
        # the object out of the hash-tree diff and leave it parked until the
        # hourly error-state recovery, turning a momentary refusal into a long
        # stall. The visibility comes from the ERROR log, not from the class.
        for err_code in self.base_handler.APIC_PERMISSION_TRANSIENT:
            self.assertEqual(
                errors.OPERATION_TRANSIENT,
                self.apic_handler.analyze_exception(
                    exceptions.ApicResponseNotOk(
                        request='', status='400', reason='',
                        err_text='', err_code=str(err_code))))

    def test_analyze_exception_request(self):
        self.assertEqual(
            errors.SYSTEM_TRANSIENT,
            self.apic_handler.analyze_exception(rexc.Timeout()))
        self.assertEqual(
            errors.SYSTEM_TRANSIENT,
            self.apic_handler.analyze_exception(rexc.ConnectionError()))
        self.assertEqual(
            errors.OPERATION_CRITICAL,
            self.apic_handler.analyze_exception(rexc.InvalidURL()))
        self.assertEqual(
            errors.OPERATION_CRITICAL,
            self.apic_handler.analyze_exception(rexc.URLRequired()))
        self.assertEqual(
            errors.OPERATION_TRANSIENT,
            self.apic_handler.analyze_exception(rexc.RequestException()))
        self.assertEqual(
            errors.UNKNOWN,
            self.apic_handler.analyze_exception(Exception()))
