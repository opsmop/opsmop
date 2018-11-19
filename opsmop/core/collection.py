
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.scope import Scope
import jinja2

class Collection(Resource):

    """
    A collection is a type of resources that can contain other Resources.

    Example:

        Collection(
            Resource(...),
            Resource(...)
        )

    OR

        Collection(*resource_list)

    
    key-value arguments are available after the resource declaration, like:
    Collection(*resource_list, when=is_os_x)
    """

    def __init__(self, *args, **kwargs):
        self.setup(items=args, **kwargs)

    def fields(self):
        return Fields(
            self,
            items = Field(kind=list, of=Resource),
        )

        conditions = conditions[:]
        if obj.when:
            conditions.append(obj.when)
        parent.child_scope(obj)

    def _claim(self, resource):
        """
        Used by walk_children, this marks each object as being a child of the parent scope
        """
        my_scope = self.scope()
        kid_scope = my_scope.deeper_scope_for(resource)
        resource.set_scope(kid_scope) # ?

    def _on_walk(self, context):
        """
        A hook that fires on traversal of each object inside walk_children.
        """
        pass

    def get_children(self, mode):
        """
        Returns child objects, mode may be 'resources' or 'handlers'
        """
        # TODO: use constants
        return self.items

    def _check_conditions(self, resource, context, apply=False):
        try:
            res = resource.conditions_true(context)
            return res
        except jinja2.exceptions.UndefinedError:
            # allow templates to fail in check mode only
            if not apply:
                raise
            else:
                return True

    def walk_children(self, items=None, context=None, mode=None, check=False, apply=False, fn=None):

        """
        A relatively complex iterator used by Executor() code.
        Walks the entire object tree calling fn() on each element.
        
        items - the kids to start the iteration with
        context - a Context() object for callback tracking
        mode - 'resources' or 'handlers'
        check/apply - whether check and apply mode are running
        fn - the function to call on each object
        """

        # TODO: break into smaller functions

        assert items is not None
        assert context is not None
        assert mode in [ 'resources', 'handlers' ]
        assert fn is not None

        self._on_walk(context)
        items_type = type(items)
 
        if items is None:
            return
       
        if issubclass(items_type, Collection):
            self._claim(items)
            proceed = self._check_conditions(items, context, apply)
            if not proceed:
                context.on_skipped(items)
                return
            else:
                items.walk_children(items=items.get_children(mode), mode=mode, context=context, fn=fn, check=check, apply=apply)

        elif issubclass(items_type, Resource):
            self._claim(items)
            proceed = self._check_conditions(items, context, apply)
            if not proceed:
                context.on_skipped(items)
                return
            else:
                return fn(items)

        elif items_type == list:
            for x in items:        
                self._claim(x)
                proceed = self._check_conditions(x, context, apply)
                if not proceed:
                    context.on_skipped(x)
                else:
                    if issubclass(type(x), Collection):
                        x.walk_children(items=x.get_children(mode), mode=mode, context=context, fn=fn, check=check, apply=apply)
                    else:
                        fn(x)

        elif items_type == dict:
            for (k,v) in items.items():
                self._claim(v)
                proceed = self._check_conditions(v, context, apply)
                if not proceed:
                    context.on_skipped(v)
                else:
                    if issubclass(type(v), Collection):
                        items.walk_children(items=v.get_children(mode), mode=mode, context=context, fn=fn, check=check, apply=apply)
                    else:
                        v.handles = k
                        fn(v)





