from urllib.parse import urlencode

from immoweb_scraper.constants import POSTAL_CODES, PROVINCES


class ImmoWebURLBuilder:
    def __init__(self):
        self.base_url = "https://www.immoweb.be/en/search/apartment/{}?"
        self.default_params = {
            "countries": "BE",
            "hasKitchenSetup": "true",
            "isAnInvestmentProperty": "false",
            "isFurnished": "false",
            "maxBedroomCount": "4",
            "minBedroomCount": "2",
            "minSurface": "90",
            "postalCodes": ",".join(POSTAL_CODES),
            "provinces": ",".join(PROVINCES),
            "page": "1",
        }

    def for_rent(self, **kwargs):
        # Set specific parameters for rental
        rent_params = {"priceType": "MONTHLY_RENTAL_PRICE", "maxPrice": "1400"}
        # Merge default parameters with rental-specific ones
        params = {**self.default_params, **rent_params, **kwargs}
        return self.base_url.format("for-rent") + urlencode(params)

    def for_sale(self, **kwargs):
        # Set specific parameters for sale
        sale_params = {"priceType": "SALE_PRICE"}
        # Merge default parameters with sale-specific ones
        params = {**self.default_params, **sale_params, **kwargs}
        return self.base_url.format("for-sale") + urlencode(params)
