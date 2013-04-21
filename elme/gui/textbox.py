from entrypoint2 import entrypoint
from traits.has_traits import HasPrivateTraits
from traits.trait_types import Str
from traitsui.editors.code_editor import CodeEditor
from traitsui.item import Item
from traitsui.view import View


class TextBox (HasPrivateTraits):
    message = Str

    view = View([
        Item(name='message',
             show_label=False,
             style='readonly',
             editor=CodeEditor(),
             ),

    ],
        buttons=['OK'],
#        kind='modal',
        width=800,
        height=600,
        resizable=True,
    )


def textbox(message='', title='Text',
            parent=None):
    msg = TextBox(message=str(message))
    x = msg.edit_traits()
    if not x.result:
        return

message = '''
item
item
item
item
item
item
item
item
item
item
item
item
item
item
item
'''


@entrypoint
def main():
    textbox(message=message)
