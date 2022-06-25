# Installation
* The system has currently been tested on Raspberry Pi Zero, Pi Zero W, 2, and 3 using an Adafruit 3.5" resistive PiTFT,
  Official Raspberry Pi 7" Capacitive Touchscreen, and Adafruit 2.8" capacitive PiTFT. It is also known to run on a
  Pimoroni Hyperpixel4. The system runs using Python 3.7 or later. The current install scripts change the system to run
  under Python 3 as distributed with Raspbian. The code is no longer comatible with Python 2 due to requirements on the
  libraries it uses. The system runs on (at least) Stretch and Buster releases of Raspbian.

    * **Note**: Some subreleases of Buster seem to do different things with setting up the Pi screen framebuffer. The
      install scripts and console try to accomodate what is going on, namely, that sometimes the buffer is /dev/fb0 and
      sometimes it is /dev/fb1. However, if you seem to have installed things correctly and still see no output on your
      screen you might try adding a local screendefinitions file (see below) that forces your system to the correct
      framebuffer in your case. If you have more than one /dev/fb? try each in turn.

  To set up a system use one of the following methods:

    * Easiest:  Build your Pi using a recent Raspbian image from the Foundation. The system has been tested and run on
      Jessie, Stretch, and Buster versions. Add the **pisetup.sh** script to the /boot partition on the SD card while
      you have the card in whatever system you use to write the image. After booting the Pi with this image you may want
      to configure Wi-Fi from the console if you need that. Then run as root `bash /boot/pisetup.sh`.
        * Note 1: The easiest and safest way to get the pisetup file from GitHub is to use the command:
        ```
        curl -L -O https://raw.githubusercontent.com/kevinkahn/softconsole/master/docs/pisetup.sh
        ```

      from Windows PowerShell. Then just drag it to the SD card /boot directory.
        * Note 2: If Raspbian finds a file called "wpa_supplicant.conf" in the boot directory it will copy that to the
          right spot to enable Wi-Fi. This file looks like:
          ```
          ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
          update_config=1
          country=US

          network={
              ssid="your wifi ssid"
              psk="your wifi key"
          }
          ```
             Also, if it finds an ssh file (content of no importance) it will enable ssh access.  So I find it easiest when I finish burning the OS image on the SD card, to then copy my wpa file and an empty ssh file to the boot partition (it will be available on your PC).  Then when you first boot the Pi you will be able to immediately log into it over the network via ssh and run the pisetup script with no need to ever use an HDMI cable.  In the same spirit as this, my script looks for a directory called "auth" and copies its contents to ~pi/Console/local so you can create your password stuff once and put it in a file that gets included in your config file.
             
        * Note 3: The installation scripts have to make some assumptions about the way the underlying OS sets things up and about how the Adafruit PiTFT scripts handle install of those screens.  While the installation scripts attempt to be resilent against changes in these dependencies, it is always possible (and has occurred multiple times) that a dependency will change in an unexpected manner.  The scripts at least attempt to report the problem if this happens.  Please report any such issue to me and I'll try to resolve the changes promptly.

      This script will ask questions needed to configure the console hardware and software:
        * A node name: allows the node to be addressed by name on the network versus only by its IP address. Set this
          and make sure it is unique on your network. You should be able to address the node later as <nodename>.local.
        * VNC Standard Port: this allows you to move the VNC server and ssh server to non-standard ports if you wish. If
          you answer yes a VNC port will be established on 5900 for the console and on 5901 for a virtual console and
          ssh will run on 22 (note if you use the headless configuration approach noted above, ssh will run on its
          normal port until after the pisetup script runs even if you move it via the prompt). If you supply a port
          number here then the VNC virtual console will appear on that port, the VNC console will appear on that port
          minus 1, and ssh will appear on that port minus 100. Don't use this unless you know why you are - one reason
          might be if you are planning to open a firewall in your router to allow non-local access to the console (often
          but not always a bad idea). To access the node via VNC you will probably want to normally use the virtual VNC
          since the console VNC will have the size and shape of your Pi screen and will only display an interactive
          terminal if the pi screen is showing one (i.e., the softconsole is not running).
        * Personal: You probably want to answer N to this.  I often run "next-release" stable versions of the softconsole at my house to try out things and get some actual useage before I generally release versions.  Setting this to yes will access such versions which may mean you get something that isn't tested for your situation.
        * Beta install: Normally you should answer N to this.  It is there so that it is possible for a new installation to directly install the current beta version in order to test a previously unsupported configuration.
        * Autostart: Normally you'll answer y to this as it sets things up to automatically run the softconsole on the pi screen at boot rather than leaving your pi at an X-window session.
        * Known screen type: If you are using one of the listed screens the install script will handle drivers etc.  If you are using another screen that you installed yourself answer N.
        * Screen type: Enter the type of pi screen you are using from the list of supported ones in the question.  Other screens may well work but you'll need to install them yourself after this script finishes.
        * Whether you want to set up a minimal ISY test. (see below)
        * Continue install: answer yes here to simplify the install process.  The system will automatically reboot and run the second part of the softconsole install. 
 If you don't answer y then when the script finishes you should reboot and then run **installconsole.sh** as root after the reboot.  Before rebooting you may do any other system configuration that you need.  For example, this is where you'd configure a screen type that isn't (yet) supported by the setup script.
   
        * **Note**: There are some long pauses in the installation scripts because the Pi needs to do a lot of work updating the system.  Particularly if you are installing on a Pi0 be patient - that little processor is working as hard as it can!
    * Expert alternative: All the install scritps are in the github repository so if you are a Linux expert and want to configure your Pi in some specific way have at it.  Manually examine the scripts above to perform the specific configurations and installations that make sense for your system.
* The resultant system should have a consolestable and possibly consolebeta directories populated and a Console directory created.  The configuration file goes in the Console directory.  The default name of config.txt is looked for first, followed by looking for a file of the form config-_systemname_.txt.  This system-name specific default lets you populate a set of console systems identically have each choose an appropriate configuration.  See the examples I provide for my use of this.
 * The console can be run manually as "sudo python -u console.py" from within the consolestable directory.  Normally, though, the console would be configured as a Linux service using the systemd manager with the name "softconsole".  See the discussion below on starting the console.  The version of the console run by systemd will be the one pointed at by the file versionselector which normally has "stable" as its content.  From the maintenance screen in console you can ask to set the beta version and download the current beta.
* Current release notes:

For a history of changes per release see the notes in the GitHub repository.  Note that all the source code for the console is available on github under kevinkahn/softconsole and you are free to examine and/or modify as you like.

# Console Directory and Files

The installation creates a number of diretories and installs many files, all based in the /home/pi directory. First
there are directories that hold the actual program and its documentation. The directory **consolestable** holds the
current released code. If you later update the release via the maintenance screen or via an automatic update procedure
the files in this directory get updated. If the system has been updated the previous version of the console code will be
in the **previousversion** subdirectory and can be restored manually by moving it back to be the actual consolestable
directory. The directory **consolebeta** holds the current beta release. Normally you won't care about or run this
version since it is test code. You can select to run this version from the console maintenance screen but I don't
suggest you do that unless you are doing because I asked you to. The directory **consolerem** is empty and is an
artifact of my debugging and test environment. The directory **consoledev** is also empty but could be populated to run
the current absolute most-recent live version of the code from github. Don't do this unless you are really a masochist
or want to do some development work.  
The directory **Console** is the only directory that you should normally have reason to manually change or use. It
holds, by default, the configuration files and the operational log files for the console. Other files left from the
install process are in a directory called **consoleinstallleftovers** which may be deleted under normal situations.
Files earlyprep.log and prep.log document the install and may be useful for diagnosing issues if a problem occurs during
system installation. The python script adafruit-pitft-touch-cal is used during installation to set up the screen
calibration. It is left behind in case any issues arise with that. Finally, the file log.txt simply records console code
installs and restarts. The contents of the 2 source directories is simply a clone of the relevant versions of the GitHub
repository, although once the console has run python also leaves compiled files here.

The **Console** directory holds the log files from each run of the console. Most recent is Console.log, previous is
Console.log.1, etc. The number of logs kept is a console parameter. The console installation script asks whether to set
up a minimal test system. If you answer 'n' then the Console directory is left empty and you should proceed to create
your configuration information manually. If you are just starting, you should probably answer 'y'. In this case, a set
of example configuration files will be copied from the example directory in consolestable to Console. By default, the
console looks for ~/Console/config.txt as its starting configuration file. I have for neatness used the subdirectory
cfglib as a place to place additional configuration files that may be included via directives in config.txt and have
conventionally used the cfg extension for these. Note, there is no difference between the config.txt format and the cfg
file formats and were I to do this again I'd probably have made them all names *.cfg. In my use, I have found that I
often what to use the same screen on a number of my consoles and this allows me to create those screen configurations
once and copy them to each system. Se the next section for a suggested way to get started via the minimal configuration
file that is in the examples. Within the Console directory are directories with names including **.HistoryBuffer**. You
should normally have no reason to look at these but if you are reporting a bug to me that has caused a Warning or Error
log entry there may be a log file in the corresponding directory that will assist in debugging. The console program is
heavily multithreaded and these history files can give some detailed information about the actual order of operations
the resulted in an error.

# Starting the Console
The Console uses systemd service support for starting.  (Much older version used the rc.local mechanism but this is now fully deprecated and all running systems should be using systemd.  If you have a very old installation that still uses rc.local you should update to systemd (updates have already done most of the work for you - they just couldn't edit the rc.local files) because the older mechanism will stop working entirely in the near future.
  
  If you do a clean install of this version or beyond a service description has been placed in /usr/lib/systemd/system.  To have the console start at boot do "sudo systemctl enable softconsole" and beginning with the next boot it will start automatically.  If you selected this option during install this has already been done for you.  To stop the console from starting automatically use "sudo systemctl disable softconsole".  At any time the console can be started with "sudo systemctl start softconsole" or stopped with "sudo systemctl stop softconsole".  All other interactions via the systemd mechanism are also available and limited console log messages will appear in syslog.  See systemd man pages for more info about service control.

# Quick Setup of Minimal Test

To ensure that the basic setup of the Console is ok and that you understand the pieces, there is a minimal test
configuration that you might want to run. If you answer 'y' to the question above about creating a minimal ISY or HA
test configuration, setup will continue by asking for the IP address of your hub, and for ISY your username and
password, or for HA an access token. It will create the file Console/cfglib/auth.cfg using this information. It will
also ask for the name of a single switch that you want to use for the test. It will use this information to create a
single screen with a single button that should turn that switch on and off. It will also define a clock screen that
should appear when the console is idle.

Now start the console as root by going to the consolestable directory and running python -u console.py. This should
bring up a very simple 1 screen instance of the console that can turn on/off the switch you picked. If you leave the
screen untouched for 15 seconds it should dim and then after another 30 seconds it will switch to display a cover
screen, here the clock.

You can also touch a nav key at the bottom of the screen to move to the next or previous screen in the chain (here there
is only one - the clock screen) to get the clock displayed. As this is a live screen and not a cover screen it will have
nav keys. Now if you don't touch the screen it will dim after 15 seconds, persist as a dim clock for 30 seconds and then
change to a dim home screen (here the test screen), persist for 30 seconds as a dim home screen, then switch to a cover
screen (here the clock also but with no nav keys). At any point where the screen is dim touching it will brighten it,
and if it is on a cover screen return you to the home screen.

Playing with this test should give a basic idea of the operation when many screens are available.  The times above are all parameters in the config file.  Multiple cover screens can be defined which will then cycle using the times in the idle list times parameter.  When the screen is "bright" touching it 3 times will switch to a Secondary chain of screens (see other example files as not such secondary chain is defined in the  minimal test).  Touching the screen 5 times will get you to the Maintenance screen from which new versions can be downloaded or the console or the Pi restarted or shutdown.
# Basic Operation/Arrangement of the Console
The basic command structure of the console is based on screens.  The program allows a main sequence of screens within which you can move forward and back via the navigation keys at the bottom of the screen.  The program also allows the definition of a secondary chain of screens.  Finally, a key on a screen can be defined to take you to another screen.  This allows trees of screens rooted in a screen on one of the chains.  Screens that are reached via a GoTo key will have "Home" and "Back" navigation keys at the bottom.  The Back key returns to the screen you came from which the Home key either returns to the screen on the chain if you are multiple screens deep in a tree, or the general console home screen if you are only one level below the chain.  (Without this difference the Home and Back keys would be equivalent on a screen one level below a chain screen.)

You can move between the main and secondary chains via 3 quick taps.  The reason for the 2 chains is that I have found that for any console instance it is likely to be convenient for have a few screens that get frequently accessed.  However, you may want to have many more, e.g., to include ones that control all other parts of your house.  It is annoying if these are in the main chain since you then would have to click through them all the time.  One of the screens on the main chain is designated home and this is the screen that the console will return to on its own if left idle for a timeout period.  The console also defines "cover" or idle screens which appear when the console has been idle for a while.  If more than one is defined the console will sequence through these screens based on timers.  Think of these as "covering" the home screen; they allow easy display of things like time or weather (or eventually perhaps other information).  These are passive screens when displayed with no navigation keys.  Touching them simply reverts the console to the home screen.  As a side note 5 taps will take you to a maintenance screen that allows some administrative operations.
## Definitions and Orientation for supported screens and touch

There are two files that provide some ability to configure the console to operate with the various touchscreens that are
available. They are found in the directory from which the console is executing (generally consolestable). In the event
that you need to modify them you may put a file of the same name in the Console directory and it will override or add to
those that come with the release.

The first of these files in screendefintions and defines the name of supported screens (e.g., 35r) and contain define
the frame buffer location, driver, and dimming mechanism for the screen. The screen type can be found in the file ~
pi/.Screentype. The entry in this file is of the form:
```
screentype, soft rotation code, touch modifier
```
where the second and third entries are optional.  If present the rotation code can be 1, 2, 3, 4 to request software rotation of the display from its native orientation by 90, 180, 270, or 360 degrees.  If set to 0 it requests use of the underlying hardware orientation.  (The 4 entry enables the soft rotation code with no effect for debugging purposes.) Normally the screen is displayed in the orientation of the underlying Pi system.  However, for the Pi4 this doesn't work since the new drivers for that system don't use the normal frame buffer.  For Pi4 systems select a soft rotation if needed.  Soft rotation may also be selected for other Pi systems if that is easier than changing the underlying orientation.  The third entry is a string that modifies the name of the touch controller setup references in the touchdefinitions file.  This makes sure that the touch coordinates map correctly to the displayed information.  For most cases, the screen rotation will automatically select the right touch rotation.  If the third entry is present it is appended after a "." to the name of the touch controller retrieved from the hardware and used to select an entry in the touchdefinitions file.

Note that there are types with a trailing 'B' which handle differences for that screen between Stretch and Buster.  Note that different releases of Buster systems seem to alter whether the native HDMI frame buffer is created.  The console will always attempt to use fb1 if it is defined in /dev for Buster systems.  If for some reason you know that on your system the screen is at some specific /dev/fb? you can change the screen type to a non-"B" name and supply the appropriate path for the frame buffer in this file.

The second of these files is touchdefinitions and defines the names of the touch controller, whether it is a capacitive controller, and a set of parameters to rationalize touch locations to screen pixels.  You shouldn't need to concern yourself with these unless you have misalignment between where you touch the screen and the image on the screen.

# Using Other Touchscreens
The console will probably run on other touchscreens without too much work.  To set this up, you need to understand that there are two separate coordinate spaces relevant to the screen.  The first is the display coordinate space that is defined by the resolution of the screen.  The console gets this from the OS and uses it to position what it draws on the screen, most importantly keys.  The second is the coordinate system used by the touch part of the device which also generally returns a pair of coordinates.  However, these may not agree with the display coordinates.  They may use a different origin or different scale or be offset in some way.  

The touchdefinition file aids in mapping a touch controller to the screen.  Don't exit the one in the installation because it will get overwritten if you upgrade.  Create a separate one in the configuration directory which will be overlaid on the one in the installation.  Note that the name of the touch controller comes from the OS and selects the line in the definition file to use.  To find your touch controller name do a "cat" of /sys/class/input/event0/device/name.  (Sometimes there may be multiple eventX files in which case figure out the one for the screen you care about.)

 The screen coordinates have (0,0) in the upper left corner of the screen and (maxx, maxy) in the lower right corner, where maxx is the horizontal screen max resolution and maxy the vertical one.  Note that if you use soft rotation of the screen these will change, as will the touch coordinates.  The touchdefinitions file has fields for a shift, flip, or scale of the touch coordinates to make them match the screen coordinates.  Scale multiplies the touch coordinate that is returned by the touch system by scale to get the screen coordinate to use.  Flip subtracts the touch coordinate from the given value which allows reversing the right to left ness of the coordinate system (flip should be set using the native touch coordinate system).  There is also has a boolean to allow swapping the treatment of the x and y touch axes.  So algorithmically what the touch handler does is:
```
1. Get the hardware touch system coordinates of a touched point
2. If swap axes is set true swap these
3. If flip is non zero subtract the appropriate coordinate from the appropiate flip value
4. Add any shift to the value to adjust misaligned touch systems
5. Multiply by the appropriate scale value 
```

If you install a new screen type there is program in the Tools directory of the installation that may help you figure
out how to set these parameters. Run it from the main installation directory and touch the screen corners and you should
get the screen resolution coordinates of those locations. If you do not, then adjust the setting in the touchdefinitions
file get them correst.

# Setting up and Running Softconsole
First I admit in advance that the syntax and parsing of the config files is both a bit arcane and somewhat error prone.  This is larglely due to the configuration parser I use and perhaps someday I can improve this.  You've been warned!  Given an understanding for the minimal test above you can then create real configuration files as you wish:

* Create a main config file, see the files in the "example_configs" directory within consolestable for help. The name of
  the config file defaults first to **config.txt**. If no config.txt file is found in the Console directory then the
  console looks for a file with the name **config-\<nodename\>.txt**. This is convenient if you are running multiple
  consoles around your home. You can create a single directory of all your configs and blindly load it onto each system
  and the system will select the correct configuration based on its name. The basic structure of the file is a sequence
  of sections started with \[section name] where the outermost part of the file is implicitly a section. Subsections
  which are currently only used to describe keys are started within a section with \[\[subsection]]. Within any section
  are parameter assignments of the form name = value. A complete list of current parameters is found in the params.txt
  file in this directory. It lists the global parameters with their type and default value if no assignment is supplied.
  It also lists for each module the local parameters of that module as well as any global parameters that can be
  overridden in that module. Strings may be written without quotes.
    * One specific example file to look at is authexample.cfg. I tend to put all the password and keys information in
      that file to make it easy to not share those things. The example shows what you will likely want for your hub(s)
      and for your weather provider.

    * While error checking is limited for the config information, the program will log to the Console.log file any
      parameters that appear in your configuration that are not actually consumed by the console as meaningful. This
      helps locate possible typos in the config file.
    * One note of importance: labels are lists of strings and should always be notated as "str1","str2". A label with a
      single string should automatically be parsed as a list of one string but if you have a case of a normal label
      appearing a single character vertical stack of characters as a trailing comma to that string to force it to be
      correctly parsed.
* The parameter MainChain provides the names in order of the screens accessible normally. The parameter SecondaryChain
  provides a list of screens that are accessible indirectly (see below). Any number of screens can be defined.
* Whenever a color needs to be specified you can use any color name from the W3C list
  at http://www.w3.org/TR/SVG11/types.html#ColorKeywords
* The config file supports an "include = filename" parameter to allow breaking it up conveniently. This can be useful if
  multiple consoles use some of the same screens and you want to have only one version of the description for those
  shared screens. It also supports a "cfglib = dirname" as a default place to look for included config files. Personally
  I have lots of small config files that I keep in a directory and specialize a single top level config file for each of
  my consoles. See the directory "example_configs" on github for lots of examples.
* Some responses from weather providers are fairly long phrases that don't display nicely on the weather screens. There
  is a file termshortenlist in the Console directory which is a json representation of a Python dictionary that maps
  phrases to shorter ones for display. It is self explanatory if you look at the examples that are prepopulated. You can
  edit this as you wish to add or change phrases to be shortened. If the console comes across a phrase that appears too
  long as it is running it will add create a termshortenlist.new file and add it to it. This provides an easy way to
  create a new version of the termshortenlist file by editing the new one.

# Hubs

As of Version 3 the console can support multiple hubs. Currently, it can handle ISY controllers and HomeAssistant
controllers. It can support, in principle, any number of hubs concurrently although testing at this point has only been
for a single ISY together with multiple HA hubs, where individual screens have had keys that operated devices from each
type of hub appearing together. HA hubs currently support on/off operation for light and switch domains. They also make
available all sensor entities in a store named with the HA Hub name. They support HA scenes. Note that scenes in HA can
only be turned on. Scene keys should either define a proxy switch/light to use to choose whether to display the console
key as on/off or use blink to provide some feedback that the scene was activated. Finally, they support a thermostat
screen that uses the standard HA climate domain but has only been tested using Nest thermostats. The old form syntax for
specifying the ISY hub via config file elements ISYaddr=, ISYuser=, ISYpasswd= are still supported. However, the new
preferred specification for a hub is to have a section in the config file named for the hub (e.g.,[[MyISY]]) with
elements in that section type=, address=, user=, and password=. An ISY Hub specification might look like:
 
```
        [[MyISY]
        type = ISY
        address = 192.168.1.15
        user = myusername
        password = mysecret
```

Current types are ISY and HASS. Note that Home Assistant Hubs do not expect a user. For a HA hub use the password
element to specify an access token that you create in your HA hub (HA 0.77 and after). No user is needed for an HA hub.
The actual format of a hub type is name.# where # is an optional version. If left out it defaults to 0. At this time the
HA hub supports version 0 that uses the old climate domain for thermostats and version 1 that supports the new climate
domain.

A default hub can be set for the configuration with DefaultHub= specifying the name of the default. Any screen can also
provide a DefaultHub= element to override the default hub for that screen. Finally, key section names can specify
explicitly the hub by which their device is controlled via the syntax hubname:nodename.

ISY hubs support Insteon and Zwave nodes on ISY994 or Polisy systems. In addition, you can specify a parameter
NodeServerSwitches = name1, name2, ... to define the nodeDefId (node definition id) from the ISY system for nodes that
behave like on/off switches. For such nodes the console will treat them the same as Insteon or Zwave switches and issue
on or off commands using the same protocol.

# Stores and Values

The console has a general notion of stored values that some screens and alerts can use. Stored values are referenced by
their store name and value name within the store and can be any single value or an array of values. For example, each
weather station that is referenced from Weather Underground has its recent data stored in a store named by the station
name. As an example for the weather station KPDX one can access the current temperature at Portland Airports as KPDX:
Cond:Temp or the forecast low temperature for the day 2 days out as KPDX:Fcst:Low:2.

## ISY
Stores are created for ISY variables (ISY:State:<varname> and ISY:Int:<varname>), local variables (LocalVar:<varname>), the weather stations, any MQTT brokers (<brokername>:<varname>), and console debug flags (Debug:<flagname>).  There is also a System store (e.g., entries of the form System:DimLevel) that holds some global system parameters that may be displayed or changed at runtime (currently mainly the DimLevel and BrightLevel values).
 
## Home Assistant
 A HA hub has an associated store of the same name.  HA sensors appear in this store as HUBNAME:entityname.  Additionally, you can access any entity attribute within HA via HUBNAME:entityname:attribute.  E.g., the brightness of a light might be HASS:light.ceiling:brightness.  Note, however, that attributes of entities in Home Assistant can come and go.  E.g., the brightness attribute of a light disappears if the light is off.  To avoid any issues with this, an attempt to access an attribute that isn't present for an entity yields None.  For screens where this value is attempted to be displayed it will be rendered as '--'.  For VarKeys it will render specially using the Appearance element "None".  See VarKey discussion for details.  Note that Home Assistant store elements may not be assigned to since they are not writable in HA.  This is different from ISY where variables can be assigned to.  HA attributes may appear in alert triggers and the ISNONE trigger can test for an unavailable attribute
 
## System Store
  The System store has some special entries that are generated dynamically: Time and UpTime.  **UpTime** is the time in seconds that the console has been up.  **Time** returns the current system time in one of 2 ways.  If used by itself (System:Time) it returns the Unix epoch time.  If used with a trailing format code (System:Time:%H-%M) it returns the string that is yielded by standard string formatting of Unix time (see, for example, https://docs.python.org/3/library/time.html).  Note that because the ':' is used to separate store fields it can't be used in a format string.  Since it would commonly be used in a time string the console substitutes '\*' with a colon in the format string.  This means a '\*' can't be used in the format string but one can always separate the time string into multiple store/format requests to the title string if that is really needed.  Also note that if you want a space in the format code enclose the entire store reference in quotes. 
  
## Uses  
 Store values may be referenced on weather and timetemp screens, in alerts, and alert screen actions.  There is also an **assignvar** alert (referenced as AssignVar.Assign) that may be used to assign a literal or another variable value to a store element.  An example of its use is to change the dim level of the screen at certain times of day.

## Other Stores
Stores are also used to store all major system and screen parameters.  System parameters are in the **System** store, while screen parameters are in a store named with the name of the screen.  Note that parameter values that are not explicitly set in a Key (or internally in a "subscreen") will inherit the value of the parameter from the enclosing screen or from an outermost **ScreenParams** store.  Use the maintenance screen, set flags, dump stores to create a StoresDump file in the Console directory if you want to see all the stores and field names.  In addition to the alert and screen references described above there is a general ability to set a store value while the console is running via MQTT.  This is definitely not for the faint of heart - feel free to contact me directly if you need to use this and the discussion below isn't adequate.

# Weather Providers

Screens that display weather need to have a store populated with the current information. You define a weather provider
like you do a hub. Currently, there is support for DarkSky (provider will go away 12/2021), and Weatherbit. Define a
provider and its key in the config file or an included subfile as:
```
    [DarkSky]
    type = WeatherProvider
    apikey = <key>

```

The general model here is that there is a single entry to define the weather provider and supply the key it needs to
demonstrate you are an authorized user. Then you define locations for which you want the weather pulled and any other
parameters needed to pull the weather, e.g., how often to refresh it. The type of each location is the name of the
weather provider. This entry results in a populated store under the name of the location that can be used to build
screens. Look at weathersources.cfg and any of the example weather screens to see how this goes together.

The **Weatherbit** provider supports an optional additional parameter units which can be set to 'I' or 'M' to indicate
respectively Imperial or Metric readings. The default is Imperial. Weatherbit supports either a Lat/Log pair or a City,
State pair for location. Weatherbit free service permits up to 500 API calls per day but it takes 2 calls to get current
and forecast conditions for a location. Thus, with multiple consoles and a few locations that refresh once an hour you
can overrun the free allotment. To avoid this issue, the consoles will share location data if they are connected to MQTT
on a network (see below). Basically, each console has a cache of recently seen weather readings that gets updated via
MQTT messages. If there is already a valid, recent reading in the cache the console uses that rather than fetching its
own readings. With this in place, any location refreshing once per hour will only use 48 API calls per day no matter how
many consoles are running.

The section names designate the provider and one or both can be used. Locations for which to get weather are defined
like (the actual contents of the Location field will depend upon what the particular weather provider requires):
```
[PortlandW]
type = APIXU
location = 'Portland, OR'
refresh = 59
[PDX]
type = APIXU
location = '45.586497654,-122.591830966'
```  
The section name will be the name of the store that will hold the weather and can be referenced where ever store references are allowed, most likely on a weather screen or timetemp screen.  Location is the string that the provider will use to return the weather.  Refresh is the optional refresh interval for getting new data in minutes (default 60).  Most providers limit calls per day so this provides some control over the demand you create.

The weather information is available in a store named as above with entries under "Cond" for current conditions, "Fcst" for forecast conditions (these are indexed by day number), as some common fields.  The set of fields available with standard names for screen display purposes are:
 * Current conditions:
```
    Time: time of readings as string
    TimeEpoch: time of readings as Unix epoch
    Location: Location of readings as string
    Temp: Current temperature as float
    Humidity: Current humidity as string
    Sky: Current sky condition as string
    Feels: Current "feels like" temperatire as float
    WindDir: Current wind direction as string
    WindMPH: Current wind speed as float
    WindGust: Current gust value as int
    Sunrise: Daily sunrise time as string
    Sunset: Daily sunset time as string
    Moonrise: Daily moonrise time as string
    Moonset: Daily moonset time as string
    Age: Dynamically computed age of reading as string
    Icon: Pygame surface of weather icon
```
 * Forecast Fields: (these are indexed by day up to the length of available forecast)
 ```
    Day: Name of day forecast is for as string
    High: Forecast high for day as float
    Low: Forecast low for day as float
    Sky: Forecast sky condition for day as string
    WindSpd: Forecast wind as float
    WindDir: Forecast wind direction as string of form "DIr@" since
     some providers do not provide this.  This form allows empty
     string for those to still have display make sense.
    Icon: Pygame surface for weather icon
```
 * Common Fields:
 ```
     FcstDays: Number of forecast days available as int
     FcstEpoch: Time of forecast as Unix epoch
     FcstData: Time of forecast as string
 ```
 * Provider Specific Fields:
 The fields above are always available no matter how they are returned by the provider.  Additionally, the native fields that the provider returns in a json message are also available under their provider name in the store.  In general, those fields begin with lower case letters whereas the standardized ones above begin with capitals.

# MQTT Broker Reference
## MQTT for Information Access
The console can subscribe to an MQTT broker and get variables updated via that route.  To do this create a separate section named as you with for each MQTT broker you wish to subscribe to.  Provide parameters that specify its type as MQTT, its address, password (if needed), and then a sequence of subsections each of which names a variable to be subscribed to.  These sections have parameters Topic, TopicType, and Expires that describe how the value will be stored in the console.  If Expires is left out then values will be valid forever, otherwise they will disappear after the listed number of seconds.

For example, the following might subscribe to a broker running in the house to which local sensors publish the current temperature and humidity on the patio.  One can then reference the current patio temperature on, for example, a timetempscreen, as myBroker:PatioTemp.  If the sensor stops posting for over 2 minutes then the console will show no value.
```
    [myBroker]
            type = MQTT
            address = server.house
            password = foobar
            [[PatioTemp]]
            Topic = Patio/Temp
            TopicType = float
            Expires = 120
            [[PatioHum]]
            Topic = Patio/Hum
            TopicType = float
            Expires = 120
```

## MQTT for Console Management
If the console subscribes to MQTT then additional function is enabled for managing the consoles and reducing Weatherbit data fetches.  If the console subscribes to multiple MQTT brokers than the first one configured is the default management broker.  You can force a specific MQTT broker to be the management broker by specifying **ReportStatus = True** in the configuration file for that broker.  The rest of this section describes the management related functions enabled by a management broker.  Note that as of 9/2019 the preferred way to control consoles over the network is via the screens found in the network section of Maintenance (see below).

At startup the console registers itself with the broker with a message to **consoles/all/nodes/\<hostname\>** containing information about the version running (version name, github sha, time of download), the time of the registration, the boottime of the pi running the console, the OS version running on the pi, and the hardware version of the pi. The console will then periodically publish to the broker at **consoles/\<hostname\>/status** a status update containing its status, uptime, and the state of the error indicator flag that notes an unseen Warning or Error in the log.  If the console goes down for any reason, the broker will publish a **dead** status. There is a short python program in the download directory called status.py that is an example of how to do a quick check of whatever consoles are running.  A console will also publish to **consoles/all/errors** a message whenever a Warning or Error level message is logged.

Finally, the consoles will accept commands from MQTT.  A console listens on the topics **consoles/all/set** and **consoles/\<hostname\>/set** for store name and value to be set in a variable (json encoded).  A console also listens on **consoles/all/cmd** and /**consoles/\<hostname\>/cmd** for the remote commands that include:
* restart: restart the console
* getstable: fetch the current stable release
* getbeta: fetch the current beta release
* usestable: set the console to start the stable version at next restart
* usebeta: set the console to start the beta version at the next restart
* status: issue a status message to MQTT
* issueError, issueWarning, issueInfo,hbdump: diagnostic/debug commands

These commands can be issued from the maintenance screens by going to "Network Concoles", "Issue Network Commands", and
then choosing a node to issue commands to by a single tap (standard commands) or a double tap (advanced commands). Nodes
not currently up show as greyed out and cannot be commanded (but see the next note).

**Note**: Once a node has ever been on your network and registered with MQTT it will appear in the list of nodes and
show as dead if it no longer exists or is actually just down. If you no longer want the node to even appear (e.g., you
renamed it or simply removed it) you need to clear its last will message from your MQTT broker. You can do this through
the console by double tapping (advanced) on the dead node name on the issue command screen. This will access an advanced
command that will clear the history for that dead node.

(For a full list of commands you can look at the file issuecommand.py or look at the commands you can issue from the Maintenance screens.)

**Note:** While you can manually issue MQTT commands from some other utility, the supported way to do this is via the Remote Console commands screen within Console Maintenance.

# Screens

## Common Parameters
All screens support some common keyword parameters that control appearance of aspects of the screen.  These include (note that these will default to any values set in the globabl part of the config file, which corresponds to the store "ScreenParams"):
* DimTO: Time before screen will go dim if not touched
* CharColor: Color of general characters on the screen
* PersistTO: Time screen will remain visible before reverting to the home screen
* BackgroundColor: Color of the screen background
* CmdKeyCol: Color of the nav key at the bottom of a screen pointing to this screen
* CmdCharCol: Corresponding character color
* DefaultHub: Specifies a specific hub for references on this screen
* KeyColor: Default color for any keys on the screen (default for next two parameters)
* KeyColorOn: Default color for any keys on the screen that are in an "on" state
* KeyColorOff: Default color for any keys on the screen that are in an "off" state
    * Note: If KeyColorOn and KeyColorOff are both specified explicitly those colors are used as is.  Otherwise, the Off color is dulled automatically when the key is in the off state.
* KeyCharColorOn: Default character color for "on" keys
* KeyCharColorOff: Default character color for "off" keys
* KeyOnOutlineColor: Color for outline for "on" keys
* KeyOffOutlineColor: Color for outline for "off" keys
* KeyOutlineOffset: Spacing offset for outline of key
* HorizButtonGap, VertButGap: pixel space to leave between adjacent buttons
* ScreenTitle: A title to be painted at the top of the screen (may be unspecified for no label)
* ScreenTitleFields: A list of store items that are to be substituted into the title when it is rendered
* ScreenTitleColor: Color for the screen label
* ScreenTitleSize: Size for the screen label
* Clocked: a value in seconds that will cause a repaint of the screen every interval.  Not needed for Clock screens and TimeTemp screens that already clock every second but useful for things like key screens if you want their title to refresh.
* label: a label for the screen to be used in nav keys that point to this screen; also is a default if a screen title is needed for a screen and one is not explicitly specified

Note that all the elements referring to keys may be explicitly specified at the key level - there are just default
values to use for the screen.

## Screen Title

If you set a non empty title for a screen that doesn't otherwise have one, the rest of the screen shrinks vertically to
allow the space. If ScreenTitleFields lists store items then these are substituted into the title whenever the screen is
rendered (including when it is rendered based on "Clocked"). Substitution is based on standard Python formatting rules
as defined in https://docs.python.org/3.7/library/string.html.

## Screen Types

### Keypad

* Keypad: mimics the KPL. Can support any number of buttons from 1 to 25 and will autoplace/autosize buttons in this
  range. Parmetrs KeysPerColumn and KeysPerRow may be used to override the auto placement of the keys. Keys may be
  colored as desired. Key types are:

#### Key Types

* ONOFF: linked to a device or scene and supports On, Off, FastOn, FastOff behaviors. If an ONOFF key is held down for a
  prolonged period of time and the underlying device is a dimmer, then a slider screen is displayed that allows the
  brightness to be set. For Insteon/ISY hubs, dimming also applies to scenes via the scene proxy mechanism. This allows
  convient dimming for common 3-way switch setups where multiple dimmers are combined in a scene to control a single
  load (or set of loads). By default the slider bar will display in the longer direction of the screen (e.g.,
  horizontally for the 7 inch screen in landscape mode and vertically for the smaller screen in portrait mode). This can
  be overriden by explicitly specifying a SlideOrientation parameter where 0 is default direction, 1 is force
  horizontal, and 2 is force vertical).
* RUNPROG: linked to a program to run. The program to run is specified by a **ProgramName** parameter. It issues a
  RunThen on the designated program for ISY hubs. It issues a automation.trigger or script.<scriptname> for the
  automation for HA hubs. A **Parameter** parameter may be supplied to provide parameter(s) to an HA script.  (ISY
  programs do not accept parameters.)  The Parameter may be a single string in which case the json {'Parameter':
  string} will be passed to HA. It may also be a comma delimited set of strings of the form A:vala,B:valb in which case
  the json {'A':vala,'B':valb} will be passed.
* (Deprecated-use RUNPROG with modifiers) ONBLINKRUNTHEN: linked to a program. Will blink to provide user feedback and
  will issue RunThen on program
* ON: will always send an "on" command to the linked device. This is useful for things like garage doors that use on
  toggles.
* OFF: will always send an "off" command to the linked device.
* GOTO: Change to a specific screen. Takes a parameter ScreenName=<name of screen to go to>. Going to another screen
  creates a stack of screens. On the new screen the Nav keys will be "Home" and "Back". Back returns to the calling
  screen. Home returns to the top screen of the stack unless that is the screen Back would go to in which case Home goes
  to the global console home screen.
* SETVAR: set the value of an ISY variable
* VARKEY: this type can be used passively to construct status displays or also allow stepping through a predefined set
  of variable values. Its **Var** parameter specifies a store item to operate on. It has an **Appearance**
  parameter that specifies the display appearance of the key for various values of the store item. This parameter has
  the form of a list of comma delimited descriptor items. Each descriptor item is of the form "range color label" (
  without the quotes). Range is either a single integer that specifies a store item value or a pair n:m which defines a
  range within which the store item falls for this descriptor to be used. Color is the color of the key for this value.
  Label is the label the key should have for this value using semicolons to separate lines within the label and a $ to
  be substituted for the store item value if desired. If the label is left out of the descriptor item the normal key
  label is used (either the key name or an explicit label parameter). if the store value doesn't match any of the ranges
  the normal key label is used. A **ValueSeq** parameter optionally specifies values that should be cyclically assigned
  to the store item if the key is pressed. If the current value of the store item is not in the ValueSeq then a press
  sets the value to the first item in the sequence. Leaving it out makes the key passive. As an example should help
  clarify. The code snippet below describes a key that will be green and say "All good" if the variable is 0; be yellow
  and say "Probably good"
  and show the value on 3 lines if the value is 1 or 2; and be red and say "Not so hot" and the value on a single line
  for values of 3 to 99. For any other values the key will display "Error in Value" and the value. Sequential presses of
  the key when the value is 0 will set the variable to 1, then 3, then 6, then 0. If something else has set the variable
  to, e.g.,4, then pressing it will make the variable 0. A **ProgramName** parameter may be optionally specified that
  will cause that script/program to be run in the hub (exactly as a RUNPROG key). In this case a **Parameter** parameter
  may also be supplied as in the RunProgram command.
   ```
  [[TestKey]]
  type = VARKEY
  label = Error in Value, $
  Var = ISY:State:tEST
  ValueSeq = 0,1,3,6 KeyCharColorOn = royalblue 
  Appearance = 0 green 'All good',1:2 yellow 'Probably; good; $',3:99 99 red 'Not so hot $'
  ```

* SETINPUT: this key is specifically for HA hubs but is somewhat similar to the VARKEY. It allows the display and
  setting of "input" entities in HA, specifically input_boolean, input_number, and input_select entities. These carry
  their own limitations on values and so do not need the value sequence information that the VARKEY has. The key takes a
  Value parameter which either provides an value for the input entity or calls an operation that is defined for that
  type of input. For input_boolean VALUE may be "toggle", "on", or "off" ("true" and "false" are accepted as
  alternatives for on and off). For input_number VALUE may be "inc", "dec", or a number to respectively increment the
  value, decrement the value, or set the value.  (Note: inc and dec use the HA defined operations and the HA defined
  step value.)  For input_select VALUE may be "first", "last", "next", "nextcycle", "prev", "prevcycle", or one of the
  HA defined selection values. The SETINPUT key also takes an "Appearance" and a "DefaultAppearance" parameter for
  control what the key looks like based on the entity value.
* SPECCMD: This key is specifically for HA hubs. It allows sending any command supported by an entity to that entity. It
  requires a "Command =" parameter that specifies the command to be sent. If parameters are needed for the command they
  can be supplied via and optional "Parameters =" paramter. For example, the following snippet issues an increase fan
  speed command to a fan and blinks to indicate the touch:
  ```
  [[fan.lr_fanlight_fan/up]]
  type = SPECCMD
  KeyColor = red
  Blink = 2
  Command=increase_speed
  label = Fan, Higher
  ```

#### Key Type Notes

* Note the key types PROC, REMOTEPROC, and REMOTECPLXPROC are reserved for internal use by the console.

* Modifier Parameters: The ONOFF, RUNPROG, VARKEY, and SETVAR keytypes support certain parameters that modify the key
  behavior:
    * Verify = 1: displays a confirmation screen before running the program. The messages on the confirmation screen can
      be customized with the GoMsg and/or NoGoMsg parameters.
    * Blink = n: provide visual feedback when the runthen is issued by blinking the key n times.  (For VARKEY the key
      will blink if you have not yet seen it with its current value, even if that value had been previously set while
      another screen was showing on the console.)
    * FastPress = 1: requires a quick double tap to activate the key. (Note not applicable to the ONOFF keys since there
      a double press corresponds to issuing a fast on or off to the device).

* Note: Scenes in general have no state to use for choosing the appearance of a button as on or off. ISY and HA handle
  scenes somewhat differently. For ISY a scene can be turned off while for HA scenes can only be turned on. To provide
  user visible feedback when a key corresponding to a scene is touched there are choices. The modifier parameter
  SceneProxy can be used to designate a device whose state should be used to pick the display appearance for the key.
  This is particularly useful for ISY scenes that simply model 3-way control of a light. For ISY scenes, the console
  will attempt to automatically choose a device to use as the scene proxy if none is selected (and will usually choose
  well). For HA automatic proxy choice is not done, so an explicit proxy would need to be specified if desired.
  Alternately, the user my opt to blink the key to provide feedback that the scene was turned on.

#### Key Appearance

All keys accept **Appearance** and **DefaultAppearance** parameters. These parameters define how the key is displayed
based on either a specified value given with the **Var =** parameter or, absent this, the state of the entity associated
with the key. Appearance takes a sequence of appearance descriptors where the first element (value matcher) describes
what values is applies to, the second chooses a color or set of colors, and the third provides a label. If the value
matcher is of the form num1:num2 it defines a number range that matches. If it is of the form tag1|tag2|tag3| it defines
a sequence of 1 or more selection values (note that there must be a trailing "|" to end the list of tags). If it is an
integer then it defines that integer value. If it is "None" then it matches a None value (see above). If it is "true" (
or "on") or "false" (or "off")
it matches that boolean condition. If is is "state*on" or "state*off" it matches the state of the relevant entity.
Finally, if it is none of these it matches a string. If none of the Appearance descriptors match then the
DefaultAppearance descriptor is used (for the default use None as the matcher). If the color is a single color then it
is the key color to use. If color is a string of the form: **(c1 c2 c3)** (note no commas) then c1 is the key color, c2
is the character color and c3 is the outline color. Any color can be suffixed with "/dull" as in red/dull to indicate
that the color should be muted. The default key coloration for on/off keys is created internally by the program using
state*on and state*off matches as a shortcut for the common case of an on/off key. Within a key label a '$' is replaced
by the value of the Var or if no Var was specified by the state of the node/entity. If the node is dimmable then the $
is replaced by the on percentage. See the example config files for examples of how all this works.

Key labels may also include dynamic values taken from the store by referencing them in the usual way as storename:name.
To do this include a "Fields =" parameter in the key description to name the desired fields and then reference them in
the key label in the normal Python manner as {} for the next field or {n} for a specific field. This is the same
convention as used in screen titles as described above.

### Clock

* Clock: displays a clock formatted according to the OutFormat parameter using any of the underlying OS time formatting
  codes. The character size for each line can be set individually. If there are more lines in the format than character
  sizes the last size is repeated. Python standard formatting is at https://docs.python.org/2/library/time.html. Linux (
  RPi) supports a somewhat richer set of codes e.g. http://linux.die.net/man/3/strftime

### Weather

* Weather: uses a weather provider to display current conditions and forecast. The location parameter is a location code
  defined as above.

### Thermostat

* Thermostat: mimics the front panel of the typical thermostat and provides full function equivalency. Has been tested
  with Insteon thermostat via ISY and Nest Thermostat via HA but should work with any device those hubs support. This
  screen uses an improved update approach for the setpoints. Touching the setpoint buttons only adjusts the values
  locally on the console and greys the values to indicate this. If no additional touch is seen for 2 seconds then the
  resultant setpoint is pushed to HA and thus the thermostat. The displayed values remain greyed until an update from
  the thermostat indicates it has set them or an addition time period passes after which the actual current setpoints
  are retrieved and displayed normally. Thus, if an error occurs updating the setpoints on the actual thermostat you may
  see the old setpoint reappear indicating something went wrong. This makes changing setpoints not have to wait for the
  latency to the hub and back for each degree of change.
### Time/Temp
* Time/Temp: combined screen, nice as a sleep screen that gives current time and the weather.  Format of the screen is largely controlled by the config.txt file.  The location is displayed unless you set the character size for that line to 0.  An icon can be displayed as part of the current conditions by setting CondIcon = True.  An icon canbe displayed as part of each forecast day by setting FcstIcon = True.  There are a variety of options for the display of the forecast days that can be selected by setting FcstLayout in the config file.  They are:
    * Block: forecast items are left aligned in a block that is centered based on the longest item (1 column) 
    * BlockCentered: forecast items are individually centered but multiline items are left aligned (1 column)
    * LineCentered: forecast items have each individual line centered (1 column)
    * 2ColVert: 2 column layout newspaper style days ordered down the column with a vertical line that visually splits the columns
    * 2ColHoriz: 2 column layout with days ordered across then down
    
    Fields that are referenced in the format descriptions of the config file will use the store corresponding to the location code specified for the screen and the type of field group being specified by default.  E.g., if the location is specified as KPDX then the default for a field, \<field\>, mentioned in the ConditionFields is KPDX:Cond:<field>.  However, any field in any part of the screen can be explicitly notated.  E.g., in the ConditionFields one could specify FOO:Fcst:High:1 to reference the forecast field for the next day high at FOO or MQTT:Humidity to reference some field Humidity that is supplied via an MQTT broker named MQTT.

    There are four regions of the screen each with its own character sizing parameter.  The font size of the clock area is given as **ClockSize**, that of the location as **LocationSize** (where 0 suppresses the location line), the current conditions block as **CondSize**, and the forecast block as **FcstSize**.  Note that for the current conditions and forecast blocks which can be multiline the appropriate size parameter can be a list of sizes which then apply sequentially to the lines.  The old parameter **CharSize** is deprecated.  It works currently but will be removed in the future.
### Picture
The Picture screen (type=Picture) is used to allow the console to function as a photo frame if desired.  It can function in one of 2 modes: directory mode and single mode.

In its default mode (directory) it will rotate through pictures (which must be jpg files) in a given directory. The
directory is designated by the parameter picturedir. If no picturedir parameter is provided the directory pics in the
config directory (normally Console) is used. If a picturedir parameter is provided, if it starts with a "/" it is used
as an absolute path to the picture directory. If it does not start with a "/" then it is interpretted as a path starting
with the config directory. A parameter picturetime sets the hold time in seconds for each photo on the screen and
defaults to 5 seconds. Pictures are oriented on the screen based on orientation information in the jpg exif if that
exists, so for most digital photos they will display correctly automatically. In operation the picture screen remembers
where in the photo it is so that if used as one screen in a set of idle screens it will pick up displaying photos where
it left off when it was last active. The directory is monitored for changes and the stream of photos will dynamically
reflect those changes. Since there is some pipelining involved, the changed photos may take 2-3 multiples of picturetime
to be visible. Also of note, the pictures are cached by the console, locally in a process format to improve efficiency.
If the source of the directory is a network drive this means that the photos will only use network bandwidth when they
are first being displayed which, given the size of typcial modern jpgs is a significant efficiency.

To use the screen in single mode provide a parameter "singlepic" which provides an absolute path to a jpg file (if it
starts with "/") or a path relative to the config directory to a jpg file. Parameter picturetime is not used in this
mode. The designated file is monitored for changes every second and will be reloaded if it changes. Thus, for single
mode the screen will reflect changes typically within a few seconds of making the change. This is helpful if the jpg is
actually a screen shot that is being updated or some other such dynamic information. Since the file is only reloaded
when it changes no caching is done for single mode.
### Alert

Alert: used to display an alarm condition. This screen type is tightly connected to Alerts which are described next.
Creating Alert screens is a two part process. First, you define the conditions that trigger the alert, this definition
includes the action to take when the trigger is fired, which is defined via Invoke= parameter naming an alert screen.  (
The 'Invoke' command may also name an Alert procedure which is a different case.)  An example of defining an Alert
screen might look like:
```
    # Alert Screen:
    # this is a Screen definition just like any other, though with some specific parameters
    [DynAlertSingleItem]
    type = Alert
    BackgroundColor = black
    MessageBack = red
    CharColor = black
    Message = AlertSingleItem:file
    DeferTime = 10 seconds
    BlinkTime = 5,1
    KeyColor = maroon
    CenterMessage = False
    AutoClear = 5 minutes
```
Most of the parameters should be self explanatory.  BlinkTime may be a single integer that specifies the on and off timing for the screen blinking, or it may be a pair in which case the first value is the on time and the second is the off time.  There are various possibilities for Message.  In general, it is a comma separated sequence of lines to be displayed.  However, it may contain references to store items in their usual ':' separated format.  It may also contain references to a file watcher.  In this case, there are two possible value cases.  If the watcher was created with Parameter SingleItem then a reference as in the example above as WATCHNAME:file causes the entire contents of the referenced file to be interpolated into the message at that point.  If the watcher was created with the Parameter Settings, then the lines in the watched file are expected to be of the form varname=value and each of the values of WATCHNAME:varname can be interpolated at the point in the message that it appears.  The screen will display until the alert condition is cleared via the screen button or via a state change in the cause.  For the case of a file watch only, the alert condition may also be cleared automatically after a time interval using the AutoClear parameter.

# Alerts

Alerts are defined in an "\[Alerts\]" section of the config files. See cfglib/pdxalerts for some examples. Currently,
alerts can be triggered periodically, based on a node state chance, or based on a variable state change. The effect of
the alert can be delayed by some time to avoid alerts for routine events that should clear within some typical window.
Alerts can either invoke an alert screen (see the away and garage alerts in the sample file) or an alert procedure (see
the update alert).
## Triggers
The condition that causes an alert is defined within the config section that defines the alert.  It has a **Type** which is currently Periodic, VarChange, NodeChange, or FileWatch.  For the VarChange trigger Var specifies a store element (see stores above), and Test and Value are used to describe how to test it.  Valid tests are as expected: **EQ**, **NE**, **GT**, **LT**, **GE**, **LE**, and **ISNONE**. For the *node* trigger Node, Test, and Value describe the trigger.  For *periodic* provides two options. You can provide parameter **Interval** which describes a repetition period either as an integer seconds or as an integer followed by "minutes" or "hours".  Alternatively, you can specify a parameter **At** which specifies either a single time of day or comma seperated list of times using standard time format (24 hour or explicit am/pm).
 
 The FileWatch trigger is slightly more complex.  It has a File parameter that specifies a path to a file to be monitored, either as an absolute pathname (starts with '/') or as a relative path from the configuration directory.  Triggering occurs if the modification time of the named file changes.  Parameter specifies how the contents of the file are to be treated.  If it is SingleItem then the entire file is placed in the store item named with the name of the AlertName:file.  If it is Settings, then the contents of the file are expected to be lines of the form name=value and all the values are accessed as AlertName:name.  FileWatch triggers may be cleared via the displayed button on their associated alert screen.
 
 For any of the triggers a Delay parameter may be specified to have the actual triggering delays some time period beyond the condition becoming true.
Triggers cause either an alert screen to be shown or an alert proc to be run.  If the screen or proc in question takes some parameter from the alert the Parameter defines it (see NetworkHealth for example).
## Local Variables
It is possible to define variables local to the console by creating a **\[\[Variables]]** section in the config file and defining one or more **varname = \<value\>** within it.  These may be used like any other store element by being referenced as LocalVars:\<name\>  At the moment they have limited but some use.
## Alert Procedures

Currently, the following alerts are available:

* **autoversion:** trigger this either at init time or periodically to check github for a new release. If a new *
  currentrelease* is found it is downloaded, installed, and the console rebooted with the new version. The old version
  is moved to a directory under the consolestable called *previousversion*.
* **networkhealth** when triggered (typically periodically)check for network connectivity to a specified IP address.
  E.g., checking for 8.8.8.8 (the Google name servers) will allow creation of an alert if Internet access is lost.
  Typically, this trigger will be used to invoke an alert screen to display the alarm. Define the trigger to have
  Parameter = IPaddress,localvarname and localvarname will be set to 1 if the address is pingable and 0 otherwise. If
  the variable changes it triggers any alert based on a "varchange" which can be used to display the alarm.
* **assignvar** When triggered (as *AssignVar.Assign*) it executes the assignments listed in it Parameter option. The
  Parameter is of the form var-ref = val where var-ref is a store idenitifier and val is either a number or a store
  identifier. E.g., Paramter = ISY:State:tEST = KPDX:Cond:Temp, ISY:Int:TestVar= 5 would assign the current KPDX
  Temperature to the ISY State variable tEST and assign the value 5 to the ISY Int variable TestVar each time it is
  fired.  (This replaces the temporary hack alert tempstoisy.)  As an example use, an assign of a value to the variable
  System:DimLevel using a periodic alert with a specific time parameter might be used to adjust the dim level of a
  console for late night versus daytime behavior.

## Alert Screens
These are screens (described above) that are triggered to appear based on a node or variable state, perhaps with a delay from the time of the state change.  E.g., display alert screen 5 minutes after garage door is opened if it is still open.  They provide a single button that can be linked to resolve the alert condition.  They are triggered by a test in the alert section of the config file defined above. An Alert screen can be deferred for a predefined time after which they will reappear. If the condition causing the alert clears they will disappear.
# Connecting Console Names with ISY Names
* Some names in the config file are used to link console objects to ISY nodes/scenes.  Specifically the section name of a thermostat sceen is used to connect that screen to an ISY thermostat and the subsection names of ONOFF keys are used to link those keys to an ISY device or scene.
* Simple names are looked up as the names of leaf nodes in the ISY node tree. You can also reference an ISY node via its
  full name using conventional "/" notation to describe the path from the root by starting the name with a "/".
* When a name is looked up in the ISY for linking preference it always given to finding the name as a scene first. Thus,
  if a device and a scene have the same name the console will link to the scene.

# Operating Softconsole
* Single tap on an On/Off key to actuate it
* Tap or double tap (depending upon config parameter) on a program key to actuate it.  Double tap or verify is recommended to lessen accidental running of programs from random screen taps.
* Change screens via the command buttons at the bottom of the screen
* Triple tap to access the secondary chain of screens (Note - ignored if in Maintenance mode) 
* 5-tap to access a maintenance screen (Note - ignored if already in Maintenance mode)
* After the designated time screen will dim
* After the designated time screen will automatically return to the home screen (except from the maintenance screen)
* From the home screen after the dim time out the screen will go to a "sleep" screen if designated - any tap will awaken it
    * The original version had only a single idle screen named by the DimHomeScreenCoverName parameter.  This parameter is deprecated but will still work if you don't opt for the new multi-idle screen ability.  You can designate a sequence of idle screens with DimIdleListNames and corresponding linger times per screen with DimIdleListTimes.  Once the console is idle it will cycle through these screens until tapped.  This got added to make a wall unit a nicer info display when not otherwise being used.
* On the maintenance/log screens single tap the lower part of the screen to see the next page or the upper part to see
  the previous page.
* On all normal display screens you may see a dim indicator displayed in the upper left-hand corner of the screen. This
  indicates that some console has had a Warning or Error level log message. If the indicator is a cross, the node you
  are looking at has had such an error. If the indicator is a circle, at least one other node on the network has had an
  error. The local node indicator is cleared once the log has been viewed. Remote node indicators are cleared when
  remote node itself clears its indicator either by network command or by viewing the log on that remote node.

# Maintenance Mode

Tapping on the screen 5 times or gesturing by swiping a finger from the upper left to the lower right of the screen puts
the console in maintenance mode and changes to a maintenance screen. There are buttons there to view the local log (and
by doing so clear any error indicator), select and/or download a version of the console (double tapping this accesses
development versions), set various debug flags, and exit or restart the console or shutdown or reboot the pi itself.

If the console is connected to an MQTT broker then an additional capability will appear for Network concoles. From here
you can display the current status of all consoles on your network, their hardware/OS and console versions, and issue
commands to them. If you choose to issue commands you will get a screen that lets you choose the console to interact
with. Selecting a console will let you see its log (or a reverse ordered recent list of errors it has encountered from
that log), command it to download versions, restart, reboot, etc. Note that double tapping on the node name accesses
some advanced commands meant mostly for debugging.

# Developers Notes
## Local Operations
During console start up it will attempt at a very early stage (before the config file has been chosen or opened) to execute a Python procedure localops.PreOp().  The localops module will be one found in the parent directory of the direcory holding the source code.  E.g., if running the code from /home/pi/consolestable it will look first for a file localops.py in /home/pi and then for a file localops.py in the source directory.  This allows you to write a Python script that performs something you need done on every console start.  The console will also call localops.LogUp() once the console log has been initalized.  This premits the PreOp procedure to arrange to have information logged once the log is started.  There is an example of my personal localops module in the sources that can be used for ideas if you need this capability.  Note that this version checks for "homesystem" so should be a noop on most systems.

## Defining New Screens by Coding a Module (updated for version 2)
New screens can be developed/deployed by subclassing screen.ScreenDesc and placing the code in the screens directory.  Screens modules have a single line of code at the module level of the form "config.screentypes[*name*] = *classname*" where *name* is the string to be used in config files to as the type value to create instances and *classname* is the name of the class defined in the module.  A screen class defines the following methods (ScreenDesc provide base level implementations that should be called if overridden):

* __init__: Create a screen object based on an entry in the config file with a type equal to the type string registered
  in the definition of the screen.
* InitDisplay(nav): code to display the screen. nav are the navigation keys or None and should be passed through the
  underlying InitDisplay of ScreenDesc
* ReInitDisplay: code to redisplay the screen if it has been removed temporarily and assumes nav keys are already set.
  Generally not overridden.
* ISYEvent(node,value): A watched ISY *node* has changed to the new *value*
* ExitScreen: code that is called as the screen is being taken off the display

## Defining New Alert Procs
Alert procs are defined as methods in classes stored in the alerts directory.  They have a single module level line of code of the form "config.alertprocs["*classname*"] = *classname*" where *classname* is the name of the class defined in the module.  The class will be instantiated once at console start time.  It may define one or more methods that will be called based on the definition of Alerts in the config file that the console reads.

## Diagnostic Support
Corresponding to each Console.log file in the Console directory there is a hidden directory **.HistoryBuffer that may contain diagnostic information.  When certain errors occur or upon user command the console will dump a recent history of all key events that have occurred over as much as the previous 5 minutes.  This includes very detailed diagnostic information from internal task lists and event queues as well as items that have been received from the hubs.

