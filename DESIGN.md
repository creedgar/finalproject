DESIGN.md
We struggled to get our website started, so we took all of CS50's finance website, then started changing it into our website. Small css changes in our website logo were made, but we kept the style of the nav-bar and most buttons from CS50. We also used ideas from W3 schools and many other websites (cited in our code) to get buttons of different style, tiles of different styles, etc. We struggled to create a lot of our functions (especially search, which took hours of thinking, writing, and debugging). It was also hard to get a fully functioning website because we originally developed building.html as a page only for Kroon Hall. It was difficult to universalize that page.

The file app.py contains the routes to all our HTML pages and the pages themselves are stored in a templates folder. The map.html file our website’s homepage and it contains a screenshot of the Yale interactive map, with markers representing different areas of the campus, embedded in the code as an SVG file. Using an SVG file allowed us to easily add CSS styling and the ‘onclick’ feature to the circle markers, seamlessly connecting them to six main area pages.

The circle markers actually all lead to one page, area.html, because we decided to universalize the area pages as opposed to have an individual page for each area although there are still individual routes in app.py and, in these routes, we conduct a SQL query where we search the database and retrieve the information relevant to the buildings in the area being displayed. The SQL query is hardcoded to retrieve information that contains the relevant location id. What is displayed to the user depends on the marker they select and to achieve this we used jinja syntax in the HTML code to input the information that we retrieved from the database. Using jinja allowed us to write generalized html code where the resulting display was specific to the relevant building, avoiding redundancy. The area page contains a tile layout of all the buildings in the area, and we were able to use jinja syntax to retrieve the relevant images for each individual building. The image tiles are clickable and to achieve this we used the <form> HTML tag as opposed to simply using a button or an anchor tag as this gave us more information about the information being sent back to server, which we could use in future pages.

Following area.html, the user presumably selects a building and we utilized a similar strategy of a universalized page populated with information from a SQL query which uses information from the GET request sent from the area.html page.

On search pages, building pages, and amenities pages, we used get and post methods in python to input our database into html. Once in html, we used jinja to fill the webpages with the data from python. We used a lot of code from finance, such as login, logout, register, and apology. We made app routes for each individual area in app.py because each individual area has its own data. The submit, review, and many other functions were heavily inspired by finance, since it helped us learn how to develop certain aspects of a webpage. Our search function dynamically fills a string called check, which starts with “SELECT * FROM amenities WHERE” and ends with user input queries.

We’ve had troubles in our project with the user going back, since a lot of our pages require the input of our databases through “POST” to function. Since so many of our pages require databases input through the “POST” method, we had some struggles with the browser’s back button not working. We think that now the browser’s back buttons should work, but just in case they don’t, we added back buttons to pages in the website to help the user navigate through the website. 

The style and aesthetic of search, submit, and review would be changed and universalized next if we were to continue with this project. These pages have relatively basic styles, and some features, such as the search table, that are awkward sizes, and don’t fit into the ideal size. 

  
We are proud that our website runs as it does, and we hope everyone enjoys Faucets and Fountains!