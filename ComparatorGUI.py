import wx
import Comparator


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame("FF XIV - Price Comparator", (150, 150), (600, 500))
        frame.SetMinSize((600, 500))
        frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, title, pos, size):
        super().__init__(None, title=title, pos=pos, size=size)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        region_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.region_label = wx.StaticText(panel, label="Region:")
        region_sizer.Add(self.region_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.region_text = wx.TextCtrl(panel)
        self.region_text.Bind(wx.EVT_TEXT, self.on_text_change)
        region_sizer.Add(self.region_text, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(region_sizer, 0, wx.ALL | wx.EXPAND, 5)

        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_label = wx.StaticText(panel, label="File:")
        file_sizer.Add(self.file_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.file_picker = wx.FilePickerCtrl(panel, wildcard="CSV files (*.csv)|*.csv",
                                             style=wx.FLP_USE_TEXTCTRL | wx.FLP_FILE_MUST_EXIST)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_text_change)
        file_sizer.Add(self.file_picker, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.search_button = wx.Button(panel, label="Search")
        self.search_button.Disable()
        sizer.Add(self.search_button, 0, wx.ALL | wx.EXPAND, 5)
        self.search_button.Bind(wx.EVT_BUTTON, self.on_search)

        self.item_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.item_list.InsertColumn(0, 'ID', width=50)
        self.item_list.InsertColumn(1, 'Item', width=150)
        self.item_list.InsertColumn(2, 'Data Center', width=150)
        self.item_list.InsertColumn(3, 'World', width=100)
        self.item_list.InsertColumn(4, 'Lowest price', width=100)
        self.item_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        sizer.Add(self.item_list, 2, wx.ALL | wx.EXPAND, 5)

        self.dc_list = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.dc_list.InsertColumn(0, 'Data Center', width=150)
        self.dc_list.InsertColumn(1, 'World', width=100)
        self.dc_list.InsertColumn(2, 'Lowest price', width=100)
        sizer.Add(self.dc_list, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)

    def on_item_selected(self, event):
        item_index = event.GetIndex()
        item_id = int(self.item_list.GetItemText(item_index, 0))

        selected_item = next((item for item in self.items if item.itemId == item_id), None)

        if selected_item:
            self.dc_list.DeleteAllItems()
            for dc in selected_item.dc:
                self.dc_list.Append((dc.dataCenter, dc.worldName, str(dc.price)))

    def on_text_change(self, event):
        region_filled = bool(self.region_text.GetValue().strip())
        file_selected = bool(self.file_picker.GetPath().strip())
        if region_filled and file_selected:
            self.search_button.Enable()
        else:
            self.search_button.Disable()

    def on_search(self, event):
        try:
            self.item_list.Show()
            self.dc_list.Show()
            self.Layout()

            self.dc_list.DeleteAllItems()

            region = self.region_text.GetValue()
            file_path = self.file_picker.GetPath()

            progress_dialog = wx.ProgressDialog("Loading", "Please wait while data is being loaded...",
                                                maximum=100, parent=self,
                                                style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

            progress_dialog.Update(0, "Starting...")

            self.items = Comparator.price_comparator(region, file_path)
            self.item_list.DeleteAllItems()

            total_items = len(self.items)
            for index, item in enumerate(self.items):
                self.item_list.Append((
                    str(item.itemId),
                    item.Name,
                    item.region.dataCenter,
                    item.region.worldName,
                    str(item.region.price)
                ))
                progress_percent = int((index + 1) / total_items * 100)
                progress_dialog.Update(progress_percent, f"Loading {index + 1} of {total_items} items...")

            progress_dialog.Destroy()
        except Exception as e:
            wx.MessageBox(f"Wystąpił błąd podczas wyszukiwania: {str(e)}", "Błąd", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
