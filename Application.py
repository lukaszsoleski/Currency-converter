from tkinter import *
from tkinter import ttk
from definitions import Currency
from definitions import Flag
from definitions import CURRENCIES_FILE_PATH,APP_ICON
from tkinter import messagebox
from urllib.error import URLError, HTTPError
from decimal import *
import decimal
from data.net.CurrencyConverter import CurrencyConverter


class Application:
    def __init__(self, root):
        """
        :param root: Reference to root window
        """
        # Set root window
        self.root = root
        self.root.resizable(False,False)


        # Define title for the app
        self.root.title("Currency Converter")
        # Will hold Entry and and base currency list
        self.topFrame = Frame(self.root)
        self.topFrame.pack(padx=3, pady=2)

        # Bottom frame will store converted results
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(padx=3, pady=2, side=LEFT)

        # Declaration of the dictionary that will store conversion results in the variable Text widget
        self.converted_values = {}

        # Create widgets
        self.create_top_frame_widgets()
        self.create_bottom_frame_widgets()

        # Set styles
        self.configure_style()

        # Create CurrencyConverter instance

        self.converter = CurrencyConverter(file=CURRENCIES_FILE_PATH)

        # Try to download latest data
        self.update_converter()  #

        # Change label details
        self.details_text.set("Exchange rates as at {0}".format(self.converter.date))

        # Presets
        self.on_button_pressed()



    def update_converter(self):
        error_occurred = False
        try:
            self.converter.update_exchange_rates()
        except (URLError, HTTPError) as e:
            messagebox.showwarning(title="The latest data is not available",
                                   message="Unable to connect to the server."
                                           " Check the internet connection and status at https://api.fixer.io/latest")
            error_occurred = True
        else:
            # Keep the latest data
            self.converter.save_rates_to_file()
        if error_occurred:
            answer = messagebox.askokcancel(title="The latest data is not available",
                                   message="Would you like to load data from a file? ")
            if answer:
                try:
                    self.converter.load_rates_from_file()
                except IOError as e:
                    messagebox.showerror(title="Critical error",message=e)
                    self.root.destroy()
            else:
                self.root.destroy()


    def create_top_frame_widgets(self):
        # ====== Top frame ======:
        # Put the information labels
        ttk.Label(self.topFrame, text="amount").grid(row=0, column=0)
        ttk.Label(self.topFrame, text="base currency").grid(row=0, column=1)

        # Will hold the changing value stored in the entry
        self.entry_value = StringVar(self.topFrame, value="1")
        self.entry = ttk.Entry(self.topFrame, textvariable=self.entry_value, width=20)
        self.entry.grid(row=1, column=0)

        # Define variable that will bind to Combobox selected item
        self.selected_currency = StringVar()
        # Create Combobox widget
        self.currency_box = ttk.Combobox(self.topFrame,
                                         textvariable=self.selected_currency,
                                         state='readonly')

        # Respond when selection will be changed
        self.currency_box.bind('<<ComboboxSelected>>', lambda x: self.on_button_pressed())
        # Specify readonly selection
        items = tuple(x.value for x in Currency)
        self.currency_box['values'] = items
        # Set default value
        self.currency_box.set(Currency.PLN.value)
        self.currency_box.grid(row=1, column=1)

        # Define button that will run conversion function
        self.convert_button = ttk.Button(self.topFrame, text="convert", command=lambda: self.on_button_pressed())

        self.convert_button.grid(row=1, column=2)

        # update this variable after fetching data
        self.details_text = StringVar(self.topFrame, value='Currency rates data not found')
        ttk.Label(self.topFrame, textvariable=self.details_text).grid(row=2, columnspan=2)


    def create_bottom_frame_widgets(self):


        i = 0
        for val in Currency:
            val = val.value

            # Create flag images
            flag = PhotoImage(file=Flag[val].value)
            label = ttk.Label(self.bottomFrame, image=flag)
            # keep reference in label so image won't get garbage collected
            label.photo = flag
            label.grid(row=i, column=0)

            # Create Text widgets that will display conversion results
            text = Text(self.bottomFrame, width=25, height=1)
            text.grid(row=i, column=1)
            text.insert('1.0', '')
            text['state'] = DISABLED
            # Insert text widgets into dictionary so as later display conversion results
            self.converted_values[val] = text

            ttk.Label(self.bottomFrame, text=val).grid(row=i, column=2)
            i += 1

    def configure_style(self):
        pass # todo configure styles

    def on_button_pressed(self,args=None):
        try:
            self.update()
        except ValueError as e:
            messagebox.showerror(title="Value Error",message=e)

    def update(self):
        amount = self.entry_value.get()
        if self.isNumber(amount):
            if float(amount) <= 0:
                raise ValueError("Oops! You have an empty wallet...")
        else:
            raise ValueError("The entered text in not a number")
        base = self.selected_currency.get()
        for k in Currency:

            k = k.value

            # Set widget reference to a temporary variable
            text = self.converted_values[k]

            # Make the Text widget editable
            text['state'] = NORMAL

            # Delete content of Text widget
            text.delete('1.0', END)

            # Make conversion
            result = self.converter.convert(amount, base, k)
            # Round result and display in widget

            result = result.quantize(Decimal("0.01"),decimal.ROUND_FLOOR)
            text.insert('1.0', result)
            # Prevent editing
            text['state'] = DISABLED


    def isNumber(self,value):
      try:
          float(value)
          return True
      except ValueError:
          return False


def main():
    root = Tk()
    app = Application(root)

    root.mainloop()


main()
