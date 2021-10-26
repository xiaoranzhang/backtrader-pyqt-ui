###############################################################################
#
# Copyright (C) 2021 - Skinok
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QGraphicsView, QComboBox, QLabel
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import DockArea, Dock

import sys
sys.path.append('C:/perso/trading/anaconda3/finplot')
import finplot as fplt

import backtrader as bt

class UserInterface:

    #########
    #  
    #########
    def __init__(self):

        # Qt 
        self.app = QApplication([])
        self.win = QMainWindow()

        # Resize windows properties
        self.win.resize(1600,1000)
        self.win.setWindowTitle("Docking charts example for finplot")
        
        # Set width/height of QSplitter
        self.win.setStyleSheet("QSplitter { width : 20px; height : 20px; }")

        # Docks
        self.createDocks()

    #########
    #  
    #########
    def createDocks(self):
        self.area = DockArea()
        self.win.setCentralWidget(self.area)

        # Create Chart widget      
        self.dock_chart = Dock("dock_chart", size = (1000, 500), closable = False, hideTitle=True, )
        self.area.addDock(self.dock_chart, position='above')

        # Create Summary widget 
        self.dock_summary = Dock("Strategy Summary", size = (200, 100), closable = False)
        self.area.addDock(self.dock_summary, position='left', relativeTo=self.dock_chart)

        # Create Trade widget 
        self.dock_trades = Dock("Trades", size = (1000, 200), closable = False)
        self.area.addDock(self.dock_trades, position='bottom')

        # Create Transaction widget 
        #self.dock_transactions = Dock("Transactions", size = (1000, 200), closable = False)
        #self.area.addDock(self.dock_transactions, position='bottom', relativeTo=self.dock_trades)

        # Create Order widget 
        self.dock_orders = Dock("Orders", size = (1000, 200), closable = False)
        self.area.addDock(self.dock_orders, position='below', relativeTo=self.dock_trades)



    #########
    #  
    #########
    def createTransactionsUI(self, trades):
        
        self.transactionTableWidget = QtGui.QTableWidget(self.dock_trades)
        self.transactionTableWidget.setRowCount(len(trades)) 
        self.transactionTableWidget.setColumnCount(4)

        labels = [ "Date","Size", "Price", "Value" ]
        self.transactionTableWidget.setHorizontalHeaderLabels( labels )

        row = 0
        for date,values in trades:
            #for trade in trades:
            self.transactionTableWidget.setItem(row,0,QtGui.QTableWidgetItem( date.strftime("%Y/%m/%d %H:%M:%S") ))
            self.transactionTableWidget.setItem(row,1,QtGui.QTableWidgetItem( str(values[0][0]) ))
            self.transactionTableWidget.setItem(row,2,QtGui.QTableWidgetItem( str(values[0][1]) ))
            self.transactionTableWidget.setItem(row,3,QtGui.QTableWidgetItem( str(values[0][2]) ))

            row += 1

        self.transactionTableWidget.horizontalHeader().setStretchLastSection(True)
        self.transactionTableWidget.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)

        self.transactionTableWidget.setStyleSheet("alternate-background-color: #AAAAAA;background-color: #CCCCCC;")
        self.transactionTableWidget.setAlternatingRowColors(True)
        self.transactionTableWidget.setSortingEnabled(True)
        self.transactionTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.transactionTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.dock_transactions.addWidget(self.transactionTableWidget)

        pass

    #########
    #  
    #########
    def createTradesUI(self, trades):
        
        self.tradeTableWidget = QtGui.QTableWidget(self.dock_trades)
        self.tradeTableWidget.setColumnCount(7)

        labels = [ "Trade Ref","Direction", "Date Open", "Date Close", "Price", "Commission", "Profit Net" ]
        self.tradeTableWidget.setHorizontalHeaderLabels( labels )

        for key, values in trades:

            self.tradeTableWidget.setRowCount(len(values[0])) 

            row = 0
            for trade in values[0]:

                if not trade.isopen:
                    self.tradeTableWidget.setItem(row,0,QtGui.QTableWidgetItem( str(trade.ref) ))
                    self.tradeTableWidget.setItem(row,1,QtGui.QTableWidgetItem( "Buy" if trade.long else "Sell" ))

                    self.tradeTableWidget.setItem(row,2,QtGui.QTableWidgetItem( str(bt.num2date(trade.dtopen)) ))
                    self.tradeTableWidget.setItem(row,3,QtGui.QTableWidgetItem( str(bt.num2date(trade.dtclose)) ))

                    self.tradeTableWidget.setItem(row,4,QtGui.QTableWidgetItem( str(trade.price) ))
                    self.tradeTableWidget.setItem(row,5,QtGui.QTableWidgetItem( str(trade.commission) ))
                    self.tradeTableWidget.setItem(row,6,QtGui.QTableWidgetItem( str(trade.pnlcomm) ))

                row += 1

        self.tradeTableWidget.horizontalHeader().setStretchLastSection(True)
        self.tradeTableWidget.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)

        self.tradeTableWidget.setStyleSheet("alternate-background-color: #AAAAAA;background-color: #CCCCCC;")
        self.tradeTableWidget.setAlternatingRowColors(True)
        self.tradeTableWidget.setSortingEnabled(True)
        self.tradeTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tradeTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.dock_trades.addWidget(self.tradeTableWidget)

        pass

    #########
    #  
    #########
    def createOrdersUI(self, orders):

        self.orderTableWidget = QtGui.QTableWidget(self.dock_orders)
        self.orderTableWidget.setRowCount(len(orders))
        self.orderTableWidget.setColumnCount(8)
        
        labels = [ "Order ID" , "Size",  ]
        self.orderTableWidget.setHorizontalHeaderLabels( labels )

        for i in range(len(orders)):
            order = orders[i]

            self.orderTableWidget.setItem(i,0,QtGui.QTableWidgetItem( str(order.ref ) ))
            self.orderTableWidget.setItem(i,1,QtGui.QTableWidgetItem( "Buy" if order.isbuy() else "Sell"))

            self.orderTableWidget.setItem(i,2,QtGui.QTableWidgetItem( str(bt.num2date(order.created.dt))  ))
            self.orderTableWidget.setItem(i,3,QtGui.QTableWidgetItem( str(bt.num2date(order.executed.dt))  ))

            self.orderTableWidget.setItem(i,4,QtGui.QTableWidgetItem( str(order.exectype)  ))

            self.orderTableWidget.setItem(i,5,QtGui.QTableWidgetItem( str(order.size ) ))
            self.orderTableWidget.setItem(i,6,QtGui.QTableWidgetItem( str(order.price ) ))
            self.orderTableWidget.setItem(i,7,QtGui.QTableWidgetItem( str(order.executed.pnl) ))

        self.orderTableWidget.horizontalHeader().setStretchLastSection(True)
        self.orderTableWidget.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)

        self.orderTableWidget.setStyleSheet("alternate-background-color: #AAAAAA;background-color: #CCCCCC;")
        self.orderTableWidget.setAlternatingRowColors(True)
        self.orderTableWidget.setSortingEnabled(True)
        self.orderTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.orderTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.dock_orders.addWidget(self.orderTableWidget)

        pass

    #########
    #  
    #########
    def show(self):
        fplt.show(qt_exec = False) # prepares plots when they're all setup
        self.win.show()
        self.app.exec_()

    #########
    #  
    #########
    def createSummaryUI(self, brokerCash, brokerValue):
        
        self.summaryTableWidget = QtGui.QTableWidget(self.dock_summary)
        self.summaryTableWidget.setRowCount(2)
        self.summaryTableWidget.setColumnCount(2)

        self.summaryTableWidget.setItem(0,0,QtGui.QTableWidgetItem("Cash"))
        self.summaryTableWidget.setItem(0,1,QtGui.QTableWidgetItem(str(brokerCash)))

        self.summaryTableWidget.setItem(1,0,QtGui.QTableWidgetItem("Value"))
        self.summaryTableWidget.setItem(1,1,QtGui.QTableWidgetItem(str(brokerValue)))

        self.summaryTableWidget.horizontalHeader().setStretchLastSection(True)
        self.summaryTableWidget.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.Stretch)

        self.summaryTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.summaryTableWidget.verticalHeader().hide()
        self.summaryTableWidget.horizontalHeader().hide()
        self.summaryTableWidget.setShowGrid(False)

        self.dock_summary.addWidget(self.summaryTableWidget)
        
        #Table will fit the screen horizontally

        pass

    #########
    #  
    #########
    def drawFinPlots(self, data):
        # fin plot
        self.ax0, self.ax1 = fplt.create_plot_widget(master=self.area, rows=2, init_zoom_periods=100)
        self.area.axs = [self.ax0, self.ax1]
        self.dock_chart.addWidget(self.ax0.ax_widget, 1, 0, 1, 2)
        #self.dock_1.addWidget(ax1.ax_widget, 1, 0, 1, 2)

        fplt.candlestick_ochl(data['Open Close High Low'.split()], ax=self.ax0)
        fplt.volume_ocv(data['Open Close Volume'.split()], ax=self.ax0.overlay())

        # def add_line(p0, p1, color=draw_line_color, width=1, style=None, interactive=False, ax=None):
        #fplt.add_line();

    #########
    #  
    #########
    def drawOrders(self, orders):
        for order in orders:
            if order.isbuy():
                direction = "buy"
            elif order.issell():
                direction = "sell"
            
            fplt.add_order(bt.num2date(order.executed.dt), order.executed.price, direction, ax=self.ax0)