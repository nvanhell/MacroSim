import wx
import threading

import matplotlib as mpl
#mpl.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


class MainFrame(wx.Frame):
    def __init__(self, parent, number_of_goods):
        wx.Frame.__init__(self, parent, title="Simulation", size=(1600, 900))
        self.Move(50, 50)

        self.tool_bar = ToolBar(self)

        self.splitter = wx.SplitterWindow(self)
        self.two_graph_panel = TwoGraphPanel(self.splitter)
        self.control_panel = ControlPanel(self.splitter)

        self.splitter.SplitHorizontally(self.two_graph_panel, self.control_panel)
        self.splitter.SetMinimumPaneSize(80)
        self.splitter.SetSashGravity(0.99)
        self.splitter.SetSashPosition(9999, redraw=True)
        self.splitter.SetSashInvisible()


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.start_button = wx.Button(self, -1, "Start", size=(60, 40), pos=(5, 10))
        self.start_button.Bind(wx.EVT_BUTTON, self.start_stop)

        self.config_button = wx.Button(self, -1, "Edit", size=(80, 40), pos=(5, 10))
        self.config_button.Bind(wx.EVT_BUTTON, self.config)

        self.sizer.Add(self.start_button)
        self.sizer.Add(self.config_button)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def start_stop(self, event):
        import main
        if not main.simulation.simulation_on:
            self.start_button.SetLabel("Stop")
            main.simulation.simulation_on = True
            t = threading.Thread(target=main.simulation.main_loop)
            t.start()
        else:
            self.start_button.SetLabel("Start")
            main.simulation.simulation_on = False

    def config(self, event):
        pass
        # Unfinished
        #config_panel = ConfigPanel(None)
        #config_panel.Show()

# Unfinished
class ConfigPanel(wx.Panel):
    def __init__(self, parent):
        pass

    def on_save(self, event):
        pass



class ToolBar:
    def __init__(self, parent):
        self.tool_bar = parent.CreateToolBar()
        self.labels = [['GDP', 'Consumption', 'Investment', 'Unemployment', 'Matches'],
                       ['Price', 'Quantity']]
        self.combo_macro = wx.ComboBox(self.tool_bar, size=(100, 20), style=wx.CB_READONLY, choices=self.labels[0])
        self.combo_macro.Bind(wx.EVT_COMBOBOX, self.set_graph)
        self.tool_bar.AddControl(self.combo_macro)

        self.combo_goods = wx.ComboBox(self.tool_bar, size=(100, 20), style=wx.CB_READONLY, choices=self.labels[1])
        self.combo_goods.Bind(wx.EVT_COMBOBOX, self.set_graph)
        self.tool_bar.AddControl(self.combo_goods)

        self.tool_three = self.tool_bar.AddControl(wx.Button(self.tool_bar, label='Test'))
        self.tool_bar.Realize()

        self.graph_type = 0
        self.graph_number = 0

    def set_graph(self, event):
        if event.GetId() == self.combo_macro.GetId():
            self.graph_type = 0
            for i, choice in enumerate(self.labels[0]):
                if self.combo_macro.GetValue() == choice:
                    self.graph_number = i
        if event.GetId() == self.combo_goods.GetId():
            self.graph_type = 1
            for i, choice in enumerate(self.labels[1]):
                if self.combo_goods.GetValue() == choice:
                    self.graph_number = i
        # Update the graphs unless the simulation is running or unless the first period hasn't been reached
        import main
        if not main.simulation.simulation_on and main.simulation.period != 0:
            main.simulation.display_graphs()


class TwoGraphPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.graph_sizer = wx.BoxSizer(wx.VERTICAL)
        self.graphs = [Graph(self), Graph(self)]
        for graph in self.graphs:
            self.graph_sizer.Add(graph, 1, wx.EXPAND | wx.ALL, border=-1)
        self.SetSizer(self.graph_sizer)
        self.Layout()


class Graph(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(50, 50))

        self.figure = Figure(facecolor="grey")
        self.canvas = Canvas(self, wx.ID_ANY, self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color="gray")
        self.axes.set_ylabel("y")
        self.figure.set_tight_layout(True)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, border=2)
        self.SetSizer(self.sizer)

        self.good_colours = ['red', 'green', 'blue', 'purple', 'orange', 'gold', 'pink', 'turquoise', 'violet']

    def draw(self, label, x, y):
        self.axes.clear()
        #self.axes.hold(True)
        self.axes.set_ylabel(label)
        self.axes.set_xlabel('Time')
        self.axes.grid(True, color="grey")
        if type(y[0]) != list:
            self.axes.plot(x, y, color="grey")
        else:
            for i, y_ in enumerate(y):
                self.axes.plot(x, y_, color=self.good_colours[i])
        self.canvas.draw()


class SettingsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, title="simulation options")
        self.panel = wx.Panel(self)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.column_sizer = wx.BoxSizer(wx.VERTICAL)

        # Creating text controls to gather input
        self.population_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.goods_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.firm_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.population_text = wx.StaticText(self, label="Population: ")
        self.population_input = wx.TextCtrl(self, value="10000")
        self.goods_text = wx.StaticText(self, label="Number of goods: ")
        self.goods_input = wx.TextCtrl(self, value="5")
        self.firm_text = wx.StaticText(self, label="Number of firms: ")
        self.firm_input = wx.TextCtrl(self, value="1")
        self.population_sizer.Add(self.population_text)
        self.population_sizer.Add(self.population_input)
        self.goods_sizer.Add(self.goods_text)
        self.goods_sizer.Add(self.goods_input)
        self.firm_sizer.Add(self.firm_text)
        self.firm_sizer.Add(self.firm_input)
        self.column_sizer.Add(self.population_sizer)
        self.column_sizer.Add(self.goods_sizer)
        self.column_sizer.Add(self.firm_sizer)

        # Printing sim 1,2 header
        self.sim_text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sim_1_text = wx.StaticText(self, label="                Sim 1                         ")
        self.sim_2_text = wx.StaticText(self, label="Sim 2")
        self.sim_text_sizer.Add(self.sim_1_text)
        self.sim_text_sizer.Add(self.sim_2_text)
        self.column_sizer.Add(self.sim_text_sizer)

        # Creating rows of inputs for the two sims
        self.labels = [" Placeholder 1 ", " Placeholder 2 ", " Placeholder 3 "]
        self.defaults = [0.5, 0.2, 0.4]
        self.settings_input = [[i for i in range(len(self.labels))],
                               [i for i in range(len(self.labels))]]

        for i, label in enumerate(self.labels):
            self.item_label = wx.StaticText(self, label=label)
            self.settings_input[0][i] = wx.TextCtrl(self, value=str(self.defaults[i]))
            self.settings_input[1][i] = wx.TextCtrl(self, value=str(self.defaults[i]))
            self.row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.row_sizer.Add(self.settings_input[0][i], 0, wx.ALL, 0)
            self.row_sizer.Add(self.settings_input[1][i], 0, wx.ALL, 0)
            self.row_sizer.Add(self.item_label, 0, wx.ALL, 0)
            self.column_sizer.Add(self.row_sizer)

        self.save_button = wx.Button(self, label='Start', size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.on_start, self.save_button)
        self.column_sizer.AddSpacer(10)
        self.column_sizer.Add(self.save_button)

        self.main_sizer.Add(self.column_sizer)
        self.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

    def on_start(self, event):
        import main
        main.create_main_frame(int(self.population_input.GetValue()),
                               int(self.goods_input.GetValue()), int(self.firm_input.GetValue()))
        self.Destroy()
