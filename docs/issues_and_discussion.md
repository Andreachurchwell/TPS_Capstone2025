# Hardest Issues Faced in My Weather App Project

This markdown is just a running list of some of the hardest issues I’ve run into during my capstone weather app build. It’s not fancy — just documenting stuff that challenged me and how I got around it (or what I’m still working on).

---

## 1. Splash Screen Issues
**Problem:** My splash screen wouldn’t show up right — sometimes it wouldn’t appear at all or it froze the app.

**Fix:** I had to play around with how long it stayed visible and how to load it without blocking the main GUI. Eventually, I got it working using `after()` and making sure it didn’t slow down the rest of the window.

---

## 2. Autocomplete Pulling Wrong Location
**Problem:** When I typed a city like “Knoxville, CA”, it pulled weather for “Knoxville, TN” because the API was using only the city name.

**Fix:** I upgraded my custom `AutocompleteEntry` widget to store the selected city’s `lat` and `lon`. Then I changed `get_weather()` to check for selected coords and use a new `fetch_current_weather_by_coords()` function instead of the city name. That finally gave me accurate results.

---

## 3. Live Radar Confusion
**Problem:** I wanted a real live radar, but it was confusing to figure out how to get it working with OpenWeather’s tile layers. Most layers like wind, temp, radar, and clouds weren’t showing up right — some were just blank or weird colors.

**Fix:** Still in progress. I added a dropdown that lets me switch map tile layers, but getting them to display correctly is ongoing. Might be a zoom level issue or something with how tiles are being rendered.

---

## 4. Upgrading to OpenWeather Dev Plan
**Problem:** I wasn’t sure what features I could actually use until I upgraded. I didn’t know if I could access 16-day forecasts or map layers.

**Fix:** Once I upgraded, I realized I had access to 7, 10, and 16-day forecasts, plus map features and more detailed data. I started using the full range of forecast data, which meant updating how I handled longer forecasts and their visuals.

---

## 5. Forecast Popup + Layout Overhaul
**Problem:** My forecast popups were messy, hard to style, and too cramped to show charts.

**Fix:** I need to build the layout to be more scrollable and spacious. I also styled the popups to match my main app and made sure I could fit Matplotlib charts inside. This took some trial and error, especially with widget sizing and dark mode styling.

---

## 6. Debug Print Overload
**Problem:** I had too many `print()` statements during debugging. It cluttered the terminal and made it hard to see real errors.

**Fix:** I eventually searched for all `print()` statements using regex in VS Code and commented them out. I also cleaned up my logs to only show helpful messages.

---

## 7. Switching to a Modular Layout
**Problem:** At first all my code was in one big file. As things grew, it became messy and hard to manage.

**Fix:** I split the app into folders like `core/`, `features/`, and `gui/`. This helped me organize things better but took time to figure out how to pass data (like `lat/lon`) between files and avoid circular imports.

---

## 8. Figuring Out ML
**Problem:** I wasn’t sure how to bring machine learning into the project once I had real forecast data.

**Fix:** Still working on this, but I’m now thinking of using ML to predict weather conditions or extend forecasts. For now, I’m focusing on finishing the UI and visuals first.

---

## 9. Chart Rendering Errors (Short-lived)
**Problem:** I got an error trying to chart the 7-day forecast — something about converting `'N/A'` to float.

**Fix:** Didn’t dive deep at the time. I just switched to a bar chart and started thinking more about cleaning data before visualizing. Might revisit this later.

---

## Notes
Still a lot more to come — but this covers the big stuff so far.
