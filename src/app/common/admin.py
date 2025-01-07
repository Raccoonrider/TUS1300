class ChainedPrepopulatedFieldsMixin:
    chained_prepopulated_fields = tuple()

    def get_prepopulated_field_key(self, field):
        model_name = self.model.__class__.__name__
        return f'{model_name}-adminform-{field}'


    def save_form(self, request, form, change:bool):

        for field in self.chained_prepopulated_fields:
            request.session[self.get_prepopulated_field_key(field)] = form.data.get(field)
        
        return super().save_form(request, form, change)


    def get_form(self, request, obj = ..., change = ..., **kwargs):
        form = super().get_form(request, obj, change, **kwargs)


        for field in self.chained_prepopulated_fields:
            value = request.session.get(self.get_prepopulated_field_key(field))
            if value:
                form.base_fields[field].initial = value

        return form