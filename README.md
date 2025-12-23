# PetPal
PetPal is a fun, interactive pet care game! Feed, nurture, and entertain your pet in order to keep it alive and happy! 

Either run the .py file if you have python or copy+paste into your IDE and run it there!

4/15/2025
- ~30% of the game has been rewritten to JavaScript. HTML and CSS has been complete.
- Reworked the 'Feed' 'Sleep' and 'Play' rooms
- New Fluffel model (temporary)
- Reworked stat progress(from Text: value -> Text: progress bar)

4/15/2025 
-Began porting game over to browser-based game using JS, HTML, and CSS

12/2022/2025
Transition from Tkinter -> Pygame
--
_Old(Tkinter): Before, it was Event-Driver. The program relied on the operating system to tell it when to wake up_

**New(Pygame): It's now Loop-Driven. The code runs 60 times per second, the engine is constantly recalculating logic, checking for input, and redrawing the screen.**
--
_Old(Tkinter): Pet stats only dropped when an action was performed, if a button was never clicked, it would live forever in a frozen state._

**New(Pygame): Introduced Delta Time (dt). Stats now decay in real-time based on the clock. If you leave the game running and walk away, hunger drops slowly**
--
_Old(Tkinter): Used Widgets_

**New(Pygame): Everything is Blitted. I moved away from standard system buttons and now every 'button' and 'bar' is now a custom shape drawn directly onto the "Surface"(screen). This allows for higher customization later on or for the user.**
--
_Old(Tkinter): Static and "snappy". When a stat changed, text simply updated._

**New(Pygame): Frame-rate independence. Because the game now  updates every few millisecondds, i've added an "Idle Bounce" logic. Pet now subtly vibrates/bounces while alive, giving it a sense of 'breathing'**
--
_Old(Tkinter): Mini-games(like Catch the Ball) required opening a Toplevel (second window)_

**New(Pygame): While the old version used buttons, Pygame allows mini-games to happen on the same screen by changing what "State" the loop is drwaing**
--
_Old(Tkinter): Stats were displayed as raw text (Hunger:50)_

**New(Pygame): Added Graphic Progress Bars. Users can now visiually see their pet's health "drain" as the green bar shorten.**
------------

Next in the pipeline.
-Replcace the PURPLE_CIRCLE placeholder with PET_SPRITE_SHEET.
-Implement SOUND_SYSTEM for munching and playing effects
-Add SAVE_STATE functionality to track pet growth across sessions.
