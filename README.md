# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/microphone.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Announcer
Announces specified phrases at specified times

## About
Announces specified phrases at specified times.

## How To Use
* Open file in ~/MycroftUserSkillsData/announcements.txt
* Enter an announcement in format "\<time\>|\<announcement\>|\<frequency\>"
  * time: (str format: HH:MM:SS) Eg. 09:01:03 is 9:01:03 seconds. 
  * announcement: (str) Phrase you want mycroft to speak at the specified time.
  * frequency: (str) Time interval between repetitions of this announcement in seconds. Eg. 3600:1 hour, 86400:24 hours, 604800:Weekly
  * Ensure that each announcement is on a different line
  
## Notes:
* After adding a new announcement, you must reload the AnnouncerSkill.
* If the time for the announcement has passed today, it will be set for the next day.
  
## Examples
* "Announce this at time"

## Credits
blimyj

## Category
**Daily**
Productivity

## Tags
#Announce

