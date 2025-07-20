Week 14 Reflection – From Forecast Failures to Fresh Fixes 🌩️🛠️
This week was full of ups and downs. It started out rough — my forecast buttons (especially 7-day, 10-day, and 16-day) were acting up, and I couldn’t figure out if the issue was on my end or something going on with OpenWeather. The app was freezing, my forecast popups were missing info, and I was starting to worry I'd have to undo days of work.

Eventually, I tracked the issue down to how I was handling the selected city coordinates. My app was defaulting to “Selmer” unless the user typed in a new city, even if they had already selected one. Once I fixed that, the forecasts worked again and the popups started behaving like they should.

During Asha’s office hour, she helped guide me through a much-needed improvement to my live radar setup. Instead of using a dropdown menu in the main window (which was clunky and limited), I moved all my tile layers (radar, clouds, wind, etc.) directly into the Leaflet-based popup using checkboxes. That update made the radar feature more powerful and user-friendly, and it cleaned up my UI at the same time.

Another win this week was finally getting serious about Git hygiene. I set up my .gitignore properly to exclude sensitive files like my API key text file and my local database. I also used git rm --cached to stop tracking weather.db, which made me feel way more confident about pushing to GitHub without risking security or clutter.

On the visual side, I added a new temp_trend_chart.py file that drops a mini trend chart into my main window. It's a good start, but it definitely still needs work to look polished and dynamic. I also started setting up a moon phase test file and have a few other features in progress that I want to clean up soon.

I also recorded a Loom walkthrough video this week to explain how my app works. At first, I struggled with getting the mic and screen settings to work, but once I got it figured out, I was able to walk through the key features: the current weather display, forecast buttons, live radar integration, and some of the visuals I’ve been working on. Making the video actually helped me realize how much progress I’ve made — and it’s a good practice run for my final presentation.

All in all, it was a chaotic but productive week. I hit some roadblocks, but I didn’t panic. I worked through them, asked for help when I needed it, and learned a lot — especially about debugging, explaining my work clearly, and managing a clean Git workflow.