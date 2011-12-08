import datetime

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class AlphabeticFilterSpec(ChoicesFilterSpec):
    """
    Adds filtering by first char (alphabetic style) of values in the admin
    filter sidebar. Set the alphabetic filter in the model field attribute
    'alphabetic_filter'.

    my_model_field.alphabetic_filter = True
    """

    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(AlphabeticFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)
        self.lookup_kwarg = '%s__istartswith' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        values_list = model.objects.values_list(f.name, flat=True)
        # getting the first char of values
        self.lookup_choices = list(set(val[0] for val in values_list if val))
        self.lookup_choices.sort()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': val.upper()}
    def title(self):
        return _('%(field_name)s that starts with') % \
            {'field_name': self.field.verbose_name}

# registering the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'alphabetic_filter', False),
                                   AlphabeticFilterSpec))

class YearFilterSpec(ChoicesFilterSpec):
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(YearFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)
        self.lookup_kwarg = '%s__year' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        values_list = model.objects.dates(f.name, 'year')
        # getting the first char of values
        self.lookup_choices = list(set(val.year for val in values_list))
        self.lookup_choices.sort()
    
    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': val}
            
    def title(self):
        return _('%(field_name)s whose year is') % \
            {'field_name': self.field.verbose_name}
            
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'year_filter', False),
                                   YearFilterSpec))

class YearWithCloseHistoryFilterSpec(ChoicesFilterSpec):
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(YearWithCloseHistoryFilterSpec, self).__init__(f, request, params,
                                                    model, model_admin)
        
        # same as in YearFilterSpec
        self.year_lookup_kwarg = '%s__year' % f.name
        self.month_lookup_kwarg = '%s__month' % f.name
        self.day_lookup_kwarg ='%s__day' % f.name
        self.gte_loookup_kwargs = '%s__gte' % f.name
        self.lte_loookup_kwargs = '%s__lte' % f.name
        
        self.lookup_active = reduce(lambda x, y: x or y, [f.name in key for key in request.GET.keys()], False)

        # collect all distinct years&months
        values_list = set((val.year, val.month) for val in model.objects.dates(f.name, 'month'))
        self.lookup_choices = list(values_list)        
        self.lookup_choices.sort(reverse=True)
        
        # custom functionality taken from django's DateFieldFilterSpec
        self.field_generic = '%s__' % self.field.name
        self.date_params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])

        today = datetime.date.today()
        one_week_ago = today - datetime.timedelta(days=7)
        today_str = isinstance(self.field, models.DateTimeField) and today.strftime('%Y-%m-%d 23:59:59') or today.strftime('%Y-%m-%d')

        self.links = (
            (_('Any date'), {}),
            (_('Today'), {'%s__year' % self.field.name: str(today.year),
                       '%s__month' % self.field.name: str(today.month),
                       '%s__day' % self.field.name: str(today.day)}),
            (_('Past 7 days'), {'%s__gte' % self.field.name: one_week_ago.strftime('%Y-%m-%d'),
                             '%s__lte' % f.name: today_str}),
            (_('This month'), {'%s__year' % self.field.name: str(today.year),
                             '%s__month' % f.name: str(today.month)})
        )
    
    def choices(self, cl):
        for title, param_dict in self.links:
            yield {'selected': self.date_params == param_dict,
                   'query_string': cl.get_query_string(param_dict, [self.field_generic]),
                   'display': title}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.year_lookup_kwarg: val[0], self.month_lookup_kwarg: val[1]}),
                    'display': '%s/%s' % (val[1], val[0])}
            
    def title(self):
        return self.field.verbose_name
            
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'year_with_close_history_filter', False),
                                   YearWithCloseHistoryFilterSpec))

class FkFilterSpec(ChoicesFilterSpec):
    """
    Unfortunately, it is not possible currently to use foreign keys in list filter
    of the admin website. list_filter=['city__country'] doesn't work.
    
    This filter spec tries to workaround this problem.
    
    It is also possible to have 2 filters for a foreign-key field but it requires
    to add a dummy field to the model. Set the fk_filterspec dictionnary on this
    dummy field and add 'fk':'real-field' to the dict.
    
    One needs to addd lookup_allowed(self, key_name) method in model admin which returns
    True if the key is the foreign key (ie. author__article__name).
    
    Credit goes to http://djangosnippets.org/snippets/2194/ by luc_j
    """
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(FkFilterSpec, self).__init__(f, request, params, model, model_admin, field_path)
        
        # ******* Extract parameters ********
        the_args = f.fk_filterspec.copy() 
        #The field of the related table
        fk_field = the_args['fk_field'] 
        
        #The name in the related table to use as label in the choices
        label = the_args.pop('label', '')
        
        #a title: by default the lookup arg
        self.filter_title = the_args.pop('title', '')
        
        #the foreign key field. By default the field the filter is assigned
        fk = the_args.pop('fk', f.name) 
        
        # ******* Build the filter definition ********
        
        self.lookup_kwarg = '{0}__{1}'.format(fk, fk_field)
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_labels = {}
        #get the list of values
        values_list = model.objects.values_list(self.lookup_kwarg, flat=True)
        #get the 
        if label:
            label_field = '{0}__{1}__{2}'.format(fk, fk_field, label)
        else:
            label_field = '{0}__{1}'.format(fk, fk_field)
        labels = model.objects.values_list(label_field, flat=True)
        for (v, l) in zip(values_list, labels):
            self.lookup_labels[v] = l
        self.lookup_choices = self.lookup_labels.keys()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': smart_unicode(self.lookup_labels[val])}
    
    def title(self):
        if self.filter_title:
            return self.filter_title
        else:
            return super(FkFilterSpec, self).title()

FilterSpec.filter_specs.insert(0,(lambda f: len(getattr(f, 'fk_filterspec', [])), FkFilterSpec))
