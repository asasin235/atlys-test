def convert_price(price_str):
    """
    Converts a price string to a float by removing currency symbols and commas.

    Args:
        price_str (str): The price string to convert.

    Returns:
        float: The converted price.
    """
    return float(price_str.replace('₹', '').replace(',', ''))