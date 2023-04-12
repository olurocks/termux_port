# Termux_Expense_Tracker

An app that helps users keep track of their expenses

## Description
A Python script that allows users to track their daily expenses by receiving alerts for bank transactions. The script will use the termux-sms-list command to retrieve SMS messages from the user's phone, and will filter the messages to include only those that are from banks. It will then classify the transactions as either credits or debits, and will keep track of the total amount of credits and debits.

If the total amount exceeds the user's daily limit, the script will send an alert via the termux-tts-speak command. The script will be designed to run continuously, with a blocking scheduler setting the frequency at which the script checks for new messages and sends alerts. It will also include error handling to prevent the script from crashing if there are no SMS messages or if there are issues with the regular expressions.

This project will require familiarity with command line tools, SMS messaging, regular expressions, error handling, and scheduling in Python. The resulting script will provide a useful and practical tool for tracking daily expenses and staying within a budget.
* works for 3 Nigerian banks for now (United Bank for Africa, Zenith Bank, Union Bank plc)


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
