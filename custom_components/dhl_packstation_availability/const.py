"""Constants for DHL Packstation Availability."""

from datetime import timedelta

DOMAIN = "dhl_packstation_availability"
BASE_URL = "https://www.dhl.de/int-postfinder/webservice/rest/v1/locationByPrimaryKeyPF/"
SCAN_INTERVAL = timedelta(minutes=15)

