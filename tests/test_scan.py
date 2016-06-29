import time

from tests import TestBase
from w3af_api_client import Scan
from w3af_api_client.utils.exceptions import APIException


class TestScan(TestBase):
    @classmethod
    def __sleep(cls):
        time.sleep(1)
        try:
            cls.__sleep_count += 1
        except AttributeError:
            cls.__sleep_count = 1

        if cls.__sleep_count == 60:
            print('.', end='')
            cls.__sleep_count = 0

    @classmethod
    def __wait_scan_to_start(cls, scan):
        while True:
            try:
                scan.get_status()
                break
            except APIException as e:
                if e.args[0] != 'Failed to retrieve scan status. Received HTTP response code 500. ' \
                                'Message: "Can NOT call get_run_time before start()."':
                    raise
                cls.__sleep()

    @classmethod
    def __wait_scan_to_end(cls, scan):
        while scan.get_status()['status'] == 'Running':
            cls.__sleep()

    def test_scan(self):
        profile = self._get_profile('fast_scan')

        scan = Scan(self.connection)
        scan.start(profile, self.targets)

        self.__wait_scan_to_start(scan)
        self.__wait_scan_to_end(scan)

        for finding in scan.get_findings():
            status_code, found = self.connection.send_request(finding.resource_href)
            self.assertEqual(status_code, 200)

        scan.cleanup()
