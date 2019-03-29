import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg
import wx
import wx.lib.scrolledpanel

class discussFigure(object):
    def __init__(self):
        pass

    def vote(self, vote_item1, vote_item2):
        total_width, n = 0.8, 2
        width = total_width / n
        x = (total_width - width) / 2

        plt.bar(x, vote_item1["value"],  width=width, label=vote_item1["name"])
        plt.bar(x + width, vote_item2["value"], width=width, label=vote_item2["name"])
        plt.legend()
        plt.show()

    def rollCall(self, present, late):
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
            return my_autopct
        labels = ["present", "late"]
        sizes = [present["value"], late["value"]]
        explode = (0, 0.1)
        plt.pie(sizes, explode=explode, labels=labels, autopct=make_autopct(sizes), shadow=True, startangle=90)
        plt.axis('equal') # Equal aspect ratio
        plt.show()

    def discussImage(self, image_path, word):
        def scale_bitmap(bitmap, width, height):
            image = wx.ImageFromBitmap(bitmap)
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
            result = wx.BitmapFromImage(image)
            return result
        class discussImageForm(wx.Frame):
            def __init__(self, parent, image_path, word):
                super(discussImageForm, self).__init__(parent, title = "討論", style=wx.DEFAULT_FRAME_STYLE, size=(300, 80))
                self.Maximize(True)
                ### variable ###

                ### layout ###
                self.panel = wx.Panel(self, wx.ID_ANY)
                mastersizer = wx.BoxSizer(wx.VERTICAL)
                bitmap = wx.Bitmap(image_path)
                bitmap = scale_bitmap(bitmap, 1200, 800)
                self.image = wx.StaticBitmap(self.panel, -1, bitmap)
                self.class_number = wx.StaticText(self.panel, label = word)
                self.class_number.SetFont(wx.Font(30, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
                
                # Additional object
                mastersizer.Add(self.image, 1, wx.ALIGN_CENTRE_HORIZONTAL)
                mastersizer.Add(self.class_number, 1, wx.ALIGN_CENTRE_HORIZONTAL)
                self.panel.SetSizer(mastersizer)
                self.Centre()
                self.Show()

                ### logic ###

                return

        app = wx.PySimpleApp()
        class_number_window = discussImageForm(None, image_path, word)
        class_number_window.Show()
        app.MainLoop()

