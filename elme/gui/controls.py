from back import BackgroundHandler
from traitsui.editors.boolean_editor import BooleanEditor
from traitsui.editors.instance_editor import InstanceEditor
from traitsui.editors.list_editor import ListEditor
from traitsui.editors.range_editor import RangeEditor
from traitsui.editors.table_editor import TableEditor
from traitsui.editors.text_editor import TextEditor
from traitsui.item import Item


def instance(name, view=None, **kwargs):
    return Item(name=name,
                style='custom',
                editor=InstanceEditor(
                view=view,
                ),
                show_label=False,
                **kwargs
                )


def button(name, **kwargs):
    return Item(name=name,
                show_label=False,
                **kwargs
                )


def readonly(name, checkbox=False, format_func=None, format_str=None, **kwargs):
    if checkbox:
        return Item(name=name,
                    editor=BooleanEditor(),
                    enabled_when='0',
                    **kwargs
                    )
    else:
        item = Item(name=name,
                    # editor=TextEditor(format_func=format_func),
                    style='readonly',
                    **kwargs
                    )
        if format_func or format_str:
            item.editor = TextEditor(format_func=format_func,
                                     format_str=format_str)
        return item


def tabs(name, **kwargs):
    '''
    page_name
    '''
    return Item(name=name,
                editor=ListEditor(
                use_notebook=True,
                dock_style='fixed',
                #                                view=view,
                **kwargs
                ),
                show_label=False,
                style='custom',
                )


class TesterHandler (BackgroundHandler):
    def loop(self):
        ''
        self.info.object.measure()


def topview(view):
    view.buttons = ['Undo', 'Revert', 'OK', 'Cancel']
    view.kind = 'live'
    view.resizable = True
#    view.handler = TesterHandler()
    return view


def table(name, **kwargs):
    return                  Item(name=name,
                                 editor=TableEditor(
                                 auto_size=False,
                                 editable=False,
                                 configurable=False,
                                 # selection_mode='row',
                                 ),
                                 style='readonly',
                                 **kwargs
                                 )


def slider(name, low=0, high=100, is_float=True):
    return Item(name=name,
                editor=RangeEditor(
                                    mode='slider',
                                    low=low,
                                    high=high,
                                    is_float=is_float,
                                    ),
                style='custom',
                )
