from tkinter import *
from PIL import Image, ImageTk
from datetime import *
import time, threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from main import *
import yfinance as yf

fig, ax = plt.subplots()
clicked_ticker = None
ticker = 'AAPL'

# Color Scheme
textcolor = "#edf2ed"
background = "#080e07"
primary = "#3ab536"
secondary = "#188514"
secondary2 = "#292C29"
accent = "#0cb106"


class Dashboard:
    
    
    def __init__(self, window):

        # Function to add a task to the list
        def add_ticker():
            ticker_text = self.ticker_entry.get()
            if ticker_text:
                self.ticker_list.insert(END, ticker_text)
                self.ticker_entry.delete(0, END)  # Clear the entry field

        # Function to remove a selected task from the list
        def remove_ticker():
            selected_item = self.ticker_list.curselection()
            if selected_item:
                self.ticker_list.delete(selected_item[0])
        
        def handle_click(event):
            global clicked_ticker
            # Get the index of the clicked item
            clicked_index = self.ticker_list.curselection()[0]
            # You can implement your desired action here based on the clicked index
            # (e.g., open a dialog to edit the task, mark it as complete)
            # print("Ticker", clicked_index + 1, "clicked!")
            print(clicked_ticker)
            # Get the value of ticker
            
            clicked_ticker = self.ticker_list.get(clicked_index)
            assign(clicked_ticker)
        

        def assign(clicked):
            global ticker
            data  = clicked
            try:
                ticker = data
            except IndexError:
                ticker = 'BTC-USD'
                
        

                
            

        self.window = window
        self.window.title('NYSE Prediction Dashboard')
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.state('zoomed')
        self.window.configure(bg=background)
        self.window.resizable(0, 0)


        # Header
        self.header = Frame(self.window, bg=accent)
        self.header.place(width=w, height="%d" % (h * 0.08))

        self.logout_text = Button(self.header, text='Logout', bg='#32cf8e', font=("", 13, "bold"), bd=0, fg='white',
                                  cursor='hand2', activebackground='#32cf8e')
        self.logout_text.place(x="%d" % (w - 200), y="%d" % (h * 0.025))


        # Sidebar
        self.sidebar = Frame(self.window, bg=primary)
        self.sidebar.place(x=0, y=0, width="%d" % (w * 0.2), height="%d" % (h))

            #Time and Date
        self.date_time = Label(self.window , background=accent, fg=textcolor)
        self.date_time.place(x='%d' % (w * 0.075), y=15)
        self.show_time()

            #Profile
        self.brandName = Label(self.sidebar, text='John Doe', bg=primary, font=("", 15, "bold") , fg=textcolor)
        self.brandName.place(x='%d' % (w * 0.075) , y='%d' % (h * 0.2))

            #Dashboard
        self.dashboard_text = Button(self.sidebar, text='Dashboard', bg=accent, font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground=secondary2, width='%d' % (w * 0.0125), height='%d' % (h * 0.002), pady=2, fg=textcolor)
        self.dashboard_text.place(x=0, y='%d' % (h * 0.3))

            # Manage
        self.manage_text = Button(self.sidebar, text='Manage', bg=accent, font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground=secondary2, width='%d' % (w * 0.0125), height='%d' % (h * 0.002), pady=2, fg=textcolor)
        self.manage_text.place(x=0, y='%d' % (h * 0.37))

            # Settings
        self.settings_text = Button(self.sidebar, text='Settings', bg=accent, font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground=secondary2, width='%d' % (w * 0.0125), height='%d' % (h * 0.002), pady=2, fg=textcolor)
        self.settings_text.place(x=0, y='%d' % (h * 0.44))

            # Exit
        self.exit_text = Button(self.sidebar, text='Exit', bg=accent, font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground=secondary2, width='%d' % (w * 0.0125), height='%d' % (h * 0.002), pady=2, command=self.window.quit, fg=textcolor)
        self.exit_text.place(x=0, y='%d' % (h * 0.51))


        # Body Frame 1 (For Graphs)
        self.bodyFrame = Frame(self.window, bg='#ffffff')
        self.bodyFrame.place(x="%d" % (w * 0.212), y="%d" % (h * 0.1), width="%d" % (w * 0.5125), height="%d" % (h * 0.5))

        canvas4 = FigureCanvasTkAgg(fig, self.bodyFrame)


        # Body Frame 2 (For Current Information)
        self.bodyFrame2 = Frame(self.window, bg=secondary2)
        self.bodyFrame2.place(x="%d" % (w * 0.212), y="%d" % (h * 0.625), width="%d" % (w * 0.25), height="%d" % (h * 0.33))

        self.price = Label(self.bodyFrame2, text='Current Price:', bg=secondary2, font=("", 30, "bold"), fg=textcolor)
        self.price2 = Label(self.bodyFrame2, text="current_price", bg=secondary2, font=("", 35, "bold"), fg=textcolor)
        self.price.pack(anchor="center")



        # Body Frame 3 (For Predicted Action)
        self.bodyFrame3 = Frame(self.window, bg=secondary2)
        self.bodyFrame3.place(x="%d" % (w * 0.475), y="%d" % (h * 0.625), width="%d" % (w * 0.25), height="%d" % (h * 0.33))

        self.action = Label(self.bodyFrame3, text='Call-to-Action:', bg=secondary2, font=("", 30, "bold"), fg=textcolor)
        self.action2 = Label(self.bodyFrame3, text="pre_action", bg=secondary2, font=("", 45, "bold"), fg=textcolor)
        self.action.pack(anchor="center")
        


        # Body Frame 4 (For Predicted Trend)
        self.bodyFrame4 = Frame(self.window, bg=secondary2)
        self.bodyFrame4.place(x="%d" % (w * 0.738), y="%d" % (h * 0.625), width="%d" % (w * 0.25), height="%d" % (h * 0.33))

        self.trend = Label(self.bodyFrame4, text='Predicted Trend:', bg=secondary2, font=("", 30, "bold"), fg=textcolor)
        self.trend2 = Label(self.bodyFrame4, text="pre_trend", bg=secondary2, font=("", 45, "bold"), fg=textcolor)
        self.trend.pack(anchor="center")

        

        # Body Frame 5 (For Tickers)
        self.bodyFrame5 = Frame(self.window, bg=secondary2)
        self.bodyFrame5.place(x="%d" % (w * 0.738), y="%d" % (h * 0.1), width="%d" % (w * 0.25), height="%d" % (h * 0.5))

        self.Ticker_Label = Label(self.bodyFrame5, text="Portfolio", font=("", 30, "bold"), bg=secondary2, fg=textcolor)
        self.Ticker_Label.pack(anchor="center", side="top")

            # update ticker
        self.ticker_entry = Entry(self.bodyFrame5, width=50, border=3, bg=background, fg=textcolor, cursor="dot", selectbackground="#585f58")
        self.ticker_entry.pack(pady=20)

            # add ticker button
        self.add_button = Button(self.bodyFrame5, text="Add Ticker", command=add_ticker, width=50, border=1, fg=textcolor, background=secondary, bd=0)
        self.add_button.pack()


            #* List Box With Click Binding 
        self.ticker_list = Listbox(self.bodyFrame5, width=50, bg=background, fg=textcolor, selectforeground="black", selectbackground="#ffffff")
        self.ticker_list.bind("<Button-1>", handle_click)
        
        self.ticker_list.pack(pady=20)
        
            # delete ticker button
        self.remove_button = Button(self.bodyFrame5, text="Remove Ticker", command=remove_ticker, width=50, border=1, fg=textcolor, background=secondary, bd=0)
        self.remove_button.pack()

        # ! Packing
        self.trend2.pack(anchor='center', expand=True)
        
        self.action2.pack(anchor='center', expand=True)
        
        self.price2.pack(anchor='center', expand=True)

        canvas4.get_tk_widget().pack(fill="both", expand=False)


        

        def constant_update():
                    
                while True:
                    # print(clicked_ticker)
                    # print(ticker)
                    price="{price:.2f}"
                    stock_data = update_info(ticker)
                    action = stock_data[0]
                    trend = stock_data[1]
                    current_price = price.format(price = stock_data[2])
                    self.trend2.config(text=action)
                    self.action2.config(text=trend)
                    self.price2.config(text=current_price)

                    #Graphs
                    # Chart 1: Line chart of price from the year
                    # Prepare data for plotting
                    
                    
                    data = stock_data[3]
                    dates = data.index.to_numpy()
                    closing_prices = data["Close"].to_numpy()

                    
                    # ! Create a hidden matplotlib figure
                    # Create the plot
                    # Customize the plot
                    ax.set_title(f"{ticker} Historical Closing Prices")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Closing Price")
                    ax.grid(True)  # Add gridlines for better readability
                    # ax.legend()  # Add legend

                    ax.plot(dates, closing_prices, label=f"{ticker} Closing Price")

                    canvas4.draw()

                    ax.clear()
                    
                    time.sleep(8)

                    



        



        global thread
        thread = threading.Thread(target=constant_update)
        thread.start()

        






        
        



        
    #! FUNCTIONS
    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%d/%m/%Y')
        set_text = f" {self.time} \n {self.date}"
        self.date_time.configure(text=set_text, font=("", 13, "bold"), bd=0, bg="white", fg="black")
        self.date_time.after(100, self.show_time)

    def exit_window(self):
        thread.join()
        self.window.quit()
    
    
    



def main():
    window = Tk()
    Dashboard(window)
    window.mainloop()

if __name__=='__main__':
    main()
