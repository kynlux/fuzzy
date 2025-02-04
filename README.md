# fuzzy
> fuzzy is game made in 3 hours lmao

> i aint deleting deprecated things from this game, lets make a keybind hell in config menu

fuzzy is low-quality game made for practicing number typing and memory (a little)

## Gameplay
### Config Menu
on join you face config menu (its empty), you have total of 6 commands (currently):
- **x** - exit from menu and start game
- **r** - record how much time you lost on single session and display it after game (set to 0, any value expect 0 will count as enabled)
- **m** - change range of numbers (currently from 0 to your number)
- **l** - set maximum lives for current session (default is 0, meaning you will lose instaly if not changed)
- **e** - set value that will make your seesion automaticly end if you reach score that you typed
- **2** - enable scoreV2
- **3** - enable scoreV3

small notice, you can chain commands, so you can do `l1r1` to set lives to 1 and enable time recording

pro tip: do `l1r1 21x` to be good at game
#### NOTE: config resets after restart


## Scoring System
scoring systems are made for different purposes and ideas, use them if you like them or your friend says to use certain one
### ScoreV1
- Infinity answer timing to get score
- Score increases by 1 every right answer

### ScoreV2
- Has combo mechanic (useless) (resets after losing a life)
- Giving score on your typing speed
  
### ScoreV3
- Has combo mechanic (multiplying score by `(combo / 10) + 1`) (resets after losing a life OR late answer)
- Additional score points base on number size (`(number / 100) + 1`)
- Higher answer timing than ScoreV2

### Actual Game
you have 1.65s of remebering number, after it its disapears and you must type it to get score and other things (based on your config)

i will try do best things to game to make it funny

## Roadmap to v1.0.0
- [x] ScoreV3 (better version of scoreV2)
- [ ] Custom timing for ScoreV2/V3 rewards
- [ ] Make unique challenges
