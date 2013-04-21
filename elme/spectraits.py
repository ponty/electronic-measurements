from formating import format_ufloat, format_amper, format_volt, format_ohm, \
    format_ohmE12, format_analog, format_beta, format_farad, format_percent
from elme.formating import format_time, format_watt, format_charge
from traits.has_traits import HasTraits
from traits.trait_handlers import TraitType
from traits.trait_types import Float, Bool, Any, default_text_editor, Enum, Int, \
    Str
from uncertainties import ufloat, Variable, AffineScalarFunc


class UFloat (TraitType):
    """ Defines a trait whose value must be ufloat.
    """
    # The function to use for evaluating strings to this type:
    evaluate = ufloat

    # The default value for the trait:
    default_value = ufloat((0, 0))

    # A description of the type of value this trait accepts:
    info_text = 'a float with uncertainty'

    def validate(self, object, name, value):
        """ Validates that a specified value is valid for this trait.
        """
#        if none(value):
#            return value
        if isinstance(value, AffineScalarFunc):
            return value

        if isinstance(value, float):
            return ufloat((value, 0))

        if isinstance(value, int):
            return ufloat((value, 0))

        self.error(object, name, value)


class UBeta (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_beta)
        ed.format_func = f
        return ed


class UCurrent (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_amper)
        ed.format_func = f
        return ed


class UVoltage (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_volt)
        ed.format_func = f
        return ed


class UResistance (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_ohm)
        ed.format_func = f
        return ed


class UCharge (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_charge)
        ed.format_func = f
        return ed


class Resistance (Float):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_ohm
        return ed


class Percentage (Float):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_percent
        return ed


class Time (Float):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_time
        return ed


class Capacitance (Float):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_farad
        return ed


class UCapacitance (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_farad)
        ed.format_func = f
        return ed


class Analog (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_analog
        return ed


class ResistanceE12 (Float):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)
        ed.format_func = format_ohmE12
        return ed


def PinTrait(typ='all'):
    analog = ['A%s' % x for x in range(6)]
    digital = ['D%s' % x for x in range(14)]
#    if typ == 'analog':
#        return Enum(analog)
#    if typ == 'digital':
#        return Enum(digital)

    return Enum(['GND'] + digital + analog)


class PinInfo(HasTraits):
    pin_nr = PinTrait()
    R = Float()
    node = Any()
    group = Str()


class UPower (UFloat):
    def create_editor(self):
        """ Returns the default traits UI editor for this type of trait.
        """
        ed = default_text_editor(self, Variable)

        def f(x):
            return format_ufloat(x, format_func=format_watt)
        ed.format_func = f
        return ed
