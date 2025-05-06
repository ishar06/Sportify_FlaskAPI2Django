from .models import Address

def user_address(request):
    address = None
    if request.user.is_authenticated:
        try:
            # First try to get the default address
            address = Address.objects.filter(user=request.user, is_default=True).first()
            if not address:
                # If no default address exists, get the first address
                address = Address.objects.filter(user=request.user).first()
        except Address.DoesNotExist:
            pass
    return {'address': address}
