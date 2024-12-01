# Sir Squirrel Assistant
Sir Squirrel Assistant is a helpful tool for the game Limbus Company by Project Moon. No longer will you need to hit the mines as Sir Squirrel will do it for you.

Do note that this has not yet been updated for Mirror Dungeon 5, but it should work regardless provided Project Moon does not greatly change Mirror Dungeon. Sir Squirrel will hit Version 1.0 when i have finished up all the work to make it compatible for Mirror Dungeon 5

UPDATE 22/11/2024: Due to the proposed changes for MD5, i will take quite awhile to update sirsquirrel so please be patient
I will also list here the things that need fixing so you can have a rough update

Added on 28/11 Update
- [x] MD5 Setup
- [x] New Theme Packs
- [x] Grace of the Dreaming Star
- [x] EGO Gift Selection (Slash, Pierce, Blunt Removed)
- [x] Pack Selection (3 Refreshes now instead of 1)
- [x] Reward Selection (No Starlight)
- [x] Abnormality Battles
- [x] Pack Exclusions
- [ ] Duplicate EGO Gifts
- [x] Market / Reststop Combined

Added on 5/12 Update
- [ ] New Choice Events
- [ ] ???

# Features
There are already other auto mirror dungeon tools out there so why should you use Sir Squirrel instead. Well here's why
* E.G.O Gift Choice
    * The ability to choose which status you want to use throughout the run
* Auto Squad Rotation
    * In conjuction with the E.G.O Gift Choice you can also choose multiple statuses and Sir Squirrel will cycle through them every one and follow the gifts accordingly
    * Choose the squad order for each team and Sir Squirrel will follow it
* Pack Selection
    * Automatically choose packs based off your E.G.O Gift as well as using a priority list for packs for each floor
    * Note that due to the nature of how it works which is win-rating through battles certain packs are already prefiltered to be excluded such as
        * Skin Prophet
        * Bamboo Kim
        * Slithcurrent
* E.G.O Gift Enhancement
    * Sir Squirrel upgrades E.G.O Gifts of the status you chose along with keywordless gifts at rest stops
* E.G.O Gift Purchase
    * Sir Squirrel purchases E.G.O Gifts according to the status you chose as well as keywordless gifts
* Resolution Aware
    * Sir Squirrel now works regardless of resolution

# Planned Features
These are features i intend to add when i have time for Sir Squirrel development
* Using EGO in battle
    * Shifted to low priority not necessary for now

* Auto Luxcavation, Threads and Dailies
    * Shifted to low priority due to mainly focusing on the eventual MD5 update

* GUI
    * A GUI might be more convienient for users

* Exception Handling
    * As of right now i do not check for a fair bit of things that can impact Sir Squirrel's performance mainly due to getting a workable product out first but i do intend to add more error messages and handling when i'm more free.

* Any Suggestions or Enhancements i can make to Sir Squirrel based on feedback that is feasible for development

# Known Issues
Need more feedback pertaining to the Resolution Aware version.

# Bug Reporting
Please let me know about any issues you face with Sir Squirrel and I will do my best to look into it.

For Bug Reports please follow the following format
* Squirrel Log Output
    * Sir Squirrel logs its actions into a file called Squirrel.log, please provide the output of the log when submitting your issue
    * Sir Squirrel also takes a screenshot whenever it runs into an issue, this can be found in the folder Error followed by the timestamp
* Be Descriptive about the issue
    * If you face an issue do let me know at which part did Sir Squirrel fail like which part did it fail at for example, in battle?, marketplace? , reststop?, during an event? and if so what event is it so i can look it up
    * Any accompanying screenshot of what it was stuck on would also be great
    * Describing the behaviour of what is happening would also be great  for example: clicking on things it shouldnt be clicking.

So an example bug report would be something like
### Example Squirrel.log output (just needs to be around the time you encountered an issue)
```
2024-10-07 19:48:58,588 - src.mirror - INFO - Selecting Squad for Battle
2024-10-07 19:49:03,468 - src.mirror - INFO - Loading
2024-10-07 19:49:11,019 - src.core - INFO - Starting Battle
2024-10-07 19:51:51,991 - src.core - INFO - Battle Event Check
2024-10-07 19:52:36,530 - src.core - INFO - Battle Event Check
2024-10-07 19:52:39,757 - src.core - INFO - Skill Check
```
Sir Squirrel was stuck at a skill check for Doomsday clock where it doesn't click on the option for the skill check

# Instructions
Do note that due to the current nature of how Sir Squirrel operates a few things need to be properly set before running it which i will outline here.
Sir Squirrel also has a keypress combination to stop it forcefully at any point by pressing (CTRL + Q)

1) Sir Squirrel now works with all resolutions. Please run it in borderless windowed
    * To use borderless fullscreen, press Alt+Enter on your keyboard while Limbus Company is in windowed mode.

3) Edit the files in the config folder before running
    * Although i have already prefilled the files, i still recommend you make edits tailoured towards your own teams

### status_selection.txt
#### Example status_selection.txt
```
sinking
burn
rupture
tremor
charge
poise
bleed
slash
blunt
pierce
```
You can follow this format and simply omit whichever statuses you do not want to use. So if you plan to only use sinking and tremor, your status_selection.txt should look something like this. The order is top to bottom so sinking will be first followed by tremor.
```
sinking
tremor
```
You also need not worry if you are running the bot more times than the number of statuses you have as it will simply cycle through the statuses accordingly. So using our above example of sinking and tremor, if you are running the Sir Squirrel 5 times it will run as follows:
```
sinking
tremor
sinking
tremor
sinking
```
Do note the default behaviour should there be any typos of any sort is to use Poise as the gifts.
### squad_order.json
#### Example squad_order.json
```
{
    "tremor": {
        "yisang": 12,
        "faust": 1,
        "donquixote": 7,
        "ryoshu": 8,
        "meursault": 6,
        "honglu": 3,
        "heathcliff": 5,
        "ishmael": 4,
        "rodion": 2,
        "sinclair": 9,
        "outis": 10,
        "gregor": 11
    },
    "rupture": {
        "yisang": 1,
        "faust": 6,
        "donquixote": 3,
        "ryoshu": 7,
        "meursault": 8,
        "honglu": 2,
        "heathcliff": 9,
        "ishmael": 10,
        "rodion": 11,
        "sinclair": 4,
        "outis": 5,
        "gregor": 12
    }
}
```
I used the json format simply because it is way more convinient and also provides a pretty easy way for you to customize the squad order for each statuses. Simply edit the numbers for the team from 1 to 12, and double check you only have 1 of each number for the specific status as per the example. I have the file already populated with every possible team. Default will simply use the team that was already selected if it cannot find your squad name.

You will also need to edit your squads to use the name of the status you want to use as per the example below

If you do not know how to edit your squad names heres how:
1) Go to Sinners
![Step 1](/img/squad1.png)
2) Click on a team at the side
![Step 2](/img/squad2.png)
3) Click on the pencil icon at the top
![Step 3](/img/squad3.png)
4) Scroll and click on the corrosponding keyword
![Step 4](/img/squad4.png)
Your team name should look something like this

![Squads Example](/img/Squads.png)

### f1/f2/f3/f4.txt
#### Example f1.txt
```
pictures/mirror/packs/f1/forgotten.png
pictures/mirror/packs/f1/gamblers.png
pictures/mirror/packs/f1/unloving.png
pictures/mirror/packs/f1/nagel.png
pictures/mirror/packs/f1/outcast.png
pictures/mirror/packs/f1/erosion.png
pictures/mirror/packs/f1/nest.png
pictures/mirror/packs/f1/factory.png
```
By default Sir Squirrel will pick packs based on the same E.G.O status you have chosen but will use the list if it can't find any E.G.O Status or if there are pack exceptions present in the list. The following are the exempted packs as they contain bosses that can't be beat by win-rating. Also note not to include this in the respective f2/f3/f4.txt as it will pick them if you include it
```
"pictures/mirror/packs/f2/violet.png"
"pictures/mirror/packs/f3/crawling.png"
"pictures/mirror/packs/f3/slicers.png"
"pictures/mirror/packs/f3/flood.png"
"pictures/mirror/packs/f4/wrath.png"
"pictures/mirror/packs/f4/burning.png"
"pictures/mirror/packs/f4/yield.png"
"pictures/mirror/packs/f4/sloth.png"
```
The order for the pack is top to bottom. You can reference which packs contain which bosses using the link from the wiki [List of Floor Themes](https://limbuscompany.wiki.gg/wiki/List_of_Floor_Themes) after which you can refer to the names of the pack pictures in "pictures/mirror/packs/f(X)" where X is the floor number


3) Running the Bot
* Follow the pictures on how to run the bot. Make sure limbus company is running in borderless windowed as explained above and is at the home menu screen where the bar is present

Firstly Navigate to where you unzipped Sir Squirrel where sirsquirrel.exe is at, followed by clicking the top of the bar (Example is for Windows 11 but its the same for Windows 10)

![Step 1](/img/run1.png)

Next type in cmd as shown

![Step 2](/img/run2.png)

A command prompt should open up as shown

![Step 3](/img/run3.png)


Next simply type in `sirsquirrel.exe X` replacing X with the number of times you want to run Sir Squirrel. So for the example below i am running Sir Squirrel 5 times.

![Step 4](/img/run4.png)

Note that if you are in powershell there should be a PS infront then you should be using `.\sirsquirrel.exe X`

![Step 4 Optional](/img/powershell.png)


4) Enjoy
