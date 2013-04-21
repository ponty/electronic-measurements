from entrypoint2 import entrypoint
from traits.has_traits import HasPrivateTraits
from traits.trait_types import Str
from traitsui.item import Item
from traitsui.view import View


class InputBox (HasPrivateTraits):
    message = Str
    input = Str
    view = View([
        Item(name='message',
             show_label=False,
             style='readonly',
             ),
        Item(name='input',
             show_label=False,
             ),
    ],
        buttons=['OK', 'Cancel'],
        kind='modal',
        width=400,
#        height=600,
        resizable=True,
    )


def inputbox(message='', default='', title='Message',
             parent=None):
    msg = InputBox(message=message, input=default)
    x = msg.edit_traits()
    if not x.result:
        return

    return msg.input


@entrypoint
def main():
    print inputbox(message='x=', default='22')
