# Termux_Expense_Tracker

An app that helps users keep track of their expenses

## Description
The Expense Tracker with Bank Transaction Alerts is a Python script designed to help users track their daily expenses by receiving alerts for bank transactions. The script utilizes the termux-sms-list command to retrieve SMS messages from the user's phone and filters them to include only messages from three Nigerian banks: United Bank for Africa, Zenith Bank, and Union Bank plc.

###Key Features:
1. SMS Message Filtering: The script uses regular expressions to identify bank transaction messages, ensuring that only relevant messages are processed.

2. Classification of Transactions: It accurately classifies transactions as either credits or debits, providing a clear overview of the user's financial activity.

3. Daily Expense Limit: Users can set a daily expense limit, and the script will keep track of the total amount of credits and debits. If the total amount exceeds the set limit, an alert is sent via the termux-tts-speak command.

4. Continuous Operation: The script is designed to run continuously, with a blocking scheduler controlling the frequency at which it checks for new messages and sends alerts.

5. Error Handling: The script includes robust error handling to prevent crashes in scenarios where no SMS messages are available or when issues with regular expressions occur.

This project requires a strong understanding of command line tools, SMS messaging, regular expressions, error handling, and scheduling in Python. Once completed, the script will serve as a practical and useful tool for individuals looking to track their expenses and manage their budgets effectively.


## Getting Started

### Dependencies
* First you need to get termux from [fdroid](https://f-droid.org/en/packages/com.termux/) . If you don't have fdroid installed you can download [here](https://f-droid.org/)
* Also install the Termux-API [here](https://f-droid.org/en/packages/com.termux.api/)
*PS: Do not download from playstore.

* Open the installed termux app and type in "pkg install python3" on the page that looks like the command prompt on windows


### Installing

* Download the portman.py app from my github [link](https://github.com/olurocks/termux_port/archive/refs/heads/main.zip)

and extract portman.py from the zip file



### Executing program

* Open termux and type in "realpath portman.py" to get the directory the file was downloaded to. (If this doesn't give you the correct path, kindly manually copy the directory from your file manager)

* copy the path and run "python3 /the_path_you_copied/"
```
"realpath portman.py"
```

## Help

You are the first set of people to use this , kindly drop reports of bugs or improvements to be made and i'll make adjustment



## Authors

Ezekiel Olumide 
[@_d_aslan](https://twitter.com/_d_aslan)

## Version History

* 0.1
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License



## Acknowledgments

Inspiration, code snippets, etc.
* [termux wiki](https://wiki.termux.com/wiki/Termux-notification)
* [ChaosMagician](https://twitter.com/Kuro_Lytes)
