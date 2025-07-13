Week 13 Reflection – Progress & What's Next
This week was a mix of testing, fixing, and trying to figure out how I want to move forward. I spent a good chunk of time dealing with the weather map tiles. I’ve been trying to get one tile layer (like radar, wind, temp, etc.) to overlay properly on the main map, but every time I select one, the base map disappears and only the tile shows. I haven’t solved that yet, but I’m now thinking about possibly combining the tile layers with my live radar feature and scrapping the dropdown in the main window altogether.

I also cleaned up some parts of my project by removing unused files like radar_map.py, and I confirmed that nothing crashed after deleting them. I made sure the city autocomplete is working correctly with coordinates again — so if the user selects “Toronto, Kansas” instead of “Toronto, Canada,” the map and weather update accurately.

There were some things I wanted to do but didn’t quite get to — like adding the temperature trend chart to the main window. I tried working on it but wasn’t happy with how it looked, so I’ve held off on including it for now. Same with the layout file — I had planned to start separating my layout code into a layout.py file, but I haven’t done that yet either.

✅ What I Did This Week:
Troubleshooted tile map overlay issues (still not fully resolved)

Tested different visual ideas for trend charts (but didn’t finalize one)

Cleaned up unused files (like radar_map.py)

Fixed autocomplete issue with city selection and coordinates

Did more planning and thinking through the structure of the main window

🔜 To-Do List:
✅ Finalize map tile behavior — either fix the overlay or remove the dropdown

🔲 Add current timestamp to the main window and animated radar

🔲 Revisit temp trend chart for the main window

🔲 Possibly start layout.py file to clean up layout logic

🔲 Decide whether to keep forecast popups or embed them in the main window

🔲 Begin work on the team feature next week

🔲 Make sure everything is up to date on GitHub with a clear README

🔲 Integrate ML if there’s time — even something simple like a prediction or trend

This week was more about cleanup, testing, and figuring things out than major features — but it helped me get a better idea of where I’m stuck and what needs to happen next. I’m hoping to hit the ground running this upcoming week.