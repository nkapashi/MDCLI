from datetime import datetime, timedelta
import sys

generalErrorText="""ERROR:
Either no response was recevied by monerod or the resposne contained an error.
Double check your connection details and any input data."""

            
def calcUptime(timestamp):
    """Function that returns uptime in day,hour,minute format.
Args:
   param1 (int):The time of the start in unix time stamp format.
Returns:
   str: The uptime in day,hour,minute format.
"""
    startDate = datetime.fromtimestamp(timestamp).strftime('%d-%b-%y')
    uptime = (datetime.now() - datetime.fromtimestamp(timestamp)).seconds
    d = datetime(1,1,1) + timedelta(seconds=uptime)
    return (f"{d.day -1}d, {d.hour}h, {d.minute}m", startDate)

def fromUnixTime(timestamp):
    try:
        humanTime = datetime.fromtimestamp(timestamp).strftime('%d-%b-%y %H:%M')
        return humanTime
    except OverflowError:
        return "Pending"

def assertToExit(data):
    # Will need to replace assert with something else...Some day.
    try:
        assert type(data) is dict
    except AssertionError:
        sys.exit(generalErrorText)

def print_table(lines, separate_head=True):
      """Prints a formatted table given a 2 dimensional array.
      All gredit goes to:
          http://blog.paphus.com/blog/2012/09/04/simple-ascii-tables-in-python/
Args:
   param1 (list): A list consisting of tuples.
   param2 (bool): Use list first entry as a header.
Returns:
"""
      #Count the column width
      widths = []
      for line in lines:
          for i,size in enumerate([len(str(x)) for x in line]):
              while i >= len(widths):
                  widths.append(0)
              if size > widths[i]:
                  widths[i] = size

      #Generate the format string to pad the columns
      print_string = ""
      for i,width in enumerate(widths):
          print_string += "{" + str(i) + ":" + str(width) + "} | "
      if (len(print_string) == 0):
          return
      print_string = print_string[:-3]

      #Print the actual data
      for i,line in enumerate(lines):
          print(print_string.format(*line))
          if (i == 0 and separate_head):
              print("-"*(sum(widths)+3*(len(widths)-1)))
        