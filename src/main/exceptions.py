class ProductOutOfStockError(Exception):
    """
    An exception occurs due to an attempt to add
    more goods to the cart than there actually is.
    """

    def __init__(self, message="This product is no longer in stock in such quantity"):
        self.message = message
        super().__init__(self.message)
        
        
class MaxCartItemError(Exception):
    """
    An exception occurs due to an attempt to add
    more than 10 instances of product to the cart.
    """

    def __init__(self, message="You cannot add more than 10 instances of the product to the cart"):
        self.message = message
        super().__init__(self.message)
        