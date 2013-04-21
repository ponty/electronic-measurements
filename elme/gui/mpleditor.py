# from enthought.traits.api import Any
# from enthought.traits.ui.wx.basic_editor_factory import BasicEditorFactory
# from enthought.traits.ui.wx.editor import Editor
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from traits.trait_types import Any
from traitsui.basic_editor_factory import BasicEditorFactory
from traitsui.editor import Editor
import matplotlib
import wx
# from traitsui.editor import Editor

# We want matplotlib to use a wxPython backend
matplotlib.use('WXAgg')


class _MPLFigureEditor(Editor):

    scrollable = True
    panel = Any
    border_size = 0
    layout_style = 0

    def init(self, parent):
        self.control = self._create_canvas(parent)
#        self.set_tooltip()
    sizer = Any
    mpl_control = Any

    def update_editor(self):
        # matplotlib commands to create a canvas
        panel = self.panel
#        if self.sizer:
#            self.sizer.Destroy()
#            self.sizer=None
        if not self.sizer:
            self.sizer = sizer = wx.BoxSizer(wx.VERTICAL)
            panel.SetSizer(sizer)

        sizer = self.sizer
#        sizer=panel.GetSizer()
        if self.value:
            sizer.Clear(deleteWindows=1)
#            if self.mpl_control:
#                self.mpl_control.Destroy()
            self.mpl_control = FigureCanvas(panel, -1, self.value)
            sizer.Add(self.mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
            toolbar = NavigationToolbar2Wx(self.mpl_control)
            sizer.Add(toolbar, 0, wx.EXPAND)
            self.value.canvas.SetMinSize((100, 100))
        panel.Layout()

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

#        self.value=Figure()
#        axes = self.value.add_subplot(111)
#        axes.plot([1,2,3],[3,2,1])
#        if self.value:
#            mpl_control = FigureCanvas(panel, -1, self.value)
#            sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
#            toolbar = NavigationToolbar2Wx(mpl_control)
#            sizer.Add(toolbar, 0, wx.EXPAND)
#            self.value.canvas.SetMinSize((100,100))

        self.panel = panel

        return panel


class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor
