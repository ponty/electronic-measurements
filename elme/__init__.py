# from traits.has_traits import HasTraits
# from traits.trait_types import Str, Instance, DelegatesTo
#
# class Parent(HasTraits):
#    first_name = Str
#    last_name  = Str
#
# class Child(HasTraits):
#    first_name = Str
#    last_name  = Str('x')
#    father     = Instance(Parent)
#    mother     = Instance(Parent)
#
# tony  = Parent(first_name='Anthony', last_name='Jones')
# alice = Parent(first_name='Alice', last_name='Smith')
#
# cls=Child
# print cls.class_traits()
# cls.traits()()
# cls.remove_trait('last_name')
# cls.add_class_trait('last_name',   DelegatesTo('father'))
# sally = cls( first_name='Sally', father=tony)
# print 1,sally.last_name
# sally.remove_trait('last_name')
# sally.add_trait('last_name',   DelegatesTo('father'))
#
# sally.sync_trait('last_name',sally.father)
# tony.last_name='cc'
# print 2,sally.last_name
