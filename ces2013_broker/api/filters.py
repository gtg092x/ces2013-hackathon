'''
Created on Dec 11, 2012

@author: matt
'''
from rest_framework.filters import BaseFilterBackend
import shlex
class ODataFilterBackend(BaseFilterBackend):
    """
    A filter backend that uses django-filter.
    """
    

    def __init__(self):
        pass;

    def get_filter_class(self, view):
        """
        Return the django-filters `FilterSet` used to filter the queryset.
        """
        
        pass;
    
    @classmethod
    def iterate_coupling(cls,queryset,couple):
        """
        returns query dict modified
        """
        ors = couple.split(" or ")
        for _or in ors:
            include,exclude=ODataFilterBackend.iterate_coupling_ands(queryset,couple);
            queryset=queryset.filter(**include)
            if exclude and len(exclude):
                queryset=queryset.exclude(**exclude)
        return queryset;
    
    @classmethod
    def iterate_coupling_ands(cls,queryset,couple):
        """
        returns query dict modified
        """
        ands = couple.split(" and ")
        out_dict = {};
        negate_dict = {};
        for _and in ands:
            k,v,negation = ODataFilterBackend.process_pair(_and);
            if negation:
                negate_dict[k]=v;
            else:
                out_dict[k]=v;
        return out_dict,negate_dict
        pass;
    
    @classmethod
    def process_pair(cls,pair):
        """
        returns query dict modified
        """

        negate = "Not" in pair
        #args = pair.split(" ")
        
        
        args = shlex.split(pair)
        
        k = args[0];
            
        if negate:
            op = args[2]
            val = args[3]
        else:
            op = args[1]
            val = args[2]
        op = op.lower()
        if k.startswith("indexof"):
            params = k[8:-1].split(",") 
            k = params[0]
            val = params[1]
            negate = "eq" in op 
            return k+"__contains",val,negate
        
        if op == "ne":
            negate = True
        elif op =="gt":
            k+="__gt"
        elif op =="ge":
            k+="__gte"
        elif op =="le":
            k+="__lte"
        elif op =="lt":
            k+="__lt"
        elif op =="contains":
            k+="__contains"
        elif op =="in":
            """
            NOT PROPER ODATA
            """            
            
            kv = val
            val = k
            k = kv;
            k+="__contains"
        
            
        return k,val,negate
        
    

    def filter_queryset(self, request, queryset, view):
        
        if("$filter" not in request.GET):
            return queryset;
        
        filter_str = request.GET["$filter"]
        queryset = ODataFilterBackend.iterate_coupling(queryset, filter_str)

        return queryset
