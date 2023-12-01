# Protein-Value-Energy-Efficiency-Products
A very simple project where I aim to automate the analysis of protein value both in terms of cost and energy requirements at different shops (at least through their website) across the world (multiple countries) to determine the best snacks to buy for building muscle.

#Covered websites so far
1. Dia (Spain) - [No multiple results automated pull in] - still uses the Inspect method
2. Aldi (UK) - [Working multiple results automated pull in] - 80% effective - still uses the inspect method
3. Carrefour (Spain) = Not at all [started]

Currently all code is written in Python and requires the computer to actively interact with the website to defeat bot blockers etc. If you are interested in how it works, look at the code or contact me. 
The code takes a link to a product and from there will open the webpage automatically, grab the data, analyse the data and then put it into my database.
The database will be updated weekly and is made public for further analysis on my website. Crediting is required and copy and pasting is prohibitted, please add some value at least.
The basic premise started as copy all data from the webpage into a text file, save that and analyse it.
The second iteration was using the Inspect method and grabbing the body of a webpage to make it easier to analyse.
The third (most recent) iteration is using save webpage to HTML, this simply waits for the download to complete and requires far less code and risk as well as still allows analyses in HTML form to occur.
