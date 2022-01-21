from django.core.exceptions import ValidationError

"""def invoicing_first_name_validation(invoicing_first_name, self):
    if invoicing_first_name is not None:
            if not invoicing_first_name.isalpha():
                self.add_error('invoicing_first_name', 'No puede ingresar valores numéricos')"""

def invoicing_first_name_validation(self, *args, **kwargs):
        if invoicing_first_name is not None:
            if not invoicing_first_name.isalpha():
                self.add_error('invoicing_first_name', 'No puede ingresar valores numéricos')

