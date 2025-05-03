# GTD (Global Terrorism Database) Visualization App

This application provides an interactive visualization of the Global Terrorism Database (GTD), enabling users to explore terrorism-related data through a user-friendly interface.

## Features

* Interactive data visualizations of terrorism incidents.
* Filtering options by year, region, attack type, and more.
* User-friendly interface for data exploration.

## Prerequisites

* Python 3.9 was used, but older versions like 3.6 or higher installed on your system should work.
* Git installed for cloning the repository.([Domino Data Lab][2])

## Setup Instructions

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/Sydney-Anuyah/gtd.git
cd gtd
```

OR

Download the zip code and unzip in you folder.
Then navigate to the directory through your command line on windows or terminal on mac.

For me datapath looked something like "Downloads/gtd" which resulted in:

```bash
cd Downloads/gtd
```



### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

* **On Windows:**

```bash
  python -m venv gtd_env
  gtd_env\Scripts\activate
```



* **On macOS/Linux:**

```bash
  python3 -m venv gtd_env
  source gtd_env/bin/activate
```



### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```



### 4. Run the Application

Start the application using:

* **On Windows:**
```bash
python app.py
```
* **On macOS/Linux:**
```bash
python3 app.py
```



The application will start, and you can access it by navigating to `http://127.0.0.1:8050/` in your web browser.

## Project Structure

```plaintext
gtd/
├── GTD_Dataset.csv       # Dataset file
├── Procfile              # For deployment (e.g., Heroku)
├── README.md             # Project documentation
├── app.py                # Main application script
├── render.yaml           # Deployment configuration
└── requirements.txt      # Python dependencies
```



## Deployment

The presence of `Procfile` and `render.yaml` suggests readiness for deployment on platforms like Heroku or Render. Ensure you have the necessary configurations and environment variables set up as per the chosen platform's requirements.


## Acknowledgment
**Thank you Jesus Christ for being my Number 1 lover.** 
Thank you to Mum and Dad my biggest supporters.
Thank you Bolade Victor for all your support and help with the debugging process
Thank you to Mikaylah Stumbo and Junaid Mohammed for making this project a great success
Thank you to the team that gave the dataset.

Principal Investigators for the GTD: Gary LaFree, Laura Dugan, and Erin Miller
Research Staff for the GTD
Bryan Arva
Jeremy Backstrom
Brad Bartholomew
Brandon Behlendorf
Carlos R. Colon
Stephanie DiPietro
Michael Distler
Benjamin Evans
Susan Fahey
Heather Fogg
Derrick Franke
Nadine Frederique
Paul Gallo
Jennifer Gibbs
Rachelle Giguere
Margaret Hayden
James Hendrickson
Omi Hodwitz
Amy Iandiorio
Michael Jensen
William Kammerer
Sheehan Kane
Raven Korte
Oleksiy Krylyuk
Deepak Kukade
Sumit Kumar
Jacob Loewner	Anna Meier
Lauren Metelsky
Mary Michael
Danna O'Rourke
Joseph Oudin
Christopher Panek
Karina Panyan
Shelsea Pederson
Alexandra Prokopets
Kieran Quinlan
Amanda Quinn
Matthew Rhodes
Benjamin Rosenbaum
Aaron Safer-Lichtenstein
Ingrid Schulz
Jeffrey Scott
Crystal Shelton
Jaime Shoemaker
Joseph Simone
Corina Simonelli
Kimberly Tenorio
Mischelle van Brakle
Katharine Sobotka von Rosen
Jennifer A. Varriale-Carson
Brian Wingenroth
Tyler Yates


## References
National Consortium for the Study of Terrorism and Responses to Terrorism). (2022). Global Terrorism Database 1970 - 2020 [data file]. https://www.start.umd.edu/gtd


For any issues or contributions, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Sydney-Anuyah/gtd).



[1]: https://discuss.python.org/t/why-cant-install-packages-with-requirements-txt/38239?utm_source=chatgpt.com "Why can't install packages with requirements.txt? - Python Help"
[2]: https://docs.dominodatalab.com/en/latest/user_guide/9c4f82/use-requirements-txt-python-only/?utm_source=chatgpt.com "Use requirements.txt (Python only) - Domino Data Lab"
[3]: https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/?utm_source=chatgpt.com "Create virtual environment in Python | GeeksforGeeks"
