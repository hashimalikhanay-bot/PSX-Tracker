**📘 PSX Tracker — README**
Overview

PSX Tracker helps you monitor your Pakistan Stock Exchange portfolio by:

Saving your stock orders

Fetching live prices automatically

Calculating profit and loss

Showing visual performance charts

All data is stored locally for privacy and speed.

Features
**📊 Live Portfolio Tracking**

Fetches real-time PSX prices

Updates every 5 seconds

Calculates live profit and loss

**📝 Orders Manager**

Add orders

Edit orders

Delete orders

Auto-saves to:

C:\PSX\orders.json

**📉 Interactive Chart**

Shows:

Total portfolio PnL line

Individual stock PnL lines

Live updating graph

**💰 PnL Window**

Displays:

| Symbol | Shares | Buy Price | Current Price | Profit/Loss |

Updates automatically.

**💾 Local Storage**

Your data is saved locally:

C:\PSX\
    PSX.exe
    orders.json


No internet upload. No cloud.

Installation

Run:

PSX_Setup.exe


Installer will:

Install app in:

C:\PSX\


Create Desktop shortcut

Create orders.json automatically

**How To Use**
Step 1 — Open App

Launch:

PSX Tracker

Step 2 — Add Orders

Click:

Edit Orders


Enter:

Symbol → example: MEBL

Shares → example: 100

Buy Price → example: 450

Click:

Add Order

Step 3 — View Profit

Click:

View PnL

Step 4 — View Chart

Main screen shows live chart automatically.

Example

If:

You bought MEBL at 450
Current price = 487
Shares = 100


Profit:

3700 PKR

System Requirements

Windows 10 or newer

No Python required

No Excel required

No browser required

Data Source

Live prices fetched from:

Pakistan Stock Exchange website

**File Structure**
C:\PSX\
│
├── PSX.exe
├── orders.json

Safety

No login required

No personal data collected

No cloud storage

Fully offline except price fetch

Version

Current Version:

1.0

**Developer**

hashimalikhanay-bot

**Created Using:**

Python

Tkinter

Matplotlib
